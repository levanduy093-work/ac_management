# Cấu trúc dự án AC Management

## Tổng quan

Dự án AC Management là một hệ thống Python chuyên nghiệp để giám sát và ghi dữ liệu từ cảm biến công suất điện PZEM-004T sử dụng giao thức Modbus-RTU.

## Cấu trúc thư mục

```
ac_management/
├── src/                       # 📚 Thư viện chính
│   ├── __init__.py           # Package initialization
│   └── pzem.py               # Thư viện PZEM-004T hoàn chỉnh
├── tools/                     # 🔧 Công cụ ứng dụng
│   ├── __init__.py           # Package initialization
│   ├── read_ac_sensor.py     # Script giám sát đa cảm biến
│   └── reset_energy.py       # Tool reset energy counter
├── docs/                      # 📋 Tài liệu
│   ├── PZEM004T.md           # Hướng dẫn chi tiết thư viện
│   └── DATA_LOGGING.md       # Hướng dẫn CSV logging
├── data/                      # 📊 Dữ liệu
│   └── csv_logs/             # File CSV logs
│       ├── pzem__dev_ttyUSB0.csv
│       ├── pzem__dev_ttyUSB1.csv
│       └── pzem__dev_ttyUSB2.csv
├── Makefile                   # 🛠️ Quản lý dự án
├── requirements.txt           # 📦 Dependencies
├── CHANGELOG.md              # 📝 Lịch sử thay đổi
├── LICENSE                   # 📄 Giấy phép
├── README.md                 # 📖 Tài liệu chính
└── PROJECT_STRUCTURE.md      # 📋 File này
```

## Mô tả chi tiết

### 📚 Thư viện chính (`src/`)

#### `src/__init__.py`
- Khởi tạo package Python
- Export các class và function chính

#### `src/pzem.py`
- **Thư viện PZEM-004T hoàn chỉnh** (640 dòng)
- Triển khai đầy đủ giao thức Modbus-RTU
- Hỗ trợ tất cả function codes và register mapping
- Xử lý lỗi toàn diện với CRC validation
- Cache thông minh để tối ưu hiệu suất
- API đầy đủ cho đọc dữ liệu, cấu hình và điều khiển

### 🔧 Công cụ ứng dụng (`tools/`)

#### `tools/__init__.py`
- Khởi tạo package tools

#### `tools/read_ac_sensor.py`
- **Script giám sát đa cảm biến** (362 dòng)
- Tự động phát hiện và kết nối với các thiết bị PZEM-004T
- Đọc dữ liệu từ nhiều cảm biến cùng lúc
- Hiển thị dạng bảng với thông tin tổng hợp
- Ghi dữ liệu CSV với timestamp
- Hỗ trợ nhiều loại USB-to-Serial adapter

#### `tools/reset_energy.py`
- **Tool reset energy counter** (284 dòng)
- Menu tương tác với 5 tùy chọn
- Xác nhận an toàn trước khi reset
- Hiển thị thông tin thiết bị trước khi reset
- Báo cáo chi tiết kết quả reset
- Hỗ trợ nhiều loại USB-to-Serial adapter

### 📋 Tài liệu (`docs/`)

#### `docs/PZEM004T.md`
- **Hướng dẫn chi tiết thư viện** (520 dòng)
- API reference đầy đủ
- Ví dụ sử dụng thực tế
- Troubleshooting guide
- Thông số kỹ thuật chi tiết

#### `docs/DATA_LOGGING.md`
- **Hướng dẫn CSV logging** (104 dòng)
- Cấu trúc file CSV
- Quản lý dữ liệu
- Phân tích dữ liệu

### 📊 Dữ liệu (`data/`)

#### `data/csv_logs/`
- **File CSV logs** cho từng cảm biến
- Tên file dựa trên cổng serial
- Cấu trúc: `pzem__{port_name}.csv`
- Dữ liệu với timestamp và tất cả thông số đo

### 🛠️ Quản lý dự án

#### `Makefile`
- **Quản lý dự án** (74 dòng)
- Các lệnh cài đặt, test, lint, format
- Chạy các công cụ chính
- Documentation generation

#### `requirements.txt`
- **Dependencies** (4 dòng)
- pyserial: Giao tiếp serial
- tabulate: Hiển thị bảng
- pandas: Xử lý dữ liệu

### 📝 Tài liệu dự án

#### `README.md`
- **Tài liệu chính** (405 dòng)
- Tổng quan dự án
- Hướng dẫn cài đặt và sử dụng
- Tính năng chi tiết
- Troubleshooting

#### `CHANGELOG.md`
- **Lịch sử thay đổi** (67 dòng)
- Theo format Keep a Changelog
- Semantic Versioning
- Chi tiết các thay đổi qua các phiên bản

#### `LICENSE`
- **Giấy phép MIT** (22 dòng)
- Điều khoản sử dụng và phân phối

## Tính năng chính

### Thư viện PZEM-004T
- ✅ Đọc đầy đủ dữ liệu: Voltage, Current, Power, Energy, Frequency, Power Factor
- ✅ Thông số kỹ thuật chính xác: Theo tài liệu PZEM-004T với độ chính xác ±0.5%
- ✅ Cấu hình thiết bị: Set/Get power alarm threshold, change device address
- ✅ Điều khiển: Reset energy counter, calibration (factory use)
- ✅ Xử lý lỗi: CRC validation, Modbus error handling, retry mechanism
- ✅ Cache thông minh: Tối ưu hiệu suất với cache dữ liệu
- ✅ API linh hoạt: Đọc từng giá trị hoặc tất cả cùng lúc
- ✅ Quy tắc hiển thị: Tuân thủ datasheet cho công suất và năng lượng

### Công cụ hỗ trợ
- ✅ Tool reset energy: Menu tương tác, xác nhận an toàn, báo cáo chi tiết
- ✅ Hỗ trợ đa adapter: PL2303, CH340, CP210, FTDI
- ✅ Giao diện thân thiện: Emoji, màu sắc, thông báo rõ ràng
- ✅ Bảo mật cao: Nhiều cấp xác nhận để tránh reset nhầm

### Ứng dụng giám sát đa cảm biến
- ✅ Tự động phát hiện cảm biến: Quét và kết nối tự động với các thiết bị PZEM-004T
- ✅ Đa cảm biến: Hỗ trợ đọc từ nhiều cảm biến cùng lúc
- ✅ Hiển thị dạng bảng: Dữ liệu từ tất cả cảm biến hiển thị trong bảng thống nhất
- ✅ Thông tin tổng hợp: Tính tổng công suất và năng lượng của tất cả cảm biến
- ✅ Cơ chế retry: Tự động thử lại khi gặp lỗi kết nối
- ✅ Hỗ trợ adapter mở rộng: PL2303, CH340, CP210, FTDI
- ✅ Cấu trúc code tối ưu: Tách logic chính, dễ bảo trì và mở rộng

### Ghi dữ liệu CSV
- 📝 File CSV riêng biệt: Mỗi cảm biến có file CSV riêng với tên dựa trên cổng
- 🕐 Timestamp chính xác: Ghi thời gian đo với định dạng YYYY-MM-DD HH:MM:SS
- 📊 Dữ liệu đầy đủ: Ghi tất cả thông số bao gồm datetime, port và các giá trị đo
- 🗂️ Tổ chức khoa học: Dữ liệu được lưu trong thư mục `data/csv_logs/`

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

**Lưu ý**: Cấu trúc này được cập nhật lần cuối vào tháng 8/2025 và phản ánh trạng thái hiện tại của dự án. 