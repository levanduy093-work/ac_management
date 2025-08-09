# Changelog

Tất cả các thay đổi quan trọng trong dự án này sẽ được ghi lại trong file này.

## [2.2.0] - 2025-08-09 (Current)

### 🌐 Web Dashboard & Production Release

#### ✨ Major Features Added
- **🌐 Complete Web Dashboard System** với modern UI
  - Real-time monitoring với interactive charts (Chart.js)
  - Advanced export center với filtering options
  - System management với health monitoring
  - Mobile-responsive design với Bootstrap 5
- **🔗 Comprehensive REST API** cho mobile integration
  - REST endpoints + WebSocket (`/ws`, `/ws/realtime`)
  - Realtime 5 giây, biểu đồ giữ ngữ cảnh cả ngày
  - Auto-generated documentation với Swagger UI
  - CORS support cho mobile development
- **🚀 Production-Ready Deployment**
  - `run_web.py` launcher với health checks
  - Dependency validation và database verification
  - Error handling và graceful degradation
- **📱 Mobile Development Ready**
  - Complete API ecosystem
  - WebSocket real-time communication
  - JSON responses với consistent error handling

#### 🌟 Web Dashboard Features
- **Dashboard (`/`)**: Live monitoring cards, interactive charts, data filtering
- **Export (`/export`)**: Multi-format export, batch operations, preview functionality  
- **Settings (`/settings`)**: System health, database analytics, sensor management
- **API Documentation (`/docs`)**: Auto-generated Swagger UI

#### 🔧 Enhanced Tools
- **FastAPI server** (`web/api.py`) REST + WebSocket
- **Background tasks**: USB monitoring, connectivity checking
- **Advanced export**: CSV/JSON với metadata và filtering
- **System integration**: Web dashboard thay thế GUI tools hoàn toàn

#### 📋 Technical Specifications
- **Frontend**: Bootstrap 5, Chart.js, WebSocket client
- **Backend**: FastAPI, uvicorn, SQLite với optimized indexes
- **Architecture**: RESTful API + WebSocket real-time + responsive UI
- **Dependencies**: 9 packages (fastapi, uvicorn, pyserial, websockets, etc.)
- **Performance**: Real-time updates, optimized queries, background processing

#### 🔄 Changed & Enhanced
- **Updated requirements.txt** (4 → 9 packages) với web dependencies
- **Enhanced Makefile** (130 dòng) với web server commands
- **Improved project structure** với web/ directory
- **Updated documentation** với web dashboard guide (398 dòng)
- **Updated docs** (README, WEB_DASHBOARD_GUIDE, web/README, PROJECT_STRUCTURE)

#### 🚨 Breaking Changes
- **Recommended workflow** changed: Web dashboard now primary interface
- **Port 8000** required cho web server (configurable)
- **New dependencies** required cho web functionality
- **Database-first approach**: CSV storage considered legacy

#### 🏆 Production Benefits
- **🎯 Single interface**: Web dashboard thay thế multiple CLI tools
- **📱 Mobile ready**: Complete API cho mobile app development
- **🔧 Maintenance friendly**: Built-in health monitoring và cleanup
- **📈 Scalable**: FastAPI async foundation cho high concurrency
- **🔒 Enterprise ready**: Input validation, error handling, security

## [2.1.0] - 2025-08-06

### 🎉 Database & GUI Enhancement Release

#### ✨ Added
- **Database storage system** với SQLite database thay thế CSV
- **Database module** (`src/database.py`) với API đầy đủ cho quản lý dữ liệu
- **Database monitoring script** (`tools/read_ac_sensor_db.py`) cho hiệu suất tốt hơn
- **Database query tool** (`tools/query_database.py`) với nhiều tùy chọn export
- **GUI tool tương tác** (`tools/database_gui.py`) với menu-driven interface
- **Export functionality** hỗ trợ CSV và JSON với overwrite options
- **Database statistics** và sensor summary tracking
- **Automatic cleanup** dữ liệu cũ trong database
- **Makefile commands** cho database operations

#### 🔄 Changed
- **Cập nhật Makefile** (84 → 121 dòng) với database commands
- **Cải thiện error handling** trong database operations
- **Tối ưu export performance** với overwrite options
- **GUI interface** thay thế command line cho database management
- **Documentation updates** cho database features

#### 🐛 Fixed
- **Datatype mismatch** trong export functions
- **NULL value handling** trong database queries
- **Import path issues** trong GUI tool
- **File overwrite logic** trong export tools

#### 📚 Documentation
- **docs/DATABASE.md** - Hướng dẫn database storage (389 dòng)
- **README.md** - Cập nhật với database features (318 dòng)
- **PROJECT_STRUCTURE.md** - Cập nhật cấu trúc dự án (256 dòng)
- **docs/DATA_LOGGING.md** - Thêm database storage guide

#### 🔧 Database Features
- **SQLite database** với 2 bảng: `sensors` và `measurements`
- **Automatic indexing** cho hiệu suất truy vấn tốt
- **Foreign key relationships** giữa sensors và measurements
- **Timestamp tracking** cho first_seen và last_seen
- **Sensor management** với device address tracking

#### 🖥️ GUI Features
- **Menu-driven interface** không cần nhớ command line
- **Database statistics** với real-time updates
- **Export options** với overwrite controls
- **Advanced queries** cho data analysis
- **Cleanup tools** với confirmation dialogs

#### 📊 Export Features
- **Single file export** cho tất cả dữ liệu
- **Separate files by port** cho từng cảm biến
- **CSV and JSON formats** với proper encoding
- **Overwrite options** (mặc định) hoặc timestamp files
- **Filter by date range** và port selection

## [2.0.0] - 2025-08-05

### 🎉 Major Release - Complete Library Rewrite

#### ✨ Added
- **Thư viện PZEM-004T hoàn chỉnh** với triển khai đầy đủ Modbus-RTU protocol
- **API đầy đủ** hỗ trợ tất cả function codes và register mapping
- **Xử lý lỗi toàn diện** với CRC validation, error handling, retry mechanism
- **Cache thông minh** để tối ưu hiệu suất (0.1s interval)
- **Tương thích ngược** với tên class cũ `PZEM004Tv30`
- **Tính năng verify reset** để kiểm tra reset thật
- **Cấu trúc dự án chuyên nghiệp** với thư mục src/, tools/, docs/
- **Makefile** để quản lý dự án (84 dòng)
- **Documentation chi tiết** trong docs/ (572 + 114 dòng)
- **Thông số kỹ thuật chính xác** theo tài liệu PZEM-004T datasheet
- **Quy tắc hiển thị** tuân thủ datasheet cho công suất và năng lượng
- **Phương thức format_measurements()** để format dữ liệu theo datasheet
- **Quản lý file size** tự động dọn dẹp file CSV khi quá lớn

#### 🔄 Changed
- **Cải thiện reset energy** với approach đơn giản hơn, tương thích với nhiều thiết bị
- **Cập nhật read_ac_sensor.py** sử dụng thư viện mới với hiệu suất tốt hơn (362 dòng)
- **Tổ chức lại cấu trúc file** theo chuẩn Python package
- **Cập nhật thông số kỹ thuật** theo datasheet chính thức PZEM-004T
- **Cải thiện hiển thị dữ liệu** theo quy tắc datasheet
- **Hỗ trợ adapter mở rộng** thêm CP210, FTDI ngoài PL2303, CH340

#### 🐛 Fixed
- **Lỗi reset energy** với thiết bị không gửi response
- **Timing issues** trong serial communication
- **Import paths** sau khi tổ chức lại cấu trúc
- **Error handling** trong multi-sensor monitoring

#### 📚 Documentation
- **docs/PZEM004T.md** - Hướng dẫn chi tiết thư viện (572 dòng)
- **README.md** - Cập nhật với cấu trúc mới và thông số kỹ thuật chính xác (467 dòng)
- **docs/DATA_LOGGING.md** - Hướng dẫn CSV logging (114 dòng)
- **PROJECT_STRUCTURE.md** - Tài liệu cấu trúc dự án chi tiết (248 dòng)

#### 🔧 Technical Specifications Update
- **Voltage**: 80-260V, resolution 0.1V, accuracy ±0.5%
- **Current**: 0-10A (10A model) / 0-100A (100A model), resolution 0.001A, accuracy ±0.5%
- **Power**: 0-2.3kW (10A) / 0-23kW (100A), resolution 0.1W, accuracy ±0.5%
- **Energy**: 0-9999.99kWh, resolution 1Wh, accuracy ±0.5%
- **Frequency**: 45-65Hz, resolution 0.1Hz, accuracy ±0.5%
- **Power Factor**: 0.00-1.00, resolution 0.01, accuracy ±1%
- **Starting thresholds**: Current 0.01A/0.02A, Power 0.4W
- **Display rules**: Power <1000W shows decimal, ≥1000W shows integer; Energy <10kWh shows Wh, ≥10kWh shows kWh

#### 📊 Data Management
- **CSV logging system** với cấu trúc chuẩn và timestamp chính xác
- **File size management** tự động dọn dẹp khi vượt quá kích thước
- **Multi-sensor support** với threading và error handling
- **Real-time monitoring** với cache optimization

## [1.0.0] - 2025-08-04

### 🎉 Initial Release

#### ✨ Added
- **Thư viện PZEM-004T cơ bản** với các chức năng đọc dữ liệu
- **Ứng dụng giám sát đa cảm biến** với CSV logging
- **Tool reset energy** cơ bản
- **Documentation** và examples

#### 🔧 Features
- Đọc voltage, current, power, energy, frequency, power factor
- Ghi dữ liệu CSV với timestamp
- Hiển thị dạng bảng cho nhiều cảm biến
- Reset energy counter
- Hỗ trợ nhiều loại USB-to-Serial adapter

---

## Format

Dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
và dự án này tuân theo [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Categories
- **Added** - Tính năng mới
- **Changed** - Thay đổi trong tính năng hiện có
- **Deprecated** - Tính năng sẽ bị loại bỏ
- **Removed** - Tính năng đã bị loại bỏ
- **Fixed** - Sửa lỗi
- **Security** - Cải thiện bảo mật 

### Error Need To Fix
- **Reset** - Nếu mà có nhiều cổng USB được cắm vào con rasp thì không thể reset được chính xác phần energy, nhưng nếu tôi tháo hết các cổng kết nối thừa ra thì nó lại có thể reset được con pzem tôi mong muốn, cần fix lại trường hợp lỗi này.

### Fixed Issues
- **Reset Energy với nhiều thiết bị** - Đã fix lỗi reset energy khi có nhiều cổng USB PZEM được kết nối:
  - **Tạo tool mới `reset_energy_no_address_change.py`** - Giải pháp KHÔNG thay đổi địa chỉ PZEM:
    - Reset tuần tự từng thiết bị để tránh xung đột
    - Sử dụng timeout ngắn và retry mechanism
    - Giữ nguyên địa chỉ mặc định của tất cả thiết bị