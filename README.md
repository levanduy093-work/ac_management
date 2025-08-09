# 🔌 AC Management - PZEM-004T Power Monitoring System

Hệ thống giám sát điện năng PZEM-004T hoàn chỉnh và chuyên nghiệp với thư viện Python đầy đủ, web dashboard hiện đại, database management và các công cụ hỗ trợ toàn diện.

## 🎯 Tổng quan hệ thống

Đây là một **hệ thống giám sát điện năng hoàn chỉnh** bao gồm:

### 🏗️ Kiến trúc tổng thể
```
PZEM-004T Hardware → Python Library → Database → Web Dashboard & API
                                   ↓
                              Tools & Utilities
```

### 🌟 Điểm nổi bật chính

- ✅ **Web Dashboard hiện đại** với real-time monitoring và interactive charts
- ✅ **REST API hoàn chỉnh** cho mobile app integration
- ✅ **Database SQLite** với hiệu suất cao và auto-management
- ✅ **Thư viện PZEM-004T hoàn chỉnh** theo datasheet chính thức
- ✅ **Multi-sensor support** với concurrent monitoring
- ✅ **Safety-first tools** không làm hỏng cấu hình thiết bị
- ✅ **Comprehensive documentation** bằng tiếng Việt

### 📊 Web Dashboard Features

- 🌐 **Modern UI** với Bootstrap 5 và responsive design
- 📈 **Interactive charts** với Chart.js và real-time updates
- 📱 **Mobile-friendly** interface và API
- 🔄 **WebSocket real-time** updates mỗi 5 giây
- 📁 **Advanced export** với CSV/JSON và filtering options
- ⚙️ **System management** với health monitoring và cleanup tools

## 📊 Thông số giám sát

Script sẽ đọc và hiển thị các thông số điện quan trọng từ mỗi cảm biến theo tài liệu kỹ thuật PZEM-004T:

| Thông số | Đơn vị | Dải đo | Độ phân giải | Độ chính xác | Ngưỡng bắt đầu |
|----------|---------|--------|--------------|--------------|----------------|
| **Voltage** | V | 80-260V | 0.1V | ±0.5% | - |
| **Current** | A | 0-10A (10A) / 0-100A (100A) | 0.001A | ±0.5% | 0.01A (10A) / 0.02A (100A) |
| **Power** | W | 0-2.3kW (10A) / 0-23kW (100A) | 0.1W | ±0.5% | 0.4W |
| **Energy** | kWh | 0-9999.99kWh | 1Wh | ±0.5% | - |
| **Frequency** | Hz | 45-65Hz | 0.1Hz | ±0.5% | - |
| **Power Factor** | - | 0.00-1.00 | 0.01 | ±1% | - |
| **Alarm** | ON/OFF | Power threshold | - | - | - |

**Lưu ý quan trọng:**
- **Hiển thị công suất**: <1000W hiển thị 1 chữ số thập phân (VD: 999.9W), ≥1000W hiển thị số nguyên (VD: 1000W)
- **Hiển thị năng lượng**: <10kWh đơn vị Wh (VD: 9999Wh), ≥10kWh đơn vị kWh (VD: 9999.99kWh)
- **Độ chính xác**: Tất cả thông số đều có độ chính xác cao theo tiêu chuẩn công nghiệp

## 🎯 Tính năng chính

### Thư viện PZEM-004T
- ✅ **Đọc đầy đủ dữ liệu**: Voltage, Current, Power, Energy, Frequency, Power Factor
- ✅ **Cấu hình thiết bị**: Set/Get power alarm threshold, change device address
- ✅ **Điều khiển**: Reset energy counter, calibration (factory use)
- ✅ **Xử lý lỗi**: CRC validation, Modbus error handling, retry mechanism
- ✅ **Cache thông minh**: Tối ưu hiệu suất với cache dữ liệu (0.1s interval)
- ✅ **API linh hoạt**: Đọc từng giá trị hoặc tất cả cùng lúc
- ✅ **Tương thích ngược**: Hỗ trợ cả tên class cũ và mới

### Công cụ hỗ trợ
- ✅ **Tool reset energy AN TOÀN**: `reset_energy_no_address_change.py` - KHÔNG thay đổi địa chỉ PZEM
- ✅ **Hỗ trợ đa adapter**: PL2303, CH340, CP210, FTDI
- ✅ **Error handling**: Timeout và retry mechanism
- ✅ **Bảo mật**: Xác nhận trước khi reset
- ✅ **Reset tuần tự**: Tránh xung đột khi có nhiều thiết bị cùng địa chỉ

### Ứng dụng giám sát đa cảm biến
- ✅ **Tự động phát hiện cảm biến**: Quét và kết nối tự động với các thiết bị PZEM-004T
- ✅ **Đa cảm biến**: Hỗ trợ đọc từ nhiều cảm biến cùng lúc với threading
- ✅ **Hiển thị dạng bảng**: Dữ liệu từ tất cả cảm biến hiển thị trong bảng thống nhất
- ✅ **Thông tin tổng hợp**: Tính tổng công suất và năng lượng của tất cả cảm biến
- ✅ **Cơ chế retry**: Tự động thử lại khi gặp lỗi kết nối
- ✅ **Hỗ trợ adapter mở rộng**: PL2303, CH340, CP210, FTDI
- ✅ **Cấu trúc code tối ưu**: Tách logic chính, dễ bảo trì và mở rộng

### Ghi dữ liệu CSV
- 📝 **File CSV riêng biệt**: Mỗi cảm biến có file CSV riêng với tên dựa trên cổng
- 🕐 **Timestamp chính xác**: Ghi thời gian đo với định dạng YYYY-MM-DD HH:MM:SS
- 📊 **Dữ liệu đầy đủ**: Ghi tất cả thông số bao gồm datetime, port và các giá trị đo
- 🗂️ **Tổ chức khoa học**: Dữ liệu được lưu trong thư mục `data/csv_logs/`
- 📏 **Quản lý dung lượng**: Tự động dọn dẹp file khi vượt quá kích thước

### Ghi dữ liệu Database (MỚI)
- 💾 **SQLite Database**: Lưu trữ dữ liệu trong database SQLite `data/pzem_data.db`
- ⚡ **Hiệu suất cao**: Truy vấn nhanh với indexes và tối ưu hóa
- 🔍 **Truy vấn linh hoạt**: Hỗ trợ SQL queries mạnh mẽ
- 📊 **Thống kê chi tiết**: Theo dõi sensors và measurements
- 🗑️ **Tự động dọn dẹp**: Xóa dữ liệu cũ tự động
- 🔧 **Tool truy vấn**: `query_database.py` với nhiều tùy chọn xuất dữ liệu
- 🖥️ **GUI Tool**: `database_gui.py` với giao diện tương tác dễ sử dụng

## 🗂️ Cấu trúc dự án

```
ac_management/
├── src/                       # 📚 Thư viện chính
│   ├── __init__.py           # Package initialization
│   ├── pzem.py               # Thư viện PZEM-004T hoàn chỉnh (709 dòng)
│   └── database.py           # Database SQLite module (367 dòng)
├── web/                       # 🌐 Web Dashboard
│   ├── api.py                # FastAPI server chính (748 dòng)
│   ├── static/               # CSS, JS, assets
│   ├── templates/            # HTML templates
│   │   ├── dashboard.html    # Dashboard chính
│   │   ├── export.html       # Export data page
│   │   └── settings.html     # Settings page
│   └── README.md             # Web documentation
├── tools/                     # 🔧 Công cụ ứng dụng
│   ├── __init__.py           # Package initialization
│   ├── read_ac_sensor_db.py  # Multi-sensor monitoring (243 dòng)
│   ├── database_gui.py       # GUI tool tương tác (618 dòng)
│   ├── query_database.py     # Database query tool (403 dòng)
│   ├── reset_energy_no_address_change.py # Energy reset tool (299 dòng)
│   └── read_ac_sensor.py     # Legacy CSV monitoring (362 dòng)
├── docs/                      # 📋 Tài liệu chi tiết
│   ├── PZEM004T.md           # API documentation (572 dòng)
│   ├── DATABASE.md           # Database guide (389 dòng)
│   └── DATA_LOGGING.md       # Data logging guide (231 dòng)
├── data/                      # 📊 Dữ liệu
│   ├── pzem_data.db          # SQLite database chính
│   ├── csv_logs/             # CSV exports
│   └── json_log/             # JSON exports
├── run_web.py                 # 🚀 Web server launcher (116 dòng)
├── Makefile                   # 🛠️ Project management (130 dòng)
├── requirements.txt           # 📦 Dependencies (9 dòng)
├── CHANGELOG.md              # 📝 Version history
├── PROJECT_STRUCTURE.md      # 📋 Detailed structure
├── WEB_DASHBOARD_GUIDE.md    # 🌐 Web dashboard guide
└── README.md                 # 📖 Main documentation
```

## 🚀 Cài đặt và sử dụng

### Yêu cầu hệ thống
- **Python**: 3.9+
- **Dependencies**: FastAPI, uvicorn, pyserial, tabulate, pandas, websockets, jinja2, aiofiles
- **OS**: Linux, macOS, Windows
- **Phần cứng**: PZEM-004T + USB-to-Serial adapter (PL2303, CH340, CP210, FTDI)

### Cài đặt nhanh
```bash
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt
```

### 🌐 Chạy Web Dashboard (Khuyến nghị)

#### Cách nhanh nhất
```bash
# Terminal 1: Start data collection
make run-monitor-db

# Terminal 2: Start web dashboard  
make run-web
```

#### Hoặc manual
```bash
# Chạy data collection
python tools/read_ac_sensor_db.py

# Chạy web server (terminal khác)
python run_web.py
```

#### Truy cập dashboard
- **Dashboard**: http://localhost:8000
- **Export Data**: http://localhost:8000/export
- **Settings**: http://localhost:8000/settings
- **API Docs**: http://localhost:8000/docs

### 🔧 Chạy monitoring (standalone)

#### Database storage (khuyến nghị)
```bash
python tools/read_ac_sensor_db.py
# hoặc
make run-monitor-db
```

#### CSV storage (legacy)
```bash
python tools/read_ac_sensor.py
# hoặc
make run-monitor
```

### Tool reset energy (AN TOÀN - KHUYẾN NGHỊ)
```bash
# Chạy tool reset không thay đổi địa chỉ (AN TOÀN HƠN)
python tools/reset_energy_no_address_change.py

# Hoặc sử dụng command line
python tools/reset_energy_no_address_change.py --all          # Reset tất cả thiết bị
python tools/reset_energy_no_address_change.py --port /dev/ttyUSB0  # Reset thiết bị cụ thể
```

**💡 Lưu ý quan trọng:**
- Tool `reset_energy_no_address_change.py` **KHÔNG thay đổi địa chỉ** của các thiết bị PZEM
- Giữ nguyên địa chỉ mặc định (0xF8) để tránh ảnh hưởng đến cấu hình
- Sử dụng cơ chế reset tuần tự để tránh xung đột
- **Khuyến nghị sử dụng tool này thay vì thay đổi địa chỉ**

### 💾 Quản lý Database

#### GUI Tool (Khuyến nghị)
```bash
# Interactive database management
make db-gui
```

#### Command Line Tools
```bash
# Xem thống kê database
make db-stats

# Xem thông tin sensors
make db-sensors

# Xem measurements gần nhất
make db-latest

# Dọn dẹp dữ liệu cũ
make db-cleanup
```

### Xuất dữ liệu

#### Command Line
```bash
# Xuất dữ liệu ra CSV (file đơn)
python tools/query_database.py --export-csv export.csv --days 7

# Xuất dữ liệu ra JSON (file đơn)
python tools/query_database.py --export-json export.json --days 30

# Xuất dữ liệu theo port riêng biệt (CSV)
python tools/query_database.py --export-csv-separate --days 7

# Xuất dữ liệu theo port riêng biệt (JSON)
python tools/query_database.py --export-json-separate --days 30

# Không overwrite file cũ (tạo file mới với timestamp)
python tools/query_database.py --export-csv-separate --no-overwrite --days 7
```

#### GUI Tool (Khuyến nghị)
```bash
make db-gui
# Hoặc
python tools/database_gui.py
```

## 📊 Quản lý dữ liệu CSV

### Cấu trúc file CSV
```csv
datetime,port,voltage_v,current_a,power_w,energy_wh,frequency_hz,power_factor,alarm_status
2025-08-04 10:30:00,/dev/ttyUSB0,225.4,0.830,185.2,1547,50.0,0.98,OFF
2025-08-04 10:30:05,/dev/ttyUSB0,225.6,0.835,186.1,1547,50.0,0.98,OFF
```

### Xem dữ liệu CSV
```bash
# Xem 10 dòng cuối
tail -10 data/csv_logs/pzem__dev_ttyUSB0.csv

# Đếm số dòng dữ liệu
wc -l data/csv_logs/pzem__dev_ttyUSB0.csv
```

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

# Hoặc thêm user vào group dialout
sudo usermod -a -G dialout $USER
```

#### 3. Thiết bị không phản hồi
- Kiểm tra kết nối TTL: GND, TX, RX, 5V
- Đảm bảo nguồn 5V cho TTL interface
- Kiểm tra địa chỉ thiết bị (mặc định 0xF8)

#### 4. Dữ liệu không chính xác
- Kiểm tra kết nối điện L, N
- Với PZEM-004T-100A, kiểm tra CT
- Reset thiết bị nếu cần

#### 5. Reset energy không hoạt động với nhiều thiết bị
```bash
# Giải pháp AN TOÀN - KHÔNG thay đổi địa chỉ (KHUYẾN NGHỊ)
python tools/reset_energy_no_address_change.py
```

**💡 Khuyến nghị:** Sử dụng `reset_energy_no_address_change.py` để tránh ảnh hưởng đến cấu hình PZEM.

## 📚 Tài liệu tham khảo

### 🌐 Web Dashboard
- **[WEB_DASHBOARD_GUIDE.md](WEB_DASHBOARD_GUIDE.md)**: Hướng dẫn đầy đủ web dashboard
- **[web/README.md](web/README.md)**: API documentation và deployment

### 📖 Thư viện và Tools
- **[docs/PZEM004T.md](docs/PZEM004T.md)**: API reference thư viện PZEM-004T
- **[docs/DATABASE.md](docs/DATABASE.md)**: Database management guide
- **[docs/DATA_LOGGING.md](docs/DATA_LOGGING.md)**: Data logging và export

### 🏗️ Cấu trúc dự án
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**: Cấu trúc dự án chi tiết
- **[CHANGELOG.md](CHANGELOG.md)**: Lịch sử phát triển và cập nhật

## 🤝 Đóng góp và phát triển

### 🏗️ Kiến trúc hệ thống
```
PZEM-004T Sensors
       ↓
Serial Communication (Modbus-RTU)
       ↓
Python PZEM Library (src/pzem.py)
       ↓
Database Storage (src/database.py)
       ↓
FastAPI Web Server (web/api.py)
    ↙        ↘
Web Dashboard  REST API
       ↓         ↓
Bootstrap UI   Mobile App
Chart.js      (Future)
```

### 🔧 Core Components
- **`src/pzem.py`**: Thư viện PZEM-004T hoàn chỉnh (709 dòng)
- **`src/database.py`**: Database SQLite module (367 dòng)
- **`web/api.py`**: FastAPI server với REST API (748 dòng)
- **`tools/read_ac_sensor_db.py`**: Multi-sensor monitoring (243 dòng)
- **`tools/database_gui.py`**: GUI management tool (618 dòng)
- **`tools/reset_energy_no_address_change.py`**: Safe energy reset (299 dòng)

### 🌟 Key Features Implemented
- ✅ **Complete PZEM-004T library** với Modbus-RTU protocol
- ✅ **Modern web dashboard** với real-time charts
- ✅ **SQLite database** với efficient storage
- ✅ **REST API** cho mobile integration  
- ✅ **Multi-sensor support** với concurrent monitoring
- ✅ **Safety tools** không làm hỏng cấu hình
- ✅ **Comprehensive documentation** bằng tiếng Việt

## 📈 Roadmap & Future Development

### ✅ Đã hoàn thành (v2.1.0+)
- [x] Web dashboard với real-time monitoring
- [x] REST API endpoints hoàn chỉnh
- [x] Database storage system
- [x] Mobile-ready API với WebSocket
- [x] Advanced export functionality
- [x] Comprehensive documentation

### 🚧 Đang phát triển
- [ ] **Authentication system** (JWT cho API)
- [ ] **Data aggregation** (hourly/daily summaries)
- [ ] **Alert system** (email/SMS notifications)
- [ ] **Performance optimization** (caching, compression)

### 🔮 Kế hoạch tương lai
- [ ] **Mobile app** (React Native/Flutter)
- [ ] **Cloud deployment** (Docker + Kubernetes)
- [ ] **PostgreSQL support** cho production scale
- [ ] **Machine learning** dự đoán consumption patterns
- [ ] **Multi-tenant system** cho nhiều location

## 📄 License

Dự án này được phân phối dưới giấy phép MIT. Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 🤝 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork dự án
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📞 Liên hệ

- **Email**: [levanduy.work@gmail.com]
- **GitHub**: [levanduy093-work]

## 🎉 Quick Start Guide

### 🚀 Để bắt đầu ngay (2 phút):
```bash
# 1. Clone và cài đặt
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt

# 2. Chạy monitoring (Terminal 1)
make run-monitor-db

# 3. Chạy web dashboard (Terminal 2) 
make run-web

# 4. Truy cập dashboard: http://localhost:8000
```

### 📱 API cho mobile app:
- **Base URL**: `http://localhost:8000/api/`
- **WebSocket**: `ws://localhost:8000/ws/realtime`
- **Documentation**: `http://localhost:8000/docs`

---

**🏆 AC Management** - Hệ thống giám sát điện năng PZEM-004T hoàn chỉnh và chuyên nghiệp. Từ hardware setup đến web dashboard, tất cả đều được thiết kế để đảm bảo **reliability**, **safety** và **ease of use**.