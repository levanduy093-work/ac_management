#!/usr/bin/env python3
"""
FastAPI Web Server for PZEM-004T Data Monitoring
Provides REST API endpoints and web dashboard for data visualization
"""

import sys
import os
import asyncio
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
import json
import csv
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# FastAPI imports
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, Request, Depends, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from itsdangerous import URLSafeSerializer, BadSignature
from collections import deque

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import PZEMDatabase
 
# Serial and device control imports
try:
    import serial  # type: ignore
    import serial.tools.list_ports  # type: ignore
except Exception:
    serial = None  # Will check at runtime

try:
    from pzem import PZEM004T  # type: ignore
except Exception:
    PZEM004T = None  # Will check at runtime

# Initialize FastAPI app
DISABLE_DOCS = os.environ.get("DISABLE_DOCS", "true").lower() in ("1", "true", "yes")

app = FastAPI(
    title="PZEM-004T Monitoring API",
    description="REST API for PZEM-004T power monitoring data",
    version="1.0.0",
    docs_url=None if DISABLE_DOCS else "/docs",
    redoc_url=None if DISABLE_DOCS else "/redoc",
    openapi_url=None if DISABLE_DOCS else "/openapi.json",
)

# Load environment variables from .env if present
load_dotenv()

# Setup static files and templates
web_dir = Path(__file__).parent
static_dir = web_dir / "static"
templates_dir = web_dir / "templates"

# Create directories if they don't exist
static_dir.mkdir(exist_ok=True)
templates_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Initialize database
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'pzem_data.db')
database = PZEMDatabase(db_path)

# ===== Auth & security config =====
API_TOKEN = os.environ.get("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN must be set in .env for production deployment")

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-secret")
SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME", "acm_session")
serializer = URLSafeSerializer(SECRET_KEY, salt="acm-session")
COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "false").lower() in ("1", "true", "yes")

# Simple in-memory rate limiter for login attempts
_login_attempts: Dict[str, deque] = {}
LOGIN_MAX_ATTEMPTS = int(os.environ.get("LOGIN_MAX_ATTEMPTS", "10"))
LOGIN_WINDOW_SECONDS = int(os.environ.get("LOGIN_WINDOW_SECONDS", "300"))  # 5 minutes

def create_session_token(username: str) -> str:
    return serializer.dumps({"u": username, "t": int(time.time())})

def verify_session_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return serializer.loads(token)
    except BadSignature:
        return None

@app.middleware("http")
async def session_auth_middleware(request: Request, call_next):
    try:
        path = request.url.path
        if path.startswith("/static/"):
            return await call_next(request)

        # Login page and POST login are open
        if path in ("/login", "/logout") or path == "/":
            # Allow GET / to redirect if not logged-in; data API still protected below
            pass

        # Protect all /api/* endpoints with session cookie
        if path.startswith("/api/"):
            session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            session = verify_session_token(session_cookie) if session_cookie else None
            if not session:
                return JSONResponse(status_code=401, content={"success": False, "detail": "Unauthorized"})

            # Basic anti-CSRF for state-changing methods: require custom header
            if request.method in ("POST", "PUT", "PATCH", "DELETE"):
                if request.headers.get("X-Requested-With") != "XMLHttpRequest":
                    return JSONResponse(status_code=403, content={"success": False, "detail": "Forbidden"})
                # Check Origin when present (support reverse proxy/tunnel)
                origin = request.headers.get("Origin")
                if origin:
                    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or ""
                    allowed = set()
                    if host:
                        allowed.add(f"https://{host}")
                        allowed.add(f"http://{host}")
                    # Also allow explicit scheme from forwarded proto if present
                    xf_proto = request.headers.get("x-forwarded-proto")
                    if xf_proto and host:
                        allowed.add(f"{xf_proto}://{host}")
                    if origin not in allowed:
                        return JSONResponse(status_code=403, content={"success": False, "detail": "Invalid Origin"})
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})

# WebSocket manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Global variable to store last known USB port status
_last_usb_status = {}
_monitoring_task = None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    # Session cookie auth for WebSocket
    session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
    session = verify_session_token(session_cookie) if session_cookie else None
    if not session:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ===== WEB DASHBOARD ROUTES =====

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    # If not logged in, redirect to login page
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    session = verify_session_token(session_cookie) if session_cookie else None
    if not session:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/export", response_class=HTMLResponse)
async def export_page(request: Request):
    """Data export page"""
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    session = verify_session_token(session_cookie) if session_cookie else None
    if not session:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("export.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings and management page"""
    session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
    session = verify_session_token(session_cookie) if session_cookie else None
    if not session:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("settings.html", {"request": request})

# Login/logout routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_submit(request: Request, password: str = Form(...)):
    # Rate limit per client IP
    client_ip = request.client.host if request.client else "unknown"
    q = _login_attempts.setdefault(client_ip, deque())
    now = time.time()
    # remove old entries
    while q and now - q[0] > LOGIN_WINDOW_SECONDS:
        q.popleft()
    if len(q) >= LOGIN_MAX_ATTEMPTS:
        return JSONResponse(status_code=429, content={"success": False, "detail": "Too many attempts. Try later."})
    q.append(now)

    if password != API_TOKEN:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Invalid password"})
    token = create_session_token("admin")
    response = JSONResponse({"success": True})
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
        max_age=7*24*3600,
        path="/",
    )
    return response

@app.post("/logout")
async def logout_submit():
    response = JSONResponse({"success": True})
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return response

# ===== API ROUTES =====

@app.get("/api/stats")
async def get_database_stats():
    """Get database statistics"""
    try:
        stats = database.get_database_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== ENERGY RESET HELPERS =====

def _ensure_device_libs_available():
    if serial is None:
        raise HTTPException(status_code=500, detail="Thiếu thư viện 'pyserial'. Vui lòng cài đặt: pip install pyserial")
    if PZEM004T is None:
        raise HTTPException(status_code=500, detail="Không thể import PZEM004T. Kiểm tra thư mục 'src' và mô-đun 'pzem.py'.")

def _find_pzem_ports() -> List[str]:
    ports = []
    for port in serial.tools.list_ports.comports():
        desc_lower = (port.description or "").lower()
        device_lower = (port.device or "").lower()
        hwid_lower = (port.hwid or "").lower()
        keywords = ["pl2303", "usb-serial", "usb serial", "ch340"]
        if (
            any(k in desc_lower for k in keywords)
            or any(k in device_lower for k in keywords)
            or "vid:067b" in hwid_lower
        ):
            ports.append(port.device)
    return ports

def _get_pzem_info(port: str) -> Tuple[Optional[int], float, bool, Optional[str]]:
    device = None
    try:
        device = PZEM004T(port=port, timeout=2.0)
        address = device.get_address()
        if address is None:
            address = device.DEFAULT_ADDRESS
        measurements = device.get_all_measurements()
        energy = measurements.get("energy", 0.0) if measurements else 0.0
        return (address, energy, True, None)
    except Exception as exc:  # noqa: BLE001
        return (None, 0.0, False, str(exc))
    finally:
        if device:
            try:
                device.close()
            except Exception:
                pass

def _reset_pzem_isolated(port: str, target_address: Optional[int], verify_reset: bool) -> Dict[str, Any]:
    device = None
    result: Dict[str, Any] = {
        "port": port,
        "address": target_address,
        "energy_before": None,
        "energy_after": None,
        "success": False,
        "error": None,
    }
    try:
        device = (
            PZEM004T(port=port, address=target_address, timeout=1.0)
            if target_address is not None
            else PZEM004T(port=port, timeout=1.0)
        )

        before = device.get_all_measurements()
        energy_before = before.get("energy", 0.0) if before else 0.0
        result["energy_before"] = energy_before

        success = False
        for _ in range(3):
            try:
                if device.reset_energy(verify_reset=False):
                    success = True
                    break
                time.sleep(0.2)
            except Exception as exc:  # noqa: BLE001
                result["error"] = str(exc)
                time.sleep(0.3)

        if not success:
            result["success"] = False
            return result

        # Allow device time to process
        time.sleep(1.0)

        after = device.get_all_measurements()
        energy_after = after.get("energy", 0.0) if after else 0.0
        result["energy_after"] = energy_after

        if not verify_reset:
            result["success"] = True
            return result

        result["success"] = (energy_after < energy_before) or (energy_after == 0.0)
        if not result["success"] and result["error"] is None:
            result["error"] = "Không xác minh được reset (năng lượng không giảm)"
        return result
    except Exception as exc:  # noqa: BLE001
        result["success"] = False
        result["error"] = str(exc)
        return result
    finally:
        if device:
            try:
                device.close()
            except Exception:
                pass

def _reset_all_pzems_sequential(verify_reset: bool) -> Dict[str, Any]:
    detected = _find_pzem_ports()
    if not detected:
        raise HTTPException(status_code=404, detail="Không phát hiện thiết bị PZEM nào")

    devices_info: List[Dict[str, Any]] = []
    for p in detected:
        addr, eng, ok, err = _get_pzem_info(p)
        if ok:
            devices_info.append({"port": p, "address": addr, "energy": eng})
        else:
            devices_info.append({"port": p, "address": None, "energy": 0.0, "error": err, "skipped": True})

    valid = [d for d in devices_info if not d.get("skipped")]
    if not valid:
        raise HTTPException(status_code=404, detail="Không có thiết bị PZEM hợp lệ")

    addresses = [d["address"] for d in valid if d.get("address") is not None]
    duplicate_addresses = [a for a in set(addresses) if addresses.count(a) > 1]

    results: List[Dict[str, Any]] = []
    for dev in valid:
        res = _reset_pzem_isolated(dev["port"], dev.get("address"), verify_reset)
        results.append(res)
        # Wait longer between devices with duplicate address
        if dev.get("address") in duplicate_addresses:
            time.sleep(2.0)
        else:
            time.sleep(1.0)

    total = len(results)
    success_count = sum(1 for r in results if r.get("success"))
    fail_count = total - success_count
    return {
        "detected_ports": detected,
        "results": results,
        "summary": {
            "total": total,
            "success": success_count,
            "failed": fail_count,
            "duplicate_addresses": duplicate_addresses,
        },
    }

@app.get("/api/database/stats")
async def get_database_stats_detailed():
    """Get detailed database statistics (alternative endpoint)"""
    try:
        stats = database.get_database_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensors")
async def get_sensors():
    """Get sensor summary"""
    try:
        sensors = database.get_sensor_summary()
        return {
            "success": True,
            "data": sensors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/measurements")
async def get_measurements(
    limit: int = Query(100, description="Number of measurements to return"),
    port: Optional[str] = Query(None, description="Filter by sensor port"),
    days: Optional[int] = Query(None, description="Filter by last N days"),
    sensor_id: Optional[int] = Query(None, description="Filter by sensor ID")
):
    """Get measurements with optional filtering"""
    try:
        if port:
            data = database.get_measurements_by_port(port, limit)
        else:
            data = database.get_latest_measurements(limit)
        
        # Filter by date if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            data = [
                record for record in data 
                if datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date
            ]
        
        return {
            "success": True,
            "data": data,
            "count": len(data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== ENERGY RESET API =====

@app.post("/api/energy/reset")
def reset_energy(
    port: Optional[str] = Query(None, description="Cổng muốn reset. Bỏ trống để reset TẤT CẢ."),
    verify: bool = Query(True, description="Xác minh sau reset bằng cách đọc lại năng lượng"),
):
    """Reset bộ đếm năng lượng trên thiết bị PZEM-004T.

    - Nếu cung cấp `port`: reset thiết bị trên cổng đó.
    - Nếu không: reset tất cả thiết bị tìm thấy tuần tự.
    """
    try:
        _ensure_device_libs_available()

        if port:
            # Optional: quick validation that port exists
            available_ports = [p.device for p in serial.tools.list_ports.comports()]
            if port not in available_ports:
                # Still allow attempt, but mark a note
                note = "Cổng không nằm trong danh sách phát hiện. Vẫn thử reset."
            else:
                note = None

            addr, energy, ok, err = _get_pzem_info(port)
            if not ok:
                raise HTTPException(status_code=404, detail=f"Không thể kết nối tới {port}: {err}")

            res = _reset_pzem_isolated(port, addr, verify)
            return {
                "success": res.get("success", False),
                "mode": "single",
                "note": note,
                "data": res,
                "timestamp": datetime.now().isoformat(),
            }

        # Reset all devices
        batch = _reset_all_pzems_sequential(verify)
        return {
            "success": batch["summary"]["failed"] == 0,
            "mode": "all",
            "data": batch,
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi reset năng lượng: {str(e)}")

@app.get("/api/measurements/range")
async def get_measurements_by_date_range(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    port: Optional[str] = Query(None, description="Filter by sensor port")
):
    """Get measurements within a date range"""
    try:
        # Validate dates
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Include end date
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Get data
        if port:
            data = database.get_measurements_by_port(port, 10000)  # Large limit
        else:
            data = database.get_latest_measurements(10000)
        
        # Filter by date range
        filtered_data = []
        for record in data:
            record_dt = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
            if start_dt <= record_dt <= end_dt:
                filtered_data.append(record)
        
        return {
            "success": True,
            "data": filtered_data,
            "count": len(filtered_data),
            "date_range": {
                "start": start_date,
                "end": end_date
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard")
async def get_dashboard_data(
    port: Optional[str] = Query(None, description="Filter by sensor port"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """Get comprehensive dashboard data, optionally filtered by sensor"""
    try:
        # Get all dashboard data in one call
        stats = database.get_database_stats()
        sensors = database.get_sensor_summary()
        
        # Get measurements - filtered by port if specified
        if port:
            latest_measurements = database.get_measurements_by_port(port, 50)
            # Filter sensors to only include the selected one
            selected_sensors = [s for s in sensors if s['port'] == port]
        else:
            latest_measurements = database.get_latest_measurements(50)
            selected_sensors = sensors
        
        # Calculate summary statistics for selected data
        if latest_measurements:
            if port:
                # Single sensor - latest_measurements already filtered by port from database
                # Take the most recent measurement (first item, already sorted by timestamp DESC)
                latest = latest_measurements[0]
                total_power = latest['power'] if latest['power'] is not None else 0.0
                total_energy = latest['energy'] if latest['energy'] is not None else 0.0
                avg_voltage = latest['voltage'] if latest['voltage'] is not None else 0.0
                sensor_count = 1
            else:
                # All sensors - aggregate data from all sensors
                # Group by port to get latest measurement per sensor for power calculation
                sensor_latest = {}
                for m in latest_measurements:
                    if m['port'] not in sensor_latest:
                        sensor_latest[m['port']] = m
                
                total_power = sum(m['power'] for m in sensor_latest.values() if m['power'])
                total_energy = sum(m['energy'] for m in sensor_latest.values() if m['energy'])
                avg_voltage = sum(m['voltage'] for m in sensor_latest.values() if m['voltage']) / len(sensor_latest) if sensor_latest else 0
                sensor_count = len(selected_sensors)
        else:
            total_power = 0
            total_energy = 0
            avg_voltage = 0
            sensor_count = len(selected_sensors)
        
        # Build chart data
        chart_data: List[Dict]
        if start_date and end_date:
            # If date range is provided, return full data for that range
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

            # Pull a large window then filter by date range
            if port:
                range_source = database.get_measurements_by_port(port, 100000)
            else:
                range_source = database.get_latest_measurements(100000)

            chart_data = [
                r for r in range_source
                if start_dt <= datetime.strptime(r['timestamp'], '%Y-%m-%d %H:%M:%S') <= end_dt
            ]
        else:
            # Default: last 24 hours from the available latest measurements
            cutoff_time = datetime.now() - timedelta(hours=24)
            chart_data = [
                record for record in latest_measurements 
                if datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_time
            ]
        
        return {
            "success": True,
            "data": {
                "stats": stats,
                "sensors": sensors,
                "latest_measurements": latest_measurements,
                "summary": {
                    "total_power": total_power,
                    "total_energy": total_energy,
                    "avg_voltage": avg_voltage,
                    "sensor_count": sensor_count,
                    "selected_port": port
                },
                "chart_data": chart_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensor/{sensor_id}/stats")
async def get_sensor_stats(sensor_id: int):
    """Get statistics for a specific sensor"""
    try:
        # Get sensor info
        sensors = database.get_sensor_summary()
        sensor = next((s for s in sensors if s.get('id') == sensor_id), None)
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Get recent measurements for this sensor
        measurements = database.get_measurements_by_port(sensor['port'], 1000)
        
        if not measurements:
            return {
                "success": True,
                "data": {
                    "sensor": sensor,
                    "stats": None,
                    "recent_data": []
                }
            }
        
        # Calculate statistics
        voltages = [m['voltage'] for m in measurements if m['voltage']]
        currents = [m['current'] for m in measurements if m['current']]
        powers = [m['power'] for m in measurements if m['power']]
        energies = [m['energy'] for m in measurements if m['energy']]
        
        stats = {
            "voltage": {
                "min": min(voltages) if voltages else 0,
                "max": max(voltages) if voltages else 0,
                "avg": sum(voltages) / len(voltages) if voltages else 0
            },
            "current": {
                "min": min(currents) if currents else 0,
                "max": max(currents) if currents else 0,
                "avg": sum(currents) / len(currents) if currents else 0
            },
            "power": {
                "min": min(powers) if powers else 0,
                "max": max(powers) if powers else 0,
                "avg": sum(powers) / len(powers) if powers else 0
            },
            "total_energy": sum(energies) if energies else 0,
            "measurement_count": len(measurements)
        }
        
        return {
            "success": True,
            "data": {
                "sensor": sensor,
                "stats": stats,
                "recent_data": measurements[:20]  # Last 20 measurements
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_export_filename(format_ext: str, port: Optional[str] = None, days: Optional[int] = None) -> str:
    """Generate descriptive filename for exports"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    filename = "PZEM004T"
    
    # Add sensor info
    if port:
        port_name = port.replace('/dev/', '').replace('/', '_')
        filename += f"_{port_name}"
    else:
        filename += "_ALL_SENSORS"
    
    # Add time range info
    if days:
        filename += f"_last_{days}days"
    else:
        filename += "_all_time"
    
    # Add timestamp
    filename += f"_{timestamp}"
    
    # Add extension
    filename += f".{format_ext}"
    
    return filename

@app.get("/api/export/csv")
async def export_csv(
    port: Optional[str] = Query(None, description="Filter by sensor port"),
    days: Optional[int] = Query(None, description="Filter by last N days"),
    limit: Optional[int] = Query(None, description="Limit number of records")
):
    """Export data to CSV file"""
    try:
        # Get data
        if port:
            data = database.get_measurements_by_port(port, limit or 10000)
        else:
            data = database.get_latest_measurements(limit or 10000)
        
        # Filter by date if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            data = [
                record for record in data 
                if datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date
            ]
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found")
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            temp_filename = temp_file.name
        
        # Generate descriptive filename
        filename = generate_export_filename("csv", port, days)
        
        return FileResponse(
            temp_filename,
            media_type='text/csv',
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/json")
async def export_json(
    port: Optional[str] = Query(None, description="Filter by sensor port"),
    days: Optional[int] = Query(None, description="Filter by last N days"),
    limit: Optional[int] = Query(None, description="Limit number of records")
):
    """Export data to JSON file"""
    try:
        # Get data
        if port:
            data = database.get_measurements_by_port(port, limit or 10000)
        else:
            data = database.get_latest_measurements(limit or 10000)
        
        # Filter by date if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            data = [
                record for record in data 
                if datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date
            ]
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found")
        
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            json.dump({
                "export_timestamp": datetime.now().isoformat(),
                "total_records": len(data),
                "data": data
            }, temp_file, indent=2)
            temp_filename = temp_file.name
        
        # Generate descriptive filename
        filename = generate_export_filename("json", port, days)
        
        return FileResponse(
            temp_filename,
            media_type='application/json',
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cleanup")
async def cleanup_old_data(
    days_to_keep: int = Query(30, description="Number of days of data to keep")
):
    """Cleanup old data from database"""
    try:
        if days_to_keep <= 0:
            raise HTTPException(status_code=400, detail="days_to_keep must be positive")
        
        deleted_count = database.cleanup_old_data(days_to_keep)
        
        # Get updated stats
        new_stats = database.get_database_stats()
        
        return {
            "success": True,
            "data": {
                "deleted_records": deleted_count,
                "days_kept": days_to_keep,
                "updated_stats": new_stats
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== WEBSOCKET FOR REAL-TIME UPDATES =====

@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data updates"""
    # Optional API token check for WebSocket connections
    if API_TOKEN:
        provided = websocket.headers.get("x-api-key") or websocket.query_params.get("api_key")
        if provided != API_TOKEN:
            await websocket.close(code=1008)
            return
    await manager.connect(websocket)
    try:
        while True:
            # Get latest measurement
            latest = database.get_latest_measurements(1)
            if latest:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "measurement_update",
                        "data": latest[0],
                        "timestamp": datetime.now().isoformat()
                    }),
                    websocket
                )
            
            # Wait for 5 seconds before next update
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ===== HEALTH CHECK =====

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        stats = database.get_database_stats()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "total_measurements": stats.get('total_measurements', 0)
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )

@app.get("/api/sensors/connectivity")
async def check_sensors_connectivity():
    """Check real-time connectivity of all known sensors"""
    try:
        import serial
        from serial.tools import list_ports
        import sys
        import os
        
        # Add src directory to path to import PZEM004T
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
        from pzem import PZEM004T
        
        # Get all known sensors from database
        sensors = database.get_sensor_summary()
        
        # Get list of available serial ports
        available_ports = [port.device for port in list_ports.comports()]
        
        connectivity_status = []
        
        for sensor in sensors:
            port = sensor['port']
            status = {
                'port': port,
                'device_address': sensor['device_address'],
                'physically_connected': port in available_ports,
                'can_communicate': False,
                'last_measurement': sensor['last_measurement'],
                'error': None
            }
            
            # Only test communication if port is physically available
            if status['physically_connected']:
                try:
                    # Try to connect and read data
                    pzem = PZEM004T(port, sensor['device_address'], timeout=2.0)
                    measurements = pzem.read_measurements()
                    if measurements:
                        status['can_communicate'] = True
                    pzem.close()
                except Exception as e:
                    status['error'] = str(e)
                    status['can_communicate'] = False
            
            # Determine overall online status
            time_threshold = 60000  # 1 minute in milliseconds
            last_measurement_time = None
            if sensor['last_measurement']:
                try:
                    from datetime import datetime
                    last_measurement_time = datetime.fromisoformat(sensor['last_measurement'].replace('Z', '+00:00'))
                    time_since_last = (datetime.now() - last_measurement_time).total_seconds() * 1000
                    recent_data = time_since_last < time_threshold
                except:
                    recent_data = False
            else:
                recent_data = False
            
            status['is_online'] = status['physically_connected'] and status['can_communicate']
            status['has_recent_data'] = recent_data
            
            connectivity_status.append(status)
        
        return {
            "success": True,
            "data": connectivity_status,
            "available_ports": available_ports,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def monitor_usb_ports():
    """Background task to monitor USB port changes"""
    global _last_usb_status
    
    while True:
        try:
            import serial
            from serial.tools import list_ports
            import sys
            import os
            
            # Get current USB ports
            current_ports = [port.device for port in list_ports.comports() if 'USB' in port.device]
            
            # Get known sensors from database
            sensors = database.get_sensor_summary()
            known_ports = [sensor['port'] for sensor in sensors]
            
            # Check for changes
            current_status = {}
            changes_detected = False
            
            for port in known_ports:
                is_connected = port in current_ports
                current_status[port] = is_connected
                
                # Check if status changed
                if port not in _last_usb_status or _last_usb_status[port] != is_connected:
                    changes_detected = True
                    
                    # Broadcast change via WebSocket
                    message = {
                        "type": "usb_status_change",
                        "port": port,
                        "connected": is_connected,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast(json.dumps(message))
            
            # Update last known status
            _last_usb_status = current_status
            
            if changes_detected:
                # Also broadcast full connectivity status
                try:
                    connectivity_status = []
                    for sensor in sensors:
                        port = sensor['port']
                        status = {
                            'port': port,
                            'device_address': sensor['device_address'],
                            'physically_connected': port in current_ports,
                            'can_communicate': False,
                            'last_measurement': sensor['last_measurement'],
                            'error': None
                        }
                        
                        # Test communication if physically connected
                        if status['physically_connected']:
                            try:
                                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
                                from pzem import PZEM004T
                                
                                pzem = PZEM004T(port, sensor['device_address'], timeout=1.0)
                                measurements = pzem.read_measurements()
                                if measurements:
                                    status['can_communicate'] = True
                                pzem.close()
                            except Exception as e:
                                status['error'] = str(e)
                                status['can_communicate'] = False
                        
                        status['is_online'] = status['physically_connected'] and status['can_communicate']
                        connectivity_status.append(status)
                    
                    # Broadcast full update
                    full_update = {
                        "type": "connectivity_update",
                        "data": connectivity_status,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast(json.dumps(full_update))
                    
                except Exception as e:
                    print(f"Error in connectivity check: {e}")
            
        except Exception as e:
            print(f"Error in USB monitoring: {e}")
        
        # Check every 2 seconds
        await asyncio.sleep(2)

@app.delete("/api/measurements")
async def delete_all_measurements():
    """Delete all measurements but keep sensor records"""
    try:
        with sqlite3.connect(database.db_path) as conn:
            cursor = conn.cursor()
            
            # Count measurements before deletion
            cursor.execute('SELECT COUNT(*) FROM measurements')
            count_before = cursor.fetchone()[0]
            
            # Delete all measurements
            cursor.execute('DELETE FROM measurements')
            
            # Reset total_readings in sensors table
            cursor.execute('UPDATE sensors SET total_readings = 0')
            
            conn.commit()
            
        return {
            "success": True,
            "message": f"Đã xóa {count_before} measurements",
            "deleted_count": count_before
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xóa measurements: {str(e)}")

@app.delete("/api/database/reset")
async def reset_database(
    deep: bool = Query(False, description="Deep reset - recreate database file completely")
):
    """Reset entire database - delete all data"""
    try:
        if deep:
            # Deep reset: Delete and recreate entire database file
            import os
            
            # Count data before deletion
            with sqlite3.connect(database.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM measurements')
                measurement_count = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM sensors')
                sensor_count = cursor.fetchone()[0]
            
            # Delete the database file completely
            if os.path.exists(database.db_path):
                os.remove(database.db_path)
            
            # Recreate database with schema
            database._create_tables()
            
            return {
                "success": True,
                "message": f"Đã reset sâu toàn bộ database: {measurement_count} measurements và {sensor_count} sensors. File database đã được tạo mới.",
                "deleted_measurements": measurement_count,
                "deleted_sensors": sensor_count,
                "reset_type": "deep"
            }
        else:
            # Normal reset: Just delete data
            with sqlite3.connect(database.db_path) as conn:
                cursor = conn.cursor()
                
                # Count data before deletion
                cursor.execute('SELECT COUNT(*) FROM measurements')
                measurement_count = cursor.fetchone()[0]
                
                cursor.execute('SELECT COUNT(*) FROM sensors')
                sensor_count = cursor.fetchone()[0]
                
                # Delete all data
                cursor.execute('DELETE FROM measurements')
                cursor.execute('DELETE FROM sensors')
                
                # Reset autoincrement counters
                cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("measurements", "sensors")')
                
                conn.commit()
                
                # VACUUM to shrink database file size
                cursor.execute('VACUUM')
                
                conn.commit()
                
            return {
                "success": True,
                "message": f"Đã xóa toàn bộ database: {measurement_count} measurements và {sensor_count} sensors (Schema được giữ lại)",
                "deleted_measurements": measurement_count,
                "deleted_sensors": sensor_count,
                "reset_type": "normal"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi reset database: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the app starts"""
    global _monitoring_task
    _monitoring_task = asyncio.create_task(monitor_usb_ports())

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background tasks when the app shuts down"""
    global _monitoring_task
    if _monitoring_task:
        _monitoring_task.cancel()
        try:
            await _monitoring_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    import asyncio
    
    print("🔌 Starting PZEM-004T Web Monitoring Server...")
    print(f"📊 Database: {db_path}")
    print("🌐 Dashboard: http://localhost:8000")
    print("📡 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
