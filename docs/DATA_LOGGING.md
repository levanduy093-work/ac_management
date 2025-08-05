# PZEM Data Logging System

## Cấu trúc thư mục
```
ac_management/
├── src/                       # Thư viện chính
│   ├── __init__.py
│   └── pzem.py               # Thư viện PZEM-004T
├── tools/                     # Công cụ ứng dụng
│   ├── __init__.py
│   ├── read_ac_sensor.py     # Script giám sát đa cảm biến
│   └── reset_energy.py       # Tool reset energy
├── docs/                      # Tài liệu
│   ├── PZEM004T.md           # Hướng dẫn thư viện
│   └── DATA_LOGGING.md       # File này
├── data/                      # Dữ liệu
│   └── csv_logs/             # File CSV logs
│       ├── pzem__dev_ttyUSB0.csv
│       ├── pzem__dev_ttyUSB1.csv
│       └── pzem__dev_ttyUSB2.csv
├── requirements.txt           # Dependencies
├── Makefile                   # Quản lý dự án
└── README.md                  # Tài liệu chính
```

## Tính năng ghi dữ liệu CSV

### 1. File CSV riêng biệt cho mỗi cổng
- Mỗi cổng PZEM sẽ có file CSV riêng
- Tên file dựa trên tên cổng: `pzem_{port_name}.csv`
- Ví dụ: `/dev/ttyUSB0` → `pzem_dev_ttyUSB0.csv`

### 2. Cấu trúc dữ liệu CSV
| Cột | Mô tả | Đơn vị |
|-----|-------|--------|
| datetime | Thời gian đo | YYYY-MM-DD HH:MM:SS |
| port | Tên cổng | String |
| voltage_v | Điện áp | V |
| current_a | Dòng điện | A |
| power_w | Công suất | W |
| energy_wh | Năng lượng | Wh |
| frequency_hz | Tần số | Hz |
| power_factor | Hệ số công suất | - |
| alarm_status | Trạng thái báo động | ON/OFF |

### 3. Tự động tạo header
- File CSV tự động được tạo với header khi lần đầu ghi dữ liệu
- Nếu file đã tồn tại, chương trình sẽ kiểm tra và cập nhật header nếu cần

### 4. Thông tin CSV trong giao diện
- Hiển thị số lượng bản ghi đã lưu
- Hiển thị kích thước file
- Cập nhật real-time

## Cách sử dụng

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy chương trình
```bash
python tools/read_ac_sensor.py
```

### 3. Xem dữ liệu CSV
```bash
# Xem file CSV
cat data/csv_logs/pzem__dev_ttyUSB0.csv

# Hoặc sử dụng pandas để phân tích
python -c "import pandas as pd; df = pd.read_csv('data/csv_logs/pzem__dev_ttyUSB0.csv'); print(df.tail())"
```

## Quản lý dữ liệu

### 1. Backup dữ liệu
```bash
# Tạo backup toàn bộ thư mục data
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/
```

### 2. Phân tích dữ liệu
```python
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu
df = pd.read_csv('data/csv_logs/pzem__dev_ttyUSB0.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

# Vẽ biểu đồ công suất theo thời gian
plt.figure(figsize=(12, 6))
plt.plot(df['datetime'], df['power_w'])
plt.title('Power Consumption Over Time')
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.show()
```

### 3. Dọn dẹp dữ liệu cũ
```bash
# Xóa dữ liệu cũ hơn 30 ngày
find data/csv_logs/ -name "*.csv" -mtime +30 -delete
```

## Lưu ý quan trọng

1. **Dung lượng ổ cứng**: Mỗi sensor ghi ~1KB/giờ, theo dõi dung lượng định kỳ
2. **Backup định kỳ**: Nên backup dữ liệu hàng tuần
3. **Quyền truy cập**: Đảm bảo chương trình có quyền ghi vào thư mục `data/`
4. **Đồng bộ thời gian**: Kiểm tra đồng hồ hệ thống để đảm bảo timestamp chính xác
