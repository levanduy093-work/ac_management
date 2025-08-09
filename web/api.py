#!/usr/bin/env python3
"""
FastAPI Web Server for PZEM-004T Data Monitoring
Provides REST API endpoints and web dashboard for data visualization
"""

import sys
import os
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
import csv
import tempfile
from pathlib import Path

# FastAPI imports
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import PZEMDatabase

# Initialize FastAPI app
app = FastAPI(
    title="PZEM-004T Monitoring API",
    description="REST API for PZEM-004T power monitoring data",
    version="1.0.0"
)

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
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/export", response_class=HTMLResponse)
async def export_page(request: Request):
    """Data export page"""
    return templates.TemplateResponse("export.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings and management page"""
    return templates.TemplateResponse("settings.html", {"request": request})

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
async def get_dashboard_data():
    """Get comprehensive dashboard data"""
    try:
        # Get all dashboard data in one call
        stats = database.get_database_stats()
        sensors = database.get_sensor_summary()
        latest_measurements = database.get_latest_measurements(50)
        
        # Calculate summary statistics
        total_power = sum(m['power'] for m in latest_measurements if m['power'])
        total_energy = sum(m['energy'] for m in latest_measurements if m['energy'])
        avg_voltage = sum(m['voltage'] for m in latest_measurements if m['voltage']) / len(latest_measurements) if latest_measurements else 0
        
        # Get last 24 hours data for charts
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
                    "sensor_count": len(sensors)
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
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pzem_data_{timestamp}.csv"
        
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
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pzem_data_{timestamp}.json"
        
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
