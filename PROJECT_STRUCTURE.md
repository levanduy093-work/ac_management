# 🏗️ Cấu trúc dự án AC Management

## 🎯 Tổng quan

AC Management là **hệ thống giám sát điện năng PZEM-004T hoàn chỉnh** với web dashboard hiện đại, REST API, database management và tools hỗ trợ. Hệ thống được thiết kế theo kiến trúc modular với focus vào reliability, scalability và ease of use.

## 🗂️ Cấu trúc thư mục

```
ac_management/
├── src/                       # 📚 Core Libraries
│   ├── __init__.py           # Package initialization
│   ├── pzem.py               # PZEM-004T library (Modbus‑RTU)
│   └── database.py           # SQLite database module
├── web/                       # 🌐 Web Dashboard System
│   ├── api.py                # FastAPI server (REST + WebSocket)
│   ├── static/               # CSS, JS, assets
│   ├── templates/            # HTML templates
│   │   ├── login.html        # Login page (session-based auth)
│   │   ├── dashboard.html    # Main dashboard
│   │   ├── export.html       # Data export page
│   │   └── settings.html     # System settings
│   └── README.md             # Web documentation
├── tools/                     # 🔧 Application Tools
│   ├── __init__.py           # Package initialization
│   ├── read_ac_sensor_db.py  # Database monitoring (243 dòng)
│   ├── database_gui.py       # Interactive GUI tool (618 dòng)
│   ├── query_database.py     # Database query tool (403 dòng)
│   ├── reset_energy_no_address_change.py # Safe energy reset (299 dòng)
│   └── read_ac_sensor.py     # Legacy CSV monitoring (compatible)
├── docs/                      # 📋 Documentation
│   ├── PZEM004T.md           # Library API reference (572 dòng)
│   ├── DATABASE.md           # Database guide (389 dòng)
│   └── DATA_LOGGING.md       # Data logging guide (231 dòng)
├── data/                      # 📊 Data Storage
│   ├── pzem_data.db          # Main SQLite database
│   ├── csv_logs/             # CSV export files
│   └── json_log/             # JSON export files
├── run_web.py                 # 🚀 Web server launcher (116 dòng)
├── Makefile                   # 🛠️ Project management (130 dòng)
├── requirements.txt           # 📦 Dependencies (9 packages)
├── CHANGELOG.md              # 📝 Version history
├── LICENSE                   # 📄 MIT License
├── README.md                 # 📖 Main documentation
├── PROJECT_STRUCTURE.md      # 📋 This file
└── WEB_DASHBOARD_GUIDE.md    # 🌐 Web dashboard guide (398 dòng)
```

## 📋 Mô tả chi tiết từng module

### 📚 Core Libraries (`src/`)

#### `src/pzem.py` (709 dòng) - PZEM-004T Library ⭐
- **Complete Modbus-RTU implementation** theo datasheet chính thức
- **Full API support**: đọc dữ liệu, cấu hình, reset, calibration
- **Smart caching**: Tối ưu hiệu suất với 0.1s interval
- **Error handling**: CRC validation, timeout, retry mechanism
- **Backward compatibility**: Hỗ trợ tên class cũ `PZEM004Tv30`
- **Safety focus**: Verified operations và comprehensive logging

#### `src/database.py` (367 dòng) - Database Management
- **SQLite database manager** với 2 bảng: `sensors` và `measurements`
- **Automatic optimization**: Indexes, foreign keys, cleanup
- **Rich API**: Statistics, queries, export functionality
- **Thread-safe operations** cho concurrent access
- **Data integrity**: Validation và error handling

### 🌐 Web Dashboard System (`web/`) - NEW ⭐

#### `web/api.py` - FastAPI Server
- **Modern REST API** với FastAPI framework
- **Real-time WebSocket** cho live updates
- **Comprehensive endpoints**: 
  - Dashboard data aggregation
  - Sensor management và statistics
  - Export functionality (CSV/JSON)
  - System health monitoring
- **Mobile-ready**: CORS support, proper response formats
- **Background tasks**: USB monitoring, real-time updates
- **Security**: Session-based auth (cookie HttpOnly), CSRF header + Origin check, input validation

#### `web/templates/` - HTML Templates
- **`dashboard.html`**: Main monitoring interface với Chart.js
- **`export.html`**: Advanced export với filtering options
- **`settings.html`**: System management và configuration
- **Responsive design**: Bootstrap 5, mobile-friendly
- **Interactive features**: Real-time charts, WebSocket integration

#### `web/static/` - Frontend Assets
- **CSS styling**: Custom themes, responsive layouts
- **JavaScript**: Chart.js integration, WebSocket handling
- **Assets**: Icons, images, fonts

### 🔧 Application Tools (`tools/`)

#### `tools/read_ac_sensor_db.py` - Main Monitoring ⭐
- **Primary monitoring tool** cho database storage
- **Multi-sensor concurrent reading** với threading
- **Auto-discovery**: Tìm và kết nối PZEM-004T tự động
- **Real-time display**: Table format với total power/energy
- **Database integration**: Lưu trữ hiệu quả vào SQLite
- **Error resilience**: Retry mechanism, timeout handling
- **Adapter support**: PL2303, CH340, CP210, FTDI

#### `tools/database_gui.py` - GUI Management ⭐
- **Interactive GUI tool** cho database management
- **Menu-driven interface**: Không cần nhớ commands
- **Complete functionality**:
  - Database statistics và sensor summary
  - Export data (CSV/JSON) với overwrite options
  - Advanced queries (by port, date range, statistics)
  - Cleanup old data với confirmation
- **User-friendly**: Perfect cho non-technical users

#### `tools/query_database.py` - CLI Power Tool
- **Command-line database interface** cho advanced users
- **Flexible export options**:
  - Single file export hoặc separate by port
  - CSV và JSON formats
  - Date filtering, port filtering, record limits
  - Overwrite control hoặc timestamp files
- **Statistics display**: Database stats, sensor summary
- **Cleanup functions**: Automated old data removal

#### `tools/reset_energy_no_address_change.py` - Safety Tool ⭐
- **SAFE energy reset tool** - KHÔNG thay đổi địa chỉ thiết bị
- **Sequential reset**: Tránh conflicts khi có nhiều devices
- **Smart timeout**: Retry mechanism với conflict detection  
- **Address preservation**: Giữ nguyên default address (0xF8)
- **Interactive menu**: User-friendly với confirmations
- **Conflict resolution**: Handles multiple devices cùng địa chỉ

#### `tools/read_ac_sensor.py` (362 dòng) - Legacy CSV Tool
- **Original CSV-based monitoring** (maintained for compatibility)
- **CSV file per sensor** với timestamp management
- **Threading support** cho multiple sensors
- **File size management** với auto-cleanup
- **Similar features** như database version nhưng CSV output

### 📋 Documentation (`docs/`)

#### `docs/PZEM004T.md` (572 dòng) - Library Reference
- **Complete API documentation** cho PZEM-004T library
- **Technical specifications** theo official datasheet
- **Hardware connection guide** với wiring diagrams
- **Usage examples** từ basic đến advanced
- **Troubleshooting guide** cho common issues

#### `docs/DATABASE.md` (389 dòng) - Database Guide  
- **SQLite database management** comprehensive guide
- **Schema documentation**: tables, indexes, relationships
- **Tool usage**: GUI, CLI, migration
- **Performance optimization** và maintenance
- **Backup và recovery** procedures

#### `docs/DATA_LOGGING.md` (231 dòng) - Data Management
- **Data logging strategies**: CSV vs Database
- **Export functionality** và formats
- **Data analysis examples** với pandas
- **Cleanup và maintenance** best practices

### 🚀 Web Server Launcher

#### `run_web.py` (116 dòng) - FastAPI Launcher ⭐
- **Intelligent web server launcher** với comprehensive checks
- **Dependency validation**: Kiểm tra required packages
- **Database verification**: Ensures data availability
- **Configuration options**: Host, port, reload, skip-checks
- **User-friendly output**: Status messages và helpful URLs
- **Error handling**: Graceful degradation và helpful messages

### 🛠️ Project Management

#### `Makefile` (130 dòng) - Development Workflow ⭐
- **Complete project automation** với 25+ commands
- **Quick start**: `make run-server` (stack) hoặc `make run-monitor-db`, `make run-web`
- **Database operations**: stats, cleanup, migration
- **Development tools**: lint, format, test
- **Documentation**: `make docs`
- **Installation**: `make install`, `make install-dev`

#### `requirements.txt` (9 packages) - Dependencies
- **Core dependencies**:
  - `fastapi`, `uvicorn`: Web server framework
  - `pyserial`: PZEM communication
  - `tabulate`, `pandas`: Data processing
  - `websockets`: Real-time communication
  - `jinja2`, `aiofiles`: Web templating
  - `python-dotenv`: Load environment from `.env`
  - `itsdangerous`: Signed session token helper

### 📊 Data Storage (`data/`)

#### `data/pzem_data.db` - Main Database ⭐
- **Primary SQLite database** cho production data
- **Schema optimized**: 2 tables với proper relationships
- **Performance indexes**: Fast queries on timestamp và sensor_id
- **Auto-management**: Self-cleanup, statistics tracking
- **Backup-friendly**: Single file cho easy backup

#### `data/csv_logs/` - CSV Exports
- **Export destination** cho CSV files
- **Naming convention**: `pzem_{port_name}.csv` hoặc `export.csv`
- **Column structure**: datetime, port, voltage_v, current_a, power_w, energy_wh, frequency_hz, power_factor, alarm_status
- **Legacy compatibility**: Supports old CSV workflow

#### `data/json_log/` - JSON Exports  
- **Export destination** cho JSON files
- **Format**: UTF-8 encoded với proper indentation
- **Metadata included**: Export timestamp, record count
- **API compatible**: Ready for mobile app consumption

### 📚 Project Documentation

#### `README.md` - Main Documentation ⭐
- **Project overview** và quick start guide
- **Web dashboard features** và screenshots
- **Installation instructions** và requirements
- **Usage examples** cho tất cả major features
- **Architecture overview** và development roadmap
- **Deployment links**: `DEPLOYMENT.md`, `WEB_ENV_SETUP.md`

#### `PROJECT_STRUCTURE.md` - This File
- **Complete project structure** documentation
- **Module descriptions** với technical details
- **Development guidelines** và architecture notes
- **File purposes** và relationships

#### `WEB_DASHBOARD_GUIDE.md` (398 dòng) - Web Guide ⭐
- **Comprehensive web dashboard** documentation
- **Feature overview**: Dashboard, export, settings
- **API documentation** cho mobile development
- **Deployment instructions** và configuration
- **Troubleshooting guide** và performance tips

#### `CHANGELOG.md` - Version History
- **Detailed version history** với semantic versioning
- **Feature additions** và improvements
- **Bug fixes** và breaking changes
- **Migration guides** between versions

#### `LICENSE` - MIT License
- **Open source license** cho commercial và personal use
- **Attribution requirements** và disclaimer

## 🌟 Key Features Implemented

### 🌐 Web Dashboard System (v2.1.0+) ⭐
- **Modern web interface** với real-time monitoring
- **Interactive charts** sử dụng Chart.js
- **REST API endpoints** cho mobile integration
- **WebSocket real-time** updates mỗi 5 giây
- **Responsive design** compatible với mobile/desktop
- **Advanced export** với filtering và format options
- **System management** với health monitoring

### 🔌 Complete PZEM-004T Library
- **Full Modbus-RTU implementation** theo official datasheet
- **Complete API**: Read, configure, reset, calibration
- **Smart caching** với 0.1s interval optimization
- **Error resilience**: CRC validation, retry mechanisms
- **Backward compatibility** với existing projects
- **Safety-focused operations** với verification

### 💾 Database Management System
- **SQLite storage** với optimized schema
- **Concurrent access** support với thread safety
- **Auto-cleanup** và maintenance functions
- **Rich statistics** và monitoring capabilities
- **Export functionality** với multiple formats
- **GUI và CLI tools** cho management

### 🔧 Safety-First Tools
- **Energy reset tool** không thay đổi address
- **Multi-device support** với conflict resolution
- **Interactive menus** với confirmations
- **Error recovery** và retry mechanisms

## 🚀 Quick Usage Guide

### 🌐 Web Dashboard (Recommended)
```bash
# Start data collection (Terminal 1)
make run-monitor-db

# Start web dashboard (Terminal 2)  
make run-web

# Access: http://localhost:8000
```

### 🔧 Standalone Tools
```bash
# Database monitoring
make run-monitor-db

# GUI database management
make db-gui

# Energy reset (safe)
make run-reset

# Database statistics
make db-stats
```

### 📱 API Development
```bash
# API documentation
http://localhost:8000/docs

# WebSocket real-time
ws://localhost:8000/ws/realtime

# REST endpoints
http://localhost:8000/api/measurements
```

## 🏗️ Development & Architecture

### System Architecture
```
Hardware (PZEM-004T) → Serial → Library → Database → Web/API → Frontend
```

### Design Principles
- **Modular architecture**: Tách biệt concerns
- **Safety first**: Không làm hỏng configuration
- **User-friendly**: GUI tools cho non-technical users  
- **Production-ready**: Error handling, logging, monitoring
- **Mobile-ready**: API design cho mobile integration

### Technology Stack
- **Backend**: Python 3.9+, FastAPI, SQLite
- **Frontend**: Bootstrap 5, Chart.js, WebSocket
- **Communication**: Modbus-RTU, pyserial
- **Data**: SQLite, CSV, JSON export

## 📄 License & Contributing

**MIT License** - Free for commercial và personal use. See [LICENSE](LICENSE) for details.

**Contributing**: Fork → Feature branch → Test → Pull Request

---

**AC Management v2.1.0+** - Production-ready PZEM-004T monitoring system với web dashboard, database management, và comprehensive tooling. 