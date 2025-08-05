# Cấu trúc dự án AC Management

## Tổng quan

Dự án AC Management là một hệ thống Python chuyên nghiệp để giám sát và ghi dữ liệu từ cảm biến công suất điện PZEM-004T sử dụng giao thức Modbus-RTU. Dự án bao gồm thư viện hoàn chỉnh, ứng dụng giám sát đa cảm biến và các công cụ hỗ trợ.

## Cấu trúc thư mục

```
ac_management/
├── src/                       # 📚 Thư viện chính
│   ├── __init__.py           # Package initialization (17 dòng)
│   └── pzem.py               # Thư viện PZEM-004T hoàn chỉnh (694 dòng)
├── tools/                     # 🔧 Công cụ ứng dụng
│   ├── __init__.py           # Package initialization (7 dòng)
│   ├── read_ac_sensor.py     # Script giám sát đa cảm biến (362 dòng)
│   └── reset_energy.py       # Tool reset energy counter (82 dòng)
├── docs/                      # 📋 Tài liệu
│   ├── PZEM004T.md           # Hướng dẫn chi tiết thư viện (572 dòng)
│   └── DATA_LOGGING.md       # Hướng dẫn CSV logging (114 dòng)
├── data/                      # 📊 Dữ liệu
│   └── csv_logs/             # File CSV logs
│       ├── pzem__dev_ttyUSB0.csv (49 dòng dữ liệu)
│       ├── pzem__dev_ttyUSB1.csv (49 dòng dữ liệu)
│       └── pzem__dev_ttyUSB2.csv (49 dòng dữ liệu)
├── Makefile                   # 🛠️ Quản lý dự án (84 dòng)
├── requirements.txt           # 📦 Dependencies (4 dòng)
├── CHANGELOG.md              # 📝 Lịch sử thay đổi (82 dòng)
├── LICENSE                   # 📄 Giấy phép (22 dòng)
├── README.md                 # 📖 Tài liệu chính (407 dòng)
└── PROJECT_STRUCTURE.md      # 📋 File này (227 dòng)
```

## Mô tả chi tiết

### 📚 Thư viện chính (`src/`)

#### `src/__init__.py` (17 dòng)
- Khởi tạo package Python
- Export các class chính: `PZEM004T`, `PZEM004Tv30`
- Version: 2.0.0
- Author: AC Management Team

#### `src/pzem.py` (694 dòng)
- **Thư viện PZEM-004T hoàn chỉnh** với triển khai đầy đủ giao thức Modbus-RTU
- Hỗ trợ tất cả function codes và register mapping theo tài liệu kỹ thuật
- Xử lý lỗi toàn diện với CRC validation và error handling
- Cache thông minh để tối ưu hiệu suất (update_interval = 0.1s)
- API đầy đủ cho đọc dữ liệu, cấu hình và điều khiển
- Tương thích ngược với tên class cũ `PZEM004Tv30`
- Hỗ trợ calibration và reset energy với verification

### 🔧 Công cụ ứng dụng (`tools/`)

#### `tools/__init__.py` (7 dòng)
- Khởi tạo package tools
- Version: 2.0.0

#### `tools/read_ac_sensor.py` (362 dòng)
- **Script giám sát đa cảm biến** với tính năng nâng cao
- Tự động phát hiện và kết nối với các thiết bị PZEM-004T
- Hỗ trợ nhiều loại USB-to-Serial adapter: PL2303, CH340, CP210, FTDI
- Đọc dữ liệu từ nhiều cảm biến cùng lúc với threading
- Hiển thị dạng bảng với thông tin tổng hợp
- Ghi dữ liệu CSV với timestamp và quản lý file size
- Cơ chế retry và error handling toàn diện
- Tính tổng công suất và năng lượng của tất cả cảm biến

#### `tools/reset_energy.py` (82 dòng)
- **Tool reset energy counter** với giao diện đơn giản
- Tự động phát hiện thiết bị PZEM-004T
- Reset bộ đếm năng lượng cho từng thiết bị
- Hiển thị trạng thái reset và báo cáo kết quả
- Hỗ trợ nhiều loại USB-to-Serial adapter
- Timeout và error handling

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

### 📊 Dữ liệu (`data/`)

#### `data/csv_logs/`
- **File CSV logs** cho từng cảm biến với dữ liệu thực tế
- Tên file dựa trên cổng serial: `pzem__{port_name}.csv`
- Cấu trúc: datetime, port, voltage_v, current_a, power_w, energy_wh, frequency_hz, power_factor, alarm_status
- Dữ liệu với timestamp chính xác và tất cả thông số đo

### 🛠️ Quản lý dự án

#### `Makefile` (84 dòng)
- **Quản lý dự án** với các lệnh cài đặt, test, lint, format
- Chạy các công cụ chính: `make run-monitor`, `make run-reset`
- Documentation generation và project management

#### `requirements.txt` (4 dòng)
- **Dependencies**: pyserial, tabulate, pandas
- Phiên bản tối thiểu cho Python 3.7+

### 📝 Tài liệu dự án

#### `README.md` (407 dòng)
- **Tài liệu chính** với tổng quan dự án chi tiết
- Hướng dẫn cài đặt và sử dụng từng bước
- Tính năng chi tiết và troubleshooting guide
- Thông số kỹ thuật chính xác theo datasheet
- Ví dụ sử dụng và giao diện output

#### `CHANGELOG.md` (82 dòng)
- **Lịch sử thay đổi** theo format Keep a Changelog
- Semantic Versioning với phiên bản 2.0.0 hiện tại
- Chi tiết các thay đổi qua các phiên bản

#### `LICENSE` (22 dòng)
- **Giấy phép MIT** với điều khoản sử dụng và phân phối

## Tính năng chính

### Thư viện PZEM-004T
- ✅ **Đọc đầy đủ dữ liệu**: Voltage, Current, Power, Energy, Frequency, Power Factor
- ✅ **Thông số kỹ thuật chính xác**: Theo tài liệu PZEM-004T với độ chính xác ±0.5%
- ✅ **Cấu hình thiết bị**: Set/Get power alarm threshold, change device address
- ✅ **Điều khiển**: Reset energy counter, calibration (factory use)
- ✅ **Xử lý lỗi**: CRC validation, Modbus error handling, retry mechanism
- ✅ **Cache thông minh**: Tối ưu hiệu suất với cache dữ liệu (0.1s interval)
- ✅ **API linh hoạt**: Đọc từng giá trị hoặc tất cả cùng lúc
- ✅ **Quy tắc hiển thị**: Tuân thủ datasheet cho công suất và năng lượng
- ✅ **Tương thích ngược**: Hỗ trợ cả tên class cũ và mới

### Công cụ hỗ trợ
- ✅ **Tool reset energy**: Tự động phát hiện, reset với báo cáo chi tiết
- ✅ **Hỗ trợ đa adapter**: PL2303, CH340, CP210, FTDI
- ✅ **Error handling**: Timeout và retry mechanism
- ✅ **Bảo mật**: Xác nhận trước khi reset

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

## Thông số kỹ thuật

### Phần cứng được hỗ trợ
- **Cảm biến**: PZEM-004T-10A (0-10A), PZEM-004T-100A (0-100A)
- **USB-to-Serial adapter**: PL2303, CH340, CP210, FTDI
- **Kết nối**: TTL interface với đầy đủ 4 chân (GND, TX, RX, 5V)

### Thông số đo chính xác
- **Voltage**: 80-260V, resolution 0.1V, accuracy ±0.5%
- **Current**: 0-10A/0-100A, resolution 0.001A, accuracy ±0.5%
- **Power**: 0-2.3kW/0-23kW, resolution 0.1W, accuracy ±0.5%
- **Energy**: 0-9999.99kWh, resolution 1Wh, accuracy ±0.5%
- **Frequency**: 45-65Hz, resolution 0.1Hz, accuracy ±0.5%
- **Power Factor**: 0.00-1.00, resolution 0.01, accuracy ±1%

### Quy tắc hiển thị theo datasheet
- **Power**: <1000W hiển thị 1 chữ số thập phân, ≥1000W hiển thị số nguyên
- **Energy**: <10kWh đơn vị Wh, ≥10kWh đơn vị kWh

## Roadmap

### Tính năng đang phát triển
- [ ] Web interface với Flask/Django
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] REST API endpoints
- [ ] Mobile app companion
- [ ] Advanced analytics và machine learning
- [ ] Multi-site monitoring
- [ ] Cloud integration (AWS IoT, Azure IoT)
- [ ] GUI application với tkinter/PyQt
- [ ] Automated testing suite
- [ ] Docker containerization

### Cải thiện cấu trúc
- [ ] Examples directory với các ví dụ sử dụng
- [ ] Setup script cho cài đặt thư viện
- [ ] Unit tests và integration tests
- [ ] CI/CD pipeline
- [ ] Code coverage reporting

## Yêu cầu hệ thống

### Phần cứng
- **Cảm biến**: PZEM-004T-10A hoặc PZEM-004T-100A
- **USB-to-Serial adapter**: PL2303, CH340, CP210, FTDI
- **Kết nối**: TTL interface với đầy đủ 4 chân (GND, TX, RX, 5V)

### Phần mềm
- **Python**: 3.7+
- **Dependencies**: pyserial, tabulate, pandas
- **OS**: Linux, macOS, Windows

## Cách sử dụng

### Cài đặt
```bash
git clone <repository-url>
cd ac_management
pip install -r requirements.txt
```

### Chạy giám sát
```bash
python tools/read_ac_sensor.py
# hoặc
make run-monitor
```

### Reset energy
```bash
python tools/reset_energy.py
# hoặc
make run-reset
```

### Sử dụng thư viện
```python
from src.pzem import PZEM004T

pzem = PZEM004T(port='/dev/ttyUSB0')
measurements = pzem.get_all_measurements()
print(f"Power: {measurements['power']:.1f}W")
```

---

**Lưu ý**: Cấu trúc này được cập nhật lần cuối vào tháng 8/2025 và phản ánh trạng thái hiện tại của dự án với phiên bản 2.0.0. 