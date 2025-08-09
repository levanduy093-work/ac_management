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

- ✅ **🌐 Web Dashboard hiện đại** với real-time monitoring, interactive charts và mobile-ready UI
- ✅ **🔗 REST API hoàn chỉnh** với 17+ endpoints cho mobile integration và auto-generated docs  
- ✅ **💾 SQLite Database** với hiệu suất cao, auto-management và comprehensive analytics
- ✅ **🔌 PZEM-004T Library hoàn chỉnh** theo datasheet chính thức với Modbus-RTU protocol
- ✅ **🔧 Multi-sensor support** với concurrent monitoring và individual sensor selection
- ✅ **🛡️ Safety-first tools** không làm hỏng cấu hình thiết bị
- ✅ **📚 Comprehensive documentation** bằng tiếng Việt (3,000+ dòng docs)

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
- **👁️ Data Preview**: Live preview với sample data và statistics
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
- **🔗 17+ REST API endpoints** với Swagger UI
- **🔄 WebSocket real-time** updates tại `ws://localhost:8000/ws`
- **📋 Comprehensive endpoints**:
  - `/api/dashboard` - Dashboard data với sensor filtering
  - `/api/measurements` - Measurements với pagination và filtering
  - `/api/export/csv`, `/api/export/json` - Export functionality
  - `/api/sensors` - Sensor management và connectivity
  - `/api/database/stats` - Database statistics và health
  - `/api/cleanup`, `/api/database/reset` - Maintenance operations

## 🗂️ Cấu trúc dự án (3,482 dòng code)

```
ac_management/
├── src/                          # 📚 Core Libraries (1,074 dòng)
│   ├── pzem.py                  # Complete PZEM-004T library (708 dòng)
│   └── database.py              # SQLite database module (366 dòng)
├── web/                          # 🌐 Web Dashboard System (843+ dòng)
│   ├── api.py                   # FastAPI server với 17+ endpoints (843 dòng)
│   ├── templates/               # HTML Templates
│   │   ├── dashboard.html       # Real-time monitoring interface
│   │   ├── export.html          # Advanced export với filtering
│   │   └── settings.html        # System management và analytics
│   └── static/                  # CSS, JS, assets
├── tools/                        # 🔧 Application Tools (1,565 dòng)
│   ├── read_ac_sensor_db.py     # Main monitoring tool (242 dòng)
│   ├── database_gui.py          # Interactive GUI tool (617 dòng)
│   ├── query_database.py        # Database query CLI tool (402 dòng)
│   └── reset_energy_no_address_change.py # Safe energy reset (298 dòng)
├── docs/                         # 📋 Documentation (3,000+ dòng)
│   ├── PZEM004T.md              # Library API reference
│   ├── DATABASE.md              # Database management guide
│   └── DATA_LOGGING.md          # Data logging guide
├── data/                         # 📊 Data Storage
│   ├── pzem_data.db             # Main SQLite database
│   ├── csv_logs/                # CSV export files
│   └── json_log/                # JSON export files
├── run_web.py                    # 🚀 Web server launcher với health checks
├── Makefile                      # 🛠️ Project automation (25+ commands)
├── requirements.txt              # 📦 Dependencies (9 packages)
└── README.md                     # 📖 Main documentation
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
# Terminal 1: Start data collection
make run-monitor-db

# Terminal 2: Start web dashboard  
make run-web

# Access dashboard: http://localhost:8000
```

### Hoặc manual
```bash
# Chạy data collection (Terminal 1)
python tools/read_ac_sensor_db.py

# Chạy web server (Terminal 2)
python run_web.py
```

### Truy cập các tính năng
- **🎯 Dashboard**: http://localhost:8000 - Real-time monitoring với charts
- **📁 Export Data**: http://localhost:8000/export - Advanced export với filtering
- **⚙️ Settings**: http://localhost:8000/settings - System management
- **📋 API Docs**: http://localhost:8000/docs - Swagger UI cho mobile development
- **🔄 WebSocket**: ws://localhost:8000/ws - Real-time updates

## 💾 Database Management

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

### Quick Database Operations
```bash
# Database statistics
make db-stats

# Interactive GUI management
make db-gui

# View sensors
make db-sensors

# View latest measurements
make db-latest

# Cleanup old data
make db-cleanup
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

**💡 Lưu ý quan trọng**: Tool này **KHÔNG thay đổi địa chỉ** PZEM, giữ nguyên 0xF8 để tránh conflicts.

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
- ✅ **Interactive charts** sử dụng Chart.js với zoom/pan
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
GET /api/dashboard?port=/dev/ttyUSB1          # Dashboard data
GET /api/measurements?limit=50&port=...       # Measurements với filtering  
GET /api/sensors                              # Sensor list và status
GET /api/export/csv?port=...                 # Export functionality
WebSocket ws://localhost:8000/ws              # Real-time updates
```

### Features cho Mobile Development
- ✅ **17+ REST endpoints** với consistent JSON responses
- ✅ **WebSocket real-time** communication
- ✅ **CORS support** cho cross-origin requests
- ✅ **Auto-generated documentation** tại `/docs`
- ✅ **Error handling** với proper HTTP status codes
- ✅ **Data pagination** và filtering support

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

### ✅ Version 2.2.0 (Current) - Production Ready
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
- **[WEB_DASHBOARD_GUIDE.md](WEB_DASHBOARD_GUIDE.md)**: Complete web dashboard guide (470+ dòng)
- **[web/README.md](web/README.md)**: API documentation và deployment
- **`http://localhost:8000/docs`**: Auto-generated Swagger UI

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