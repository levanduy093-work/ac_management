# PZEM Data Logging System

## Cấu trúc thư mục
```
ac_management/
├── src/                       # Thư viện chính
│   ├── __init__.py
│   ├── pzem.py               # Thư viện PZEM-004T
│   └── database.py           # Database module
├── tools/                     # Công cụ ứng dụng
│   ├── __init__.py
│   ├── read_ac_sensor.py     # Script giám sát đa cảm biến (CSV)
│   ├── read_ac_sensor_db.py  # Script giám sát đa cảm biến (Database)
│   ├── query_database.py     # Tool truy vấn database
│   ├── database_gui.py       # GUI tool tương tác
│   └── reset_energy_no_address_change.py # Tool reset energy AN TOÀN
├── docs/                      # Tài liệu
│   ├── PZEM004T.md           # Hướng dẫn thư viện
│   ├── DATA_LOGGING.md       # File này
│   └── DATABASE.md           # Hướng dẫn database storage
├── data/                      # Dữ liệu
│   ├── csv_logs/             # File CSV logs
│   ├── json_log/             # File JSON logs
│   └── pzem_data.db          # SQLite database
├── requirements.txt           # Dependencies
├── Makefile                   # Quản lý dự án
└── README.md                  # Tài liệu chính
```

## Tính năng ghi dữ liệu

### 1. CSV Storage (Legacy)
- **File CSV riêng biệt cho mỗi cổng**
- Mỗi cổng PZEM sẽ có file CSV riêng
- Tên file dựa trên tên cổng: `pzem_{port_name}.csv`
- Ví dụ: `/dev/ttyUSB0` → `pzem_dev_ttyUSB0.csv`

### 2. Database Storage (Khuyến nghị)
- **SQLite database** với hiệu suất cao
- Tự động quản lý sensors và measurements
- Truy vấn nhanh với indexes
- Tự động dọn dẹp dữ liệu cũ
- Backup dễ dàng (chỉ 1 file)

## Cấu trúc dữ liệu

### CSV Format
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

### Database Schema
```sql
-- Bảng sensors
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    port TEXT UNIQUE NOT NULL,
    device_address INTEGER DEFAULT 248,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_readings INTEGER DEFAULT 0
);

-- Bảng measurements
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    voltage REAL,
    current REAL,
    power REAL,
    energy REAL,
    frequency REAL,
    power_factor REAL,
    alarm_status BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id)
);
```

## Cách sử dụng

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy chương trình

#### CSV Storage (Legacy)
```bash
python tools/read_ac_sensor.py
# hoặc
make run-monitor
```

#### Database Storage (Khuyến nghị)
```bash
python tools/read_ac_sensor_db.py
# hoặc
make run-monitor-db

# Chạy full stack (monitor + web)
make run-server
```

### 3. Xem dữ liệu

#### CSV Files
```bash
# Xem file CSV
cat data/csv_logs/pzem__dev_ttyUSB0.csv

# Hoặc sử dụng pandas để phân tích
python -c "import pandas as pd; df = pd.read_csv('data/csv_logs/pzem__dev_ttyUSB0.csv'); print(df.tail())"
```

#### Database
```bash
# GUI Tool (khuyến nghị)
make db-gui

# Command line
make db-stats
make db-sensors
make db-latest
```

## Quản lý dữ liệu

### 1. Backup dữ liệu

#### CSV Files
```bash
# Tạo backup toàn bộ thư mục data
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/
```

#### Database
```bash
# Backup database
cp data/pzem_data.db backup_pzem_data_$(date +%Y%m%d_%H%M%S).db
```

### 2. Xuất dữ liệu

#### Command Line
```bash
# Xuất ra CSV
python tools/query_database.py --export-csv export.csv --days 7

# Xuất ra JSON
python tools/query_database.py --export-json export.json --days 30

# Xuất theo port riêng biệt
python tools/query_database.py --export-csv-separate --days 7
```

#### GUI Tool
```bash
make db-gui
```

### 3. Phân tích dữ liệu
```python
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu CSV
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

### 4. Dọn dẹp dữ liệu cũ

#### CSV Files
```bash
# Xóa dữ liệu cũ hơn 30 ngày
find data/csv_logs/ -name "*.csv" -mtime +30 -delete
```

#### Database
```bash
# Dọn dẹp dữ liệu cũ hơn 30 ngày
make db-cleanup

# Hoặc chỉ định số ngày
python tools/query_database.py --cleanup 60
```

## Lưu ý quan trọng

1. **Dung lượng ổ cứng**: 
   - CSV: Mỗi sensor ghi ~1KB/giờ
   - Database: Hiệu quả hơn cho dữ liệu lớn
2. **Backup định kỳ**: Nên backup dữ liệu hàng tuần
3. **Quyền truy cập**: Đảm bảo chương trình có quyền ghi vào thư mục `data/`
4. **Đồng bộ thời gian**: Kiểm tra đồng hồ hệ thống để đảm bảo timestamp chính xác
5. **Khuyến nghị**: Sử dụng Database storage thay vì CSV cho dự án mới

## Migration từ CSV sang Database

Nếu bạn đang sử dụng CSV và muốn chuyển sang Database:

1. **Chạy monitoring với Database**:
   ```bash
   make run-monitor-db
   ```

2. **Dữ liệu mới sẽ được lưu vào database**

3. **Dữ liệu CSV cũ vẫn được giữ nguyên** để tham khảo

4. **Sử dụng GUI tool** để quản lý database:
   ```bash
   make db-gui
   ```
