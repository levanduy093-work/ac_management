# Cấu trúc dự án AC Management

## Tổng quan

Dự án AC Management là một hệ thống Python chuyên nghiệp để giám sát và ghi dữ liệu từ cảm biến công suất điện PZEM-004T sử dụng giao thức Modbus-RTU. Dự án bao gồm thư viện hoàn chỉnh, ứng dụng giám sát đa cảm biến và các công cụ hỗ trợ.

## Cấu trúc thư mục

```
ac_management/
├── src/                       # 📚 Thư viện chính
│   ├── __init__.py           # Package initialization (17 dòng)
│   ├── pzem.py               # Thư viện PZEM-004T hoàn chỉnh (709 dòng)
│   └── database.py           # Database module (356 dòng)
├── tools/                     # 🔧 Công cụ ứng dụng
│   ├── __init__.py           # Package initialization (7 dòng)
│   ├── read_ac_sensor.py     # Script giám sát đa cảm biến (CSV) (362 dòng)
│   ├── read_ac_sensor_db.py  # Script giám sát đa cảm biến (Database) (243 dòng)
│   ├── query_database.py     # Tool truy vấn database (403 dòng)
│   ├── database_gui.py       # GUI tool tương tác (618 dòng)
│   └── reset_energy_no_address_change.py # Tool reset energy AN TOÀN (299 dòng)
├── docs/                      # 📋 Tài liệu
│   ├── PZEM004T.md           # Hướng dẫn chi tiết thư viện (572 dòng)
│   ├── DATA_LOGGING.md       # Hướng dẫn CSV logging (114 dòng)
│   └── DATABASE.md           # Hướng dẫn database storage (389 dòng)
├── data/                      # 📊 Dữ liệu
│   ├── csv_logs/             # File CSV logs
│   ├── json_log/             # File JSON logs
│   └── pzem_data.db          # SQLite database
├── Makefile                   # 🛠️ Quản lý dự án (121 dòng)
├── requirements.txt           # 📦 Dependencies (4 dòng)
├── CHANGELOG.md              # 📝 Lịch sử thay đổi (104 dòng)
├── LICENSE                   # 📄 Giấy phép (22 dòng)
├── README.md                 # 📖 Tài liệu chính (318 dòng)
└── PROJECT_STRUCTURE.md      # 📋 File này (256 dòng)
```

## Mô tả chi tiết

### 📚 Thư viện chính (`src/`)

#### `src/__init__.py` (17 dòng)
- Khởi tạo package Python
- Export các class chính: `PZEM004T`, `PZEM004Tv30`
- Version: 2.0.0
- Author: AC Management Team

#### `src/pzem.py` (709 dòng)
- **Thư viện PZEM-004T hoàn chỉnh** với triển khai đầy đủ giao thức Modbus-RTU
- Hỗ trợ tất cả function codes và register mapping theo tài liệu kỹ thuật
- Xử lý lỗi toàn diện với CRC validation và error handling
- Cache thông minh để tối ưu hiệu suất (update_interval = 0.1s)
- API đầy đủ cho đọc dữ liệu, cấu hình và điều khiển
- Tương thích ngược với tên class cũ `PZEM004Tv30`
- Hỗ trợ calibration và reset energy với verification
- **Cải tiến reset energy** với retry mechanism và timeout thông minh

#### `src/database.py` (356 dòng)
- **Database module** cho SQLite database
- Quản lý bảng `sensors` và `measurements`
- API để lưu trữ và truy vấn dữ liệu PZEM-004T
- Tự động tạo indexes cho hiệu suất tốt
- Hỗ trợ cleanup dữ liệu cũ
- Thống kê database chi tiết

### 🔧 Công cụ ứng dụng (`tools/`)

#### `tools/__init__.py` (7 dòng)
- Khởi tạo package tools
- Version: 2.0.0

#### `tools/read_ac_sensor.py` (362 dòng)
- **Script giám sát đa cảm biến với CSV storage**
- Tự động phát hiện và kết nối với các thiết bị PZEM-004T
- Hỗ trợ nhiều loại USB-to-Serial adapter: PL2303, CH340, CP210, FTDI
- Đọc dữ liệu từ nhiều cảm biến cùng lúc với threading
- Hiển thị dạng bảng với thông tin tổng hợp
- Ghi dữ liệu CSV với timestamp và quản lý file size
- Cơ chế retry và error handling toàn diện
- Tính tổng công suất và năng lượng của tất cả cảm biến

#### `tools/read_ac_sensor_db.py` (243 dòng)
- **Script giám sát đa cảm biến với Database storage**
- Tương tự `read_ac_sensor.py` nhưng lưu vào SQLite database
- Sử dụng `database.py` module để quản lý dữ liệu
- Hiệu suất tốt hơn cho dữ liệu lớn
- Tự động quản lý sensors và measurements
- Thống kê real-time từ database

#### `tools/query_database.py` (403 dòng)
- **Tool truy vấn database** với nhiều tùy chọn
- Command line interface cho truy vấn dữ liệu
- Export dữ liệu ra CSV và JSON
- Hỗ trợ export single file và separate files by port
- Tùy chọn overwrite hoặc tạo file mới với timestamp
- Filter theo port, thời gian, số lượng records
- Thống kê database và sensor summary

#### `tools/database_gui.py` (618 dòng)
- **GUI tool tương tác** cho quản lý database
- Menu-driven interface dễ sử dụng
- Xem thống kê database và sensor summary
- Export dữ liệu với giao diện thân thiện
- Advanced queries và cleanup tools
- Không cần nhớ command line options

#### `tools/reset_energy_no_address_change.py` (299 dòng)
- **Tool reset energy counter AN TOÀN** - KHÔNG thay đổi địa chỉ PZEM
- Tự động phát hiện thiết bị PZEM-004T
- Reset bộ đếm năng lượng cho từng thiết bị tuần tự
- **Giữ nguyên địa chỉ mặc định** (0xF8) để tránh ảnh hưởng cấu hình
- Sử dụng timeout ngắn và retry mechanism để tránh xung đột
- Hiển thị trạng thái reset và báo cáo kết quả chi tiết
- Hỗ trợ nhiều loại USB-to-Serial adapter
- Menu tương tác dễ sử dụng
- **Giải pháp tối ưu** cho vấn đề reset với nhiều thiết bị

### 📋 Tài liệu (`docs/`)

#### `docs/PZEM004T.md` (572 dòng)
- **Hướng dẫn chi tiết thư viện** với API reference đầy đủ
- Ví dụ sử dụng thực tế và troubleshooting guide
- Thông số kỹ thuật chi tiết theo datasheet
- Hướng dẫn kết nối phần cứng và cài đặt

#### `docs/DATA_LOGGING.md` (114 dòng)
- **Hướng dẫn CSV logging** với cấu trúc file chi tiết
- Quản lý dữ liệu và phân tích
- Backup và dọn dẹp dữ liệu cũ

#### `docs/DATABASE.md` (389 dòng)
- **Hướng dẫn database storage** với SQLite
- Cấu trúc database và schema
- Sử dụng database tools và GUI
- Migration từ CSV sang database
- Quản lý và backup database

### 📊 Dữ liệu (`data/`)

#### `data/csv_logs/`
- **File CSV logs** cho từng cảm biến với dữ liệu thực tế
- Tên file dựa trên cổng serial: `pzem__{port_name}.csv`
- Cấu trúc: datetime, port, voltage_v, current_a, power_w, energy_wh, frequency_hz, power_factor, alarm_status
- Dữ liệu với timestamp chính xác và tất cả thông số đo

#### `data/json_log/`
- **File JSON logs** cho export dữ liệu
- Tên file: `export.json` hoặc `pzem_{port_name}.json`
- Format JSON với indent và UTF-8 encoding
- Dữ liệu tương tự CSV nhưng dạng JSON

#### `data/pzem_data.db`
- **SQLite database** chính cho lưu trữ dữ liệu
- Bảng `sensors`: thông tin cảm biến
- Bảng `measurements`: dữ liệu đo
- Indexes cho hiệu suất truy vấn tốt
- Tự động quản lý và cleanup

### 🛠️ Quản lý dự án

#### `Makefile` (121 dòng)
- **Quản lý dự án** với các commands tiện lợi
- Install dependencies và development tools
- Run monitoring scripts (CSV và Database)
- Database operations (stats, sensors, cleanup)
- Export data và GUI tools
- Code quality (lint, format)

#### `requirements.txt` (4 dòng)
- **Dependencies** cần thiết:
  - `pyserial`: Serial communication
  - `tabulate`: Table formatting
  - `pandas`: Data analysis

#### `CHANGELOG.md` (104 dòng)
- **Lịch sử thay đổi** chi tiết
- Version 2.0.0: Complete library rewrite
- Major features và bug fixes
- Breaking changes và improvements

#### `LICENSE` (22 dòng)
- **MIT License** cho dự án
- Cho phép sử dụng tự do với attribution

## Tính năng chính

### 🔌 Thư viện PZEM-004T
- **Đọc đầy đủ dữ liệu**: Voltage, Current, Power, Energy, Frequency, Power Factor
- **Cấu hình thiết bị**: Set/Get power alarm threshold, change device address
- **Điều khiển**: Reset energy counter, calibration (factory use)
- **Xử lý lỗi**: CRC validation, Modbus error handling, retry mechanism
- **Cache thông minh**: Tối ưu hiệu suất với cache dữ liệu (0.1s interval)
- **API linh hoạt**: Đọc từng giá trị hoặc tất cả cùng lúc
- **Tương thích ngược**: Hỗ trợ cả tên class cũ và mới

### 📊 Ứng dụng giám sát
- **Tự động phát hiện cảm biến**: Quét và kết nối tự động với các thiết bị PZEM-004T
- **Đa cảm biến**: Hỗ trợ đọc từ nhiều cảm biến cùng lúc với threading
- **Hiển thị dạng bảng**: Dữ liệu từ tất cả cảm biến hiển thị trong bảng thống nhất
- **Thông tin tổng hợp**: Tính tổng công suất và năng lượng của tất cả cảm biến
- **Cơ chế retry**: Tự động thử lại khi gặp lỗi kết nối
- **Hỗ trợ adapter mở rộng**: PL2303, CH340, CP210, FTDI

### 💾 Lưu trữ dữ liệu
- **CSV Storage**: File riêng biệt cho từng cảm biến
- **Database Storage**: SQLite với hiệu suất cao và quản lý tốt
- **Export Tools**: CSV và JSON với nhiều tùy chọn
- **GUI Interface**: Tương tác dễ dàng không cần command line

### 🔧 Công cụ hỗ trợ
- **Reset Energy Tool**: AN TOÀN - không thay đổi địa chỉ PZEM
- **Database Management**: Stats, cleanup, migration
- **Export Tools**: Command line và GUI
- **Error Handling**: Comprehensive error handling và retry mechanisms

## Cách sử dụng

### Cài đặt
```bash
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt
```

### Chạy giám sát
```bash
# CSV storage
make run-monitor

# Database storage (khuyến nghị)
make run-monitor-db
```

### Quản lý database
```bash
# GUI tool (khuyến nghị)
make db-gui

# Command line
make db-stats
make db-sensors
make db-latest
make db-cleanup
```

### Reset energy
```bash
make run-reset
```

## Phát triển

### Cấu trúc code
- **Modular design**: Tách biệt thư viện, tools, và documentation
- **Error handling**: Comprehensive error handling trong tất cả modules
- **Documentation**: Detailed documentation cho tất cả components
- **Testing**: Ready for unit tests và integration tests

### Contributing
- Fork dự án
- Tạo feature branch
- Commit changes với descriptive messages
- Push và tạo Pull Request

## License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết. 