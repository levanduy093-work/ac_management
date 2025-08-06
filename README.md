# 🔌 AC Management - PZEM-004T Power Monitoring & Data Logger

Một hệ thống Python chuyên nghiệp để giám sát và ghi dữ liệu từ cảm biến công suất điện PZEM-004T sử dụng giao thức Modbus-RTU. Dự án bao gồm thư viện hoàn chỉnh, ứng dụng giám sát đa cảm biến và các công cụ hỗ trợ.

## 🆕 Cập nhật mới - Thư viện PZEM-004T hoàn chỉnh

### ✨ Tính năng mới trong thư viện

- **Thư viện hoàn chỉnh**: Triển khai đầy đủ giao thức Modbus-RTU theo tài liệu kỹ thuật
- **API đầy đủ**: Hỗ trợ tất cả function codes và register mapping
- **Xử lý lỗi toàn diện**: CRC validation, error handling, retry mechanism
- **Cache thông minh**: Tối ưu hiệu suất với cache dữ liệu (0.1s interval)
- **Tương thích ngược**: Hỗ trợ cả tên class cũ và mới

### 🔄 Cập nhật ứng dụng giám sát

- **Sử dụng thư viện mới**: `read_ac_sensor.py` đã được cập nhật để sử dụng thư viện PZEM-004T mới
- **Hiệu suất tốt hơn**: Sử dụng API `get_all_measurements()` thay vì `update_values()`
- **Hỗ trợ adapter mở rộng**: Thêm hỗ trợ CP210, FTDI ngoài PL2303, CH340
- **Cấu trúc code cải thiện**: Tách logic chính vào hàm `main()` để dễ bảo trì

### 📚 Tài liệu chi tiết

- **[docs/PZEM004T.md](docs/PZEM004T.md)**: Hướng dẫn chi tiết thư viện PZEM-004T
- **[src/pzem.py](src/pzem.py)**: Thư viện chính hoàn chỉnh

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
- ✅ **Quản lý file size**: Tự động dọn dẹp file CSV khi quá lớn

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

## 🗂️ Cấu trúc dự án

```
ac_management/
├── src/                       # 📚 Thư viện chính
│   ├── __init__.py           # Package initialization (17 dòng)
│   └── pzem.py               # Thư viện PZEM-004T hoàn chỉnh (709 dòng)
├── tools/                     # 🔧 Công cụ ứng dụng
│   ├── __init__.py           # Package initialization (7 dòng)
│   ├── read_ac_sensor.py     # Script giám sát đa cảm biến (CSV) (362 dòng)
│   ├── read_ac_sensor_db.py  # Script giám sát đa cảm biến (Database) (MỚI)
│   ├── query_database.py     # Tool truy vấn database (MỚI)
│   ├── database_gui.py       # GUI tool tương tác (MỚI)
│   └── reset_energy_no_address_change.py # Tool reset energy AN TOÀN (299 dòng)
├── docs/                      # 📋 Tài liệu
│   ├── PZEM004T.md           # Hướng dẫn chi tiết thư viện (572 dòng)
│   ├── DATA_LOGGING.md       # Hướng dẫn CSV logging (114 dòng)
│   └── DATABASE.md           # Hướng dẫn database storage (MỚI)
├── data/                      # 📊 Dữ liệu
│   └── csv_logs/             # File CSV logs
│       ├── pzem__dev_ttyUSB0.csv (49 dòng dữ liệu)
│       ├── pzem__dev_ttyUSB1.csv (49 dòng dữ liệu)
│       └── pzem__dev_ttyUSB2.csv (49 dòng dữ liệu)
├── Makefile                   # 🛠️ Quản lý dự án (84 dòng)
├── requirements.txt           # 📦 Dependencies (4 dòng)
├── CHANGELOG.md              # 📝 Lịch sử thay đổi (108 dòng)
├── LICENSE                   # 📄 Giấy phép (22 dòng)
├── README.md                 # 📖 Tài liệu chính (467 dòng)
└── PROJECT_STRUCTURE.md      # 📋 Cấu trúc dự án (248 dòng)
```

## 🚀 Cài đặt và sử dụng

### Yêu cầu hệ thống
- **Python**: 3.9+
- **Dependencies**: pyserial, tabulate, pandas
- **OS**: Linux, macOS, Windows
- **Phần cứng**: PZEM-004T + USB-to-Serial adapter (PL2303, CH340, CP210, FTDI)

### Cài đặt
```bash
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt
```

### Chạy giám sát

#### Sử dụng CSV (cách cũ)
```bash
python tools/read_ac_sensor.py
# hoặc
make run-monitor
```

#### Sử dụng Database (khuyến nghị)
```bash
python tools/read_ac_sensor_db.py
# hoặc
make run-monitor-db
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

### Quản lý Database
```bash
# Xem thống kê database
make db-stats

# Xem thông tin sensors
make db-sensors

# Xem measurements gần nhất
make db-latest

# Dọn dẹp dữ liệu cũ
make db-cleanup

# Xuất dữ liệu ra CSV (file đơn)
python tools/query_database.py --export-csv export.csv --days 7

# Xuất dữ liệu ra JSON (file đơn)
python tools/query_database.py --export-json export.json --days 30

# 🆕 Xuất dữ liệu theo port riêng biệt (CSV)
python tools/query_database.py --export-csv-separate --days 7

# 🆕 Xuất dữ liệu theo port riêng biệt (JSON)
python tools/query_database.py --export-json-separate --days 30

# 🆕 GUI Tool tương tác (khuyến nghị)
make db-gui
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

- **[docs/PZEM004T.md](docs/PZEM004T.md)**: Hướng dẫn chi tiết thư viện
- **[docs/DATA_LOGGING.md](docs/DATA_LOGGING.md)**: Hướng dẫn CSV logging
- **[docs/DATABASE.md](docs/DATABASE.md)**: Hướng dẫn database storage
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**: Cấu trúc dự án chi tiết

## 🤝 Đóng góp và phát triển

### Cấu trúc code
- `src/pzem.py`: Thư viện PZEM-004T hoàn chỉnh (709 dòng)
- `tools/read_ac_sensor.py`: Ứng dụng giám sát đa cảm biến (362 dòng)
- `tools/reset_energy_no_address_change.py`: Tool reset energy AN TOÀN (299 dòng) ⭐

### Các thay đổi chính trong read_ac_sensor.py
- **Sử dụng thư viện mới**: Thay thế `PZEM004Tv30` bằng `PZEM004T`
- **API cải thiện**: Sử dụng `get_all_measurements()` thay vì `update_values()`
- **Hiệu suất tốt hơn**: Cache thông minh với interval 0.1s
- **Error handling**: Retry mechanism và timeout cải thiện
- **Hỗ trợ adapter mở rộng**: Thêm CP210, FTDI ngoài PL2303, CH340

### Các thay đổi chính trong reset_energy_no_address_change.py
- **KHÔNG thay đổi địa chỉ**: Giữ nguyên địa chỉ mặc định (0xF8)
- **Reset tuần tự**: Tránh xung đột khi có nhiều thiết bị cùng địa chỉ
- **Retry mechanism**: Thử lại 3 lần cho mỗi thiết bị
- **Timeout thông minh**: Đợi lâu hơn giữa các thiết bị có xung đột địa chỉ
- **Menu tương tác**: Dễ sử dụng với xác nhận an toàn

## 📈 Roadmap

### Tính năng đang phát triển
- [ ] Web interface với Flask/Django
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] REST API endpoints
- [ ] Mobile app companion
- [ ] Advanced analytics và machine learning
- [ ] Multi-site monitoring


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

---

**Lưu ý**: Dự án này được phát triển để giám sát và ghi dữ liệu từ cảm biến PZEM-004T một cách chuyên nghiệp và đáng tin cậy. Tool reset energy đã được tối ưu để không thay đổi địa chỉ PZEM, đảm bảo an toàn và dễ sử dụng.