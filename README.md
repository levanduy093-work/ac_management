# 🔌 AC Management - PZEM-004T Power Monitoring & Data Logger

Một hệ thống Python chuyên nghiệp để giám sát và ghi dữ liệu từ cảm biến công suất điện PZEM-004T sử dụng giao thức Modbus-RTU. Dự án bao gồm thư viện hoàn chỉnh, ứng dụng giám sát đa cảm biến và các công cụ hỗ trợ.

## 🆕 Cập nhật mới - Thư viện PZEM-004T hoàn chỉnh

### ✨ Tính năng mới trong thư viện

- **Thư viện hoàn chỉnh**: Triển khai đầy đủ giao thức Modbus-RTU theo tài liệu kỹ thuật
- **API đầy đủ**: Hỗ trợ tất cả function codes và register mapping
- **Xử lý lỗi toàn diện**: CRC validation, error handling, retry mechanism
- **Cache thông minh**: Tối ưu hiệu suất với cache dữ liệu
- **Tương thích ngược**: Hỗ trợ cả tên class cũ và mới

### 🔄 Cập nhật ứng dụng giám sát

- **Sử dụng thư viện mới**: `read_ac_sensor.py` đã được cập nhật để sử dụng thư viện PZEM-004T mới
- **Hiệu suất tốt hơn**: Sử dụng API `get_all_measurements()` thay vì `update_values()`
- **Hỗ trợ adapter mở rộng**: Thêm hỗ trợ CP210, FTDI ngoài PL2303, CH340
- **Cấu trúc code cải thiện**: Tách logic chính vào hàm `main()` để dễ bảo trì

### 📚 Tài liệu chi tiết

- **[PZEM004T.md](PZEM004T.md)**: Hướng dẫn chi tiết thư viện PZEM-004T
- **[example_usage.py](example_usage.py)**: 6 ví dụ sử dụng thực tế
- **[pzem.py](pzem.py)**: Thư viện chính hoàn chỉnh

## 📊 Thông số giám sát

Script sẽ đọc và hiển thị các thông số điện quan trọng từ mỗi cảm biến:

| Thông số | Đơn vị | Dải đo | Độ chính xác |
|----------|---------|--------|--------------|
| **Voltage** | V | 80-260V | ±0.5% |
| **Current** | A | 0-10A (10A) / 0-100A (100A) | ±0.5% |
| **Power** | W | 0-2.3kW (10A) / 0-23kW (100A) | ±0.5% |
| **Energy** | kWh | 0-9999.99kWh | ±0.5% |
| **Frequency** | Hz | 45-65Hz | ±0.5% |
| **Power Factor** | - | 0.00-1.00 | ±1% |
| **Alarm** | ON/OFF | Power threshold | - |

## 🎯 Tính năng chính

### Thư viện PZEM-004T
- ✅ **Đọc đầy đủ dữ liệu**: Voltage, Current, Power, Energy, Frequency, Power Factor
- ✅ **Cấu hình thiết bị**: Set/Get power alarm threshold, change device address
- ✅ **Điều khiển**: Reset energy counter, calibration (factory use)
- ✅ **Xử lý lỗi**: CRC validation, Modbus error handling, retry mechanism
- ✅ **Cache thông minh**: Tối ưu hiệu suất với cache dữ liệu
- ✅ **API linh hoạt**: Đọc từng giá trị hoặc tất cả cùng lúc

### Công cụ hỗ trợ
- ✅ **Tool reset energy**: Menu tương tác, xác nhận an toàn, báo cáo chi tiết
- ✅ **Hỗ trợ đa adapter**: PL2303, CH340, CP210, FTDI
- ✅ **Giao diện thân thiện**: Emoji, màu sắc, thông báo rõ ràng
- ✅ **Bảo mật cao**: Nhiều cấp xác nhận để tránh reset nhầm

### Ứng dụng giám sát đa cảm biến
- ✅ **Tự động phát hiện cảm biến**: Quét và kết nối tự động với các thiết bị PZEM-004T
- ✅ **Đa cảm biến**: Hỗ trợ đọc từ nhiều cảm biến cùng lúc
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

## 🗂️ Cấu trúc dự án

```
ac_management/
├── 📜 pzem.py                 # Thư viện PZEM-004T hoàn chỉnh
├── 📜 read_ac_sensor.py       # Script giám sát đa cảm biến
├── 📜 example_usage.py        # 6 ví dụ sử dụng thư viện
├── 📜 reset_energy.py         # Tool reset energy counter (đã cập nhật)
├── 📋 requirements.txt        # Dependencies
├── 📖 README.md              # Tài liệu này
├── 📖 PZEM004T.md            # Hướng dẫn chi tiết thư viện
├── 📝 DATA_LOGGING.md        # Hướng dẫn CSV logging
└── 📁 data/                  # Thư mục dữ liệu
    └── 📁 csv_logs/          # File CSV logs
        ├── 📊 pzem__dev_ttyUSB0.csv
        ├── 📊 pzem__dev_ttyUSB1.csv
        └── 📊 pzem__dev_ttyUSB2.csv
```

## 🔧 Yêu cầu phần cứng

### Cảm biến được hỗ trợ
- **PZEM-004T-10A**: Dải đo 0-10A (shunt tích hợp)
- **PZEM-004T-100A**: Dải đo 0-100A (CT ngoài)

### Bộ chuyển đổi USB-to-Serial được hỗ trợ
- **PL2303** (Prolific) - Hỗ trợ đầy đủ
- **CH340/CH341** (WCH) - Hỗ trợ đầy đủ
- **CP2102/CP2104** (Silicon Labs) - Hỗ trợ đầy đủ
- **FT232R** (FTDI) - Hỗ trợ đầy đủ

### Sơ đồ kết nối
```
PZEM-004T Module:
┌─────────────────┐
│   TTL Interface │
├─────────────────┤
│ GND │ TX │ RX │ 5V │
└─────┴────┴────┴────┘
         │
         ▼
┌─────────────────┐
│ TTL to USB Cable│
└─────────────────┘
         │
         ▼
┌─────────────────┐
│      PC/USB     │
└─────────────────┘
```

**Lưu ý quan trọng**: TTL Interface là thụ động, cần nguồn 5V ngoài. Tất cả 4 chân phải được kết nối: GND, TX, RX, 5V.

## 📦 Cài đặt và thiết lập

### Bước 1: Clone repository
```bash
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
```

### Bước 2: Cài đặt dependencies
```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 3: Cấp quyền truy cập Serial (Linux)
```bash
# Thêm user vào group dialout
sudo usermod -a -G dialout $USER

# Hoặc cấp quyền cho thiết bị cụ thể
sudo chmod 666 /dev/ttyUSB*
```

## 🚀 Sử dụng

### 1. Sử dụng thư viện PZEM-004T

#### Cách sử dụng cơ bản
```python
from pzem import PZEM004T

# Khởi tạo kết nối
pzem = PZEM004T(port='/dev/ttyUSB0')

# Đọc dữ liệu
voltage = pzem.get_voltage()      # V
current = pzem.get_current()      # A
power = pzem.get_power()          # W
energy = pzem.get_energy()        # kWh

# In tất cả giá trị
pzem.print_measurements()

# Đóng kết nối
pzem.close()
```

#### Chạy ví dụ
```bash
python3 example_usage.py
```

### 2. Giám sát đa cảm biến (Đã cập nhật)
```bash
python3 read_ac_sensor.py
```

**Tính năng mới:**
- Sử dụng thư viện PZEM-004T mới với hiệu suất tốt hơn
- Hỗ trợ nhiều loại USB-to-Serial adapter
- Cấu trúc code tối ưu và dễ bảo trì

### 3. Reset energy counter (Đã cập nhật)
```bash
python3 reset_energy.py
```

**Tính năng mới:**
- Menu tương tác với 5 tùy chọn
- Hiển thị thông tin thiết bị trước khi reset
- Xác nhận an toàn nhiều cấp
- Báo cáo kết quả chi tiết
- Hỗ trợ nhiều loại USB-to-Serial adapter

## 📱 Giao diện và Output

### Thư viện PZEM-004T
```
=== PZEM-004T Measurements ===
Voltage:       225.4 V
Current:         0.830 A
Power:         185.2 W
Energy:          1.547 kWh
Frequency:      50.0 Hz
Power Factor:    0.98
Alarm Status:   OFF
================================
```

### Ứng dụng đa cảm biến
```
=== PZEM Sensors Data - 2025-08-04 10:30:15 ===
Found 3 active sensor(s)

┌─────────────────┬──────────────┬──────────────┬───────────┬──────────────┬─────────────────┬──────────────┬───────┐
│ Port            │ Voltage (V)  │ Current (A)  │ Power (W) │ Energy (Wh)  │ Frequency (Hz)  │ Power Factor │ Alarm │
├─────────────────┼──────────────┼──────────────┼───────────┼──────────────┼─────────────────┼──────────────┼───────┤
│ /dev/ttyUSB0    │ 225.4        │ 0.830        │ 185.2     │ 1547         │ 50.0            │ 0.98         │ OFF   │
│ /dev/ttyUSB1    │ 226.1        │ 2.150        │ 485.6     │ 3842         │ 50.0            │ 0.97         │ OFF   │
│ /dev/ttyUSB2    │ 224.8        │ 1.240        │ 278.3     │ 2156         │ 50.1            │ 0.99         │ OFF   │
└─────────────────┴──────────────┴──────────────┴───────────┴──────────────┴─────────────────┴──────────────┴───────┘

=== Summary ===
Total Power: 949.1 W
Total Energy: 7545 Wh
```

### Tool reset energy
```
🔌 PZEM-004T Energy Reset Tool
========================================

📋 Menu:
1. Reset tất cả thiết bị (có xác nhận)
2. Reset tất cả thiết bị (không xác nhận)
3. Reset từng thiết bị (xác nhận từng cái)
4. Quét lại thiết bị
5. Thoát

Thông tin thiết bị /dev/ttyUSB0:
  Địa chỉ: 248
  Năng lượng hiện tại: 1.547 kWh
  Công suất: 185.2 W
  Điện áp: 225.4 V
  Dòng điện: 0.830 A

✅ Đã reset thành công bộ đếm năng lượng trên /dev/ttyUSB0
   Năng lượng sau reset: 0.000 kWh

📋 Tóm tắt kết quả:
   Tổng thiết bị: 3
   Reset thành công: 3
   Reset thất bại: 0
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

## 📚 Tài liệu tham khảo

- **[PZEM004T.md](PZEM004T.md)**: Hướng dẫn chi tiết thư viện
- **[example_usage.py](example_usage.py)**: 6 ví dụ sử dụng thực tế
- **[DATA_LOGGING.md](DATA_LOGGING.md)**: Hướng dẫn CSV logging

## 🤝 Đóng góp và phát triển

### Cấu trúc code
- `pzem.py`: Thư viện PZEM-004T hoàn chỉnh
- `read_ac_sensor.py`: Ứng dụng giám sát đa cảm biến (đã cập nhật)
- `example_usage.py`: Ví dụ sử dụng thư viện
- `reset_energy.py`: Tool reset energy counter (đã cập nhật)

### Các thay đổi chính trong read_ac_sensor.py
- **Import thư viện mới**: Sử dụng `PZEM004T` thay vì `PZEM004Tv30`
- **API cải thiện**: Sử dụng `get_all_measurements()` thay vì `update_values()`
- **Hỗ trợ adapter mở rộng**: Thêm CP210, FTDI ngoài PL2303, CH340
- **Cấu trúc code**: Tách logic chính vào hàm `main()` để dễ bảo trì
- **Xử lý lỗi**: Cải thiện error handling và retry mechanism

### Các thay đổi chính trong reset_energy.py
- **Menu tương tác**: 5 tùy chọn với giao diện thân thiện
- **Hiển thị thông tin**: Địa chỉ, năng lượng, công suất trước khi reset
- **Xác nhận an toàn**: Nhiều cấp xác nhận để tránh reset nhầm
- **Báo cáo chi tiết**: Tóm tắt kết quả reset với số liệu cụ thể
- **Hỗ trợ adapter mở rộng**: PL2303, CH340, CP210, FTDI

### Đóng góp
1. Fork repository này
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

### Roadmap
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

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ và hỗ trợ

- **Developer**: Lê Văn Duy
- **Email**: levanduy093.work@gmail.com  
- **GitHub**: [@levanduy093-work](https://github.com/levanduy093-work)
- **Repository**: [ac_management](https://github.com/levanduy093-work/ac_management)

### Báo lỗi (Bug Reports)
Nếu bạn gặp lỗi, vui lòng tạo [GitHub Issue](https://github.com/levanduy093-work/ac_management/issues) với thông tin:
- OS và phiên bản Python
- Model PZEM-004T và USB-to-Serial adapter
- Log lỗi chi tiết
- Các bước tái tạo lỗi
- Phiên bản thư viện đang sử dụng (cũ hay mới)

### Feature Requests
Có ý tưởng tính năng mới? Tạo [GitHub Issue](https://github.com/levanduy093-work/ac_management/issues) với label `enhancement`.

---

**⭐ Nếu dự án này hữu ích, đừng quên star repository để ủng hộ developer! ⭐**