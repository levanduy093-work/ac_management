# 🔌 AC Management - PZEM-004T Power Monitoring System

**Hệ thống giám sát điện năng PZEM-004T hoàn chỉnh và chuyên nghiệp** với web dashboard hiện đại, REST API, database management và công cụ hỗ trợ toàn diện.

## 🎯 Tổng quan hệ thống

### 🏗️ Kiến trúc tổng thể
```
PZEM-004T Hardware → Serial (Modbus-RTU) → Python Library → SQLite Database → Web Dashboard & REST API
                                                                           ↓
                                                                    Mobile App Ready
```

### 🌟 Điểm nổi bật chính

- ✅ **🌐 Web Dashboard hiện đại** với realtime, biểu đồ tương tác, responsive
- ✅ **🔗 REST API đầy đủ** (kèm WebSocket) cho ứng dụng mobile và tích hợp
- ✅ **💾 SQLite Database** tối ưu, kèm công cụ quản trị và export
- ✅ **🔌 Thư viện PZEM-004T** theo datasheet chính thức (Modbus‑RTU)
- ✅ **🔧 Hỗ trợ đa cảm biến**, lựa chọn cảm biến theo cổng
- ✅ **🛡️ Safe tools** (reset năng lượng an toàn, không đổi địa chỉ)

### 📊 Thông số kỹ thuật giám sát

Hệ thống đọc và hiển thị các thông số điện quan trọng theo tài liệu kỹ thuật PZEM-004T:

| Thông số | Đơn vị | Dải đo | Độ phân giải | Độ chính xác | Ngưỡng bắt đầu |
|----------|---------|--------|--------------|--------------|----------------|
| **Voltage** | V | 80-260V | 0.1V | ±0.5% | - |
| **Current** | A | 0-10A (10A) / 0-100A (100A) | 0.001A | ±0.5% | 0.01A (10A) / 0.02A (100A) |
| **Power** | W | 0-2.3kW (10A) / 0-23kW (100A) | 0.1W | ±0.5% | 0.4W |
| **Energy** | kWh | 0-9999.99kWh | 1Wh | ±0.5% | - |
| **Frequency** | Hz | 45-65Hz | 0.1Hz | ±0.5% | - |
| **Power Factor** | - | 0.00-1.00 | 0.01 | ±1% | - |
| **Alarm** | ON/OFF | Power threshold | - | - | - |

## 🌐 Web Dashboard System (v2.2.0) ⭐

### 🎯 Main Dashboard (`http://localhost:8000/`)
- **📊 Live Monitoring Cards**: 
  - Total power consumption (tất cả sensors hoặc individual sensor)
  - Total energy accumulated với smart formatting
  - Average voltage monitoring với alerts
  - Active sensor count với connectivity status
- **📈 Interactive Charts (Chart.js)**:
  - Power consumption timeline với zoom/pan capabilities
  - Voltage & Current monitoring graphs  
  - Real-time updates every 5 seconds via WebSocket
  - Time series optimization cho performance
- **🔍 Advanced Filtering**:
  - Individual sensor selection trong dropdown
  - Date range filtering với auto-refresh controls
  - Smart data aggregation

### 📁 Export Center (`http://localhost:8000/export`)
- **📄 Multi-format Export**:
  - CSV với proper encoding cho Excel compatibility
  - JSON với metadata và structured format
- **🎛️ Advanced Filtering Engine**:
  - Individual sensor selection hoặc all sensors
  - Time range selection ("Tất cả thời gian" exports ALL data)
  - Smart filename generation với sensor port, timerange và timestamp
- **👁️ Data Preview**: Xem trước dữ liệu và thống kê chính xác tổng bản ghi
- **🚀 Intelligent Export**: 
  - No time filter = Export ALL database data
  - With time filter = Export data trong khoảng đó

### ⚙️ System Settings (`http://localhost:8000/settings`)
- **💚 Health Monitoring Dashboard**:
  - System status indicators
  - Database connectivity checks với real-time stats
  - Sensor connectivity monitoring
- **📊 Database Analytics**:
  - Total measurements và sensors count
  - Database file size với live updates
  - Storage utilization và performance metrics
- **🗑️ Management Tools**:
  - Delete all measurements với confirmation
  - Database reset với deep reset option (recreates file to 0.03MB minimum)
  - Auto-refresh statistics sau khi thực hiện operations

### 📱 API Documentation (`http://localhost:8000/docs`)
- **REST API** kèm Swagger UI
- **WebSocket realtime** `ws://localhost:8000/ws` và `ws://localhost:8000/ws/realtime`
- **📋 Comprehensive endpoints**:
  - `/api/dashboard` - Dashboard data với sensor filtering
  - `/api/measurements` - Measurements với pagination và filtering
  - `/api/export/csv`, `/api/export/json` - Export functionality
  - `/api/sensors` - Sensor management và connectivity
  - `/api/database/stats` - Database statistics và health
  - `/api/cleanup`, `/api/database/reset` - Maintenance operations

## 🗂️ Cấu trúc dự án

```
ac_management/
├── src/                       # Core libraries
│   ├── pzem.py               # PZEM-004T library (Modbus‑RTU)
│   └── database.py           # SQLite database helper
├── web/                       # Web dashboard (FastAPI)
│   ├── api.py                # REST + WebSocket server
│   ├── templates/            # dashboard.html, export.html, settings.html
│   └── static/               # CSS/JS
├── tools/                     # CLI/GUI utilities
│   ├── read_ac_sensor_db.py
│   ├── database_gui.py
│   ├── query_database.py
│   └── reset_energy_no_address_change.py
├── docs/                      # Additional documentation
├── data/
│   └── pzem_data.db          # SQLite database
├── run_web.py                 # Launcher script
├── Makefile                   # Common commands
└── requirements.txt          # Dependencies
```

## 🚀 Cài đặt và sử dụng

### Yêu cầu hệ thống
- **Python**: 3.9+
- **Dependencies**: fastapi, uvicorn, pyserial, websockets, tabulate, pandas, jinja2, aiofiles, python-multipart
- **OS**: Linux, macOS, Windows
- **Hardware**: PZEM-004T + USB-to-Serial adapter (PL2303, CH340, CP210, FTDI)

### Cài đặt nhanh
```bash
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt
```

## 🌐 Chạy Web Dashboard (Khuyến nghị)

### Cách nhanh nhất (2 phút setup)
```bash
# Chạy cả monitor + web (stack đầy đủ)
make run-server

# Access dashboard: http://localhost:8000
```

### Hoặc manual
```bash
# Chạy data collection (Terminal 1)
python tools/read_ac_sensor_db.py

# Chạy web server (Terminal 2)
python run_web.py
```

### Truy cập nhanh
- **Login**: http://localhost:8000/login
- **Dashboard**: http://localhost:8000
- **Export**: http://localhost:8000/export
- **Settings**: http://localhost:8000/settings
- **API Docs**: http://localhost:8000/docs (có thể tắt trong production)
- **WebSocket**: ws://localhost:8000/ws hoặc ws://localhost:8000/ws/realtime

## 💾 Database

### Current Database Schema
```sql
-- Sensors table
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    port TEXT UNIQUE NOT NULL,
    device_address INTEGER DEFAULT 248,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_readings INTEGER DEFAULT 0
);

-- Measurements table
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    voltage REAL, current REAL, power REAL, energy REAL,
    frequency REAL, power_factor REAL, alarm_status BOOLEAN,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id)
);
```

### Lệnh nhanh
```bash
make db-stats     # Thống kê
make db-gui       # GUI quản trị
make db-sensors   # Danh sách cảm biến
make db-latest    # Bản ghi mới nhất
make db-cleanup   # Dọn dữ liệu cũ
```

## 🔧 Standalone Tools

### 🎯 Main Monitoring Tool
```bash
# Database storage (khuyến nghị)
python tools/read_ac_sensor_db.py
# hoặc
make run-monitor-db
```

### 🛡️ Safe Energy Reset Tool
```bash
# AN TOÀN - Không thay đổi địa chỉ thiết bị
python tools/reset_energy_no_address_change.py
# hoặc
make run-reset

# Command line options
python tools/reset_energy_no_address_change.py --all          # Reset tất cả
python tools/reset_energy_no_address_change.py --port /dev/ttyUSB0  # Reset specific
```

**Lưu ý**: Tool này **KHÔNG thay đổi địa chỉ** PZEM, giữ nguyên 0xF8 để tránh xung đột.

### 📊 Database Query Tools
```bash
# CLI tool
python tools/query_database.py --stats
python tools/query_database.py --export-csv export.csv --days 7
python tools/query_database.py --export-json-separate --days 30

# GUI tool (khuyến nghị)
python tools/database_gui.py
```

## 🎯 Tính năng chính đã triển khai

### 🌐 Web Dashboard System
- ✅ **Modern responsive UI** với Bootstrap 5 và mobile compatibility
- ✅ **Real-time monitoring** với WebSocket updates mỗi 5 giây
- ✅ **Interactive charts** (Chart.js) + tuỳ chọn làm mượt (moving average) + LTTB decimation
- ✅ **Giữ ngữ cảnh cả ngày khi realtime**: biểu đồ luôn bám theo ngày đã lọc
- ✅ **Bảng dữ liệu**: mặc định 6 dòng, nút “Hiển thị thêm” (+6 mỗi lần)
- ✅ **Individual sensor selection** trong dashboard và export
- ✅ **Advanced export system** với multiple formats và filtering
- ✅ **System health monitoring** với database analytics
- ✅ **Auto-refresh statistics** sau các operations

### 🔌 Complete PZEM-004T Library
- ✅ **Full Modbus-RTU implementation** theo official datasheet
- ✅ **Complete API**: Read measurements, configure thresholds, reset energy, calibration
- ✅ **Smart caching** với 0.1s interval optimization
- ✅ **Error resilience**: CRC validation, timeout handling, retry mechanisms
- ✅ **Backward compatibility** với existing projects
- ✅ **Safety-focused operations** với comprehensive verification

### 💾 Database Management System  
- ✅ **Optimized SQLite storage** với indexes và foreign keys
- ✅ **Concurrent access support** với thread safety
- ✅ **Auto-cleanup** và maintenance functions
- ✅ **Rich statistics** và monitoring capabilities
- ✅ **Multiple export formats** với metadata
- ✅ **GUI và CLI tools** cho comprehensive management

### 🔧 Production-Ready Features
- ✅ **Dependency validation** và health checks trong launcher
- ✅ **Error handling** và graceful degradation
- ✅ **Background tasks** cho USB monitoring và connectivity
- ✅ **Comprehensive logging** và debugging support
- ✅ **Mobile-ready API** với CORS support

## 📱 Mobile Development Ready

### API Ecosystem
```bash
# Base URL
http://localhost:8000/api/

# Key endpoints
GET /api/dashboard?port=/dev/ttyUSB1                 # Dashboard data
GET /api/measurements?limit=50&port=...              # Measurements/filtering  
GET /api/measurements/range?start_date=...&end_date=...  # Theo ngày
GET /api/sensors                                     # Sensor list & status
GET /api/export/csv|json                              # Export
DELETE /api/cleanup                                   # Dọn dữ liệu
DELETE /api/database/reset?deep=false                 # Reset database
WS   /ws, /ws/realtime                                # Real-time
```

### Features cho Mobile Development
- ✅ **17+ REST endpoints** với consistent JSON responses
- ✅ **WebSocket real-time** communication
- ✅ **Cookie-based auth** (login tại `/login`, không dùng API key)
- ✅ **Auto-generated documentation** tại `/docs` (có thể tắt)
- ✅ **Error handling** với proper HTTP status codes
- ✅ **Data pagination** và filtering support
  
Lưu ý: Với ứng dụng mobile/web client khác origin, khuyến nghị sử dụng reverse proxy cùng domain (hoặc Cloudflare Tunnel) để chia sẻ cookie phiên an toàn.

## 🔧 Khắc phục sự cố

### Lỗi thường gặp

#### 1. "No PZEM devices detected"
```bash
# Kiểm tra USB devices
lsusb

# Kiểm tra serial ports
ls -la /dev/ttyUSB*

# Cài driver nếu cần
sudo apt-get install pl2303  # Ubuntu/Debian
```

#### 2. "Permission denied" trên /dev/ttyUSB*
```bash
# Cấp quyền tạm thời
sudo chmod 666 /dev/ttyUSB0

# Hoặc thêm user vào group dialout (khuyến nghị)
sudo usermod -a -G dialout $USER
# Logout và login lại
```

#### 3. Web server không start
```bash
# Kiểm tra dependencies
python run_web.py --skip-checks

# Kiểm tra port conflicts
lsof -i :8000

# Check database
ls -la data/pzem_data.db
```

#### 4. Database size không giảm sau reset
- ✅ **Đã fix**: Sử dụng `VACUUM` command để reclaim space
- ✅ **Minimum size**: 0.03MB (32KB) là kích thước tối thiểu của SQLite với schema
- ✅ **Deep reset**: Có thể recreate toàn bộ database file

## 📈 Roadmap & Development

### ✅ Version 2.3.0 (Current) - Security & Deployment
- [x] Session-based authentication (cookie HttpOnly) và trang `/login`
- [x] CSRF protection cho POST/DELETE/PUT/PATCH (`X-Requested-With` + Origin check)
- [x] Tắt `/docs` trong production qua `DISABLE_DOCS=true`
- [x] Hướng dẫn triển khai domain (Cloudflare Tunnel) và systemd stack (`acm.target`)

### 2.2.0 - Production Web Dashboard
- [x] Complete web dashboard với real-time monitoring
- [x] 17+ REST API endpoints hoàn chỉnh  
- [x] Advanced export system với filtering
- [x] Individual sensor selection feature
- [x] System health monitoring và analytics
- [x] Mobile-ready API với comprehensive documentation
- [x] Database optimization với auto-management

### 🚧 Đang phát triển
- [ ] **Authentication system** (JWT cho API security)
- [ ] **Data aggregation** (hourly/daily summaries)
- [ ] **Alert system** (email/SMS notifications)
- [ ] **Performance optimization** (caching, compression)

### 🔮 Kế hoạch tương lai
- [ ] **Mobile app** (React Native/Flutter) 
- [ ] **Cloud deployment** (Docker + Kubernetes)
- [ ] **PostgreSQL support** cho production scale
- [ ] **Machine learning** dự đoán consumption patterns
- [ ] **Multi-tenant system** cho nhiều location

## 📚 Tài liệu tham khảo

### 🌐 Web Dashboard & API
- **[WEB_DASHBOARD_GUIDE.md](WEB_DASHBOARD_GUIDE.md)**: Complete web dashboard guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Hướng dẫn đưa dự án lên domain (Cloudflare Tunnel hoặc Nginx/Caddy)
- **`http://localhost:8000/docs`**: Auto-generated Swagger UI (có thể tắt)

### 📖 Core System Documentation  
- **[docs/PZEM004T.md](docs/PZEM004T.md)**: Library API reference (570+ dòng)
- **[docs/DATABASE.md](docs/DATABASE.md)**: Database management guide (420+ dòng)
- **[docs/DATA_LOGGING.md](docs/DATA_LOGGING.md)**: Data logging và export (230+ dòng)

### 🏗️ Project Structure
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**: Detailed structure (340+ dòng)
- **[CHANGELOG.md](CHANGELOG.md)**: Version history và features (190+ dòng)

## 📊 Project Statistics

```
📋 Code Statistics:
- Python Code: 3,482 lines
- Documentation: 3,000+ lines  
- Web Templates: HTML/CSS/JS
- Total API Endpoints: 17+
- Database Tables: 2 (sensors, measurements)
- Supported Adapters: PL2303, CH340, CP210, FTDI
```

## 🎉 Quick Start Guide

### 🚀 2-Minute Setup
```bash
# 1. Clone và install
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt

# 2. Start monitoring (Terminal 1)
make run-monitor-db

# 3. Start web dashboard (Terminal 2)
make run-web

# 4. Access: http://localhost:8000
```

### 📱 For Mobile Developers
```bash
# Start system
make run-monitor-db && make run-web

# API Documentation: http://localhost:8000/docs
# WebSocket: ws://localhost:8000/ws
# Base API: http://localhost:8000/api/
```

---

## 📄 License

Dự án này được phân phối dưới **giấy phép MIT**. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 🤝 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! 

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📞 Liên hệ

- **GitHub**: [levanduy093-work](https://github.com/levanduy093-work)
- **Email**: levanduy.work@gmail.com

---

**🏆 AC Management v2.2.0** - Production-ready PZEM-004T monitoring system với comprehensive web dashboard, mobile-ready API, và advanced database management. Designed for **reliability**, **scalability**, và **ease of use**.