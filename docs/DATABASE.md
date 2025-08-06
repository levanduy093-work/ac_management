# 📊 Database Storage Guide

Hướng dẫn sử dụng SQLite database để lưu trữ dữ liệu PZEM-004T thay vì file CSV.

## 🎯 Tổng quan

Dự án đã được mở rộng để hỗ trợ lưu trữ dữ liệu trong SQLite database thay vì file CSV. Điều này mang lại nhiều lợi ích:

### ✅ Ưu điểm của Database

- **Hiệu suất tốt hơn**: Truy vấn nhanh với indexes
- **Quản lý dữ liệu tốt hơn**: Không bị phân mảnh như CSV
- **Truy vấn linh hoạt**: SQL queries mạnh mẽ
- **Tự động dọn dẹp**: Xóa dữ liệu cũ tự động
- **Thống kê chi tiết**: Theo dõi sensors và measurements
- **Backup dễ dàng**: Chỉ cần copy 1 file database

### 📁 Cấu trúc Database

Database SQLite được lưu tại `data/pzem_data.db` với 2 bảng chính:

#### Bảng `sensors`
```sql
CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    port TEXT UNIQUE NOT NULL,
    device_address INTEGER DEFAULT 248,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_readings INTEGER DEFAULT 0
);
```

#### Bảng `measurements`
```sql
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

## 🚀 Sử dụng Database

### 1. Chạy giám sát với Database

```bash
# Sử dụng Makefile
make run-monitor-db

# Hoặc chạy trực tiếp
python tools/read_ac_sensor_db.py
```

### 2. Xem thống kê Database

```bash
# Xem thống kê tổng quan
make db-stats

# Xem thông tin sensors
make db-sensors

# Xem 20 measurements gần nhất
make db-latest
```

### 3. Dọn dẹp dữ liệu cũ

```bash
# Xóa dữ liệu cũ hơn 30 ngày
make db-cleanup

# Hoặc chỉ định số ngày
python tools/query_database.py --cleanup 60
```

## 🔧 Tool Truy vấn Database

### 🆕 GUI Tool tương tác (Khuyến nghị)

Để dễ dàng truy vấn database mà không cần nhớ command line options:

```bash
# Chạy GUI tool
make db-gui

# Hoặc chạy trực tiếp
python tools/database_gui.py
```

GUI tool cung cấp menu tương tác với các tính năng:
- 📊 Xem thống kê database
- 🔌 Xem thông tin sensors
- 📈 Xem measurements gần nhất
- 📁 Xuất dữ liệu (CSV/JSON)
- 🗑️ Dọn dẹp dữ liệu cũ
- 🔍 Truy vấn nâng cao (theo port, date range, statistics)

### Command Line Tool

#### Cú pháp cơ bản

```bash
python tools/query_database.py [OPTIONS]
```

### Các tùy chọn chính

| Tùy chọn | Mô tả |
|----------|-------|
| `--stats` | Hiển thị thống kê database |
| `--sensors` | Hiển thị thông tin sensors |
| `--latest N` | Hiển thị N measurements gần nhất |
| `--export-csv FILE` | Xuất dữ liệu ra file CSV |
| `--export-json FILE` | Xuất dữ liệu ra file JSON |
| `--port PORT` | Lọc theo port cụ thể |
| `--days N` | Lọc dữ liệu N ngày gần đây |
| `--limit N` | Giới hạn số records xuất |
| `--cleanup N` | Xóa dữ liệu cũ hơn N ngày |

### Ví dụ sử dụng

#### 1. Xem thống kê database
```bash
python tools/query_database.py --stats
```

Output:
```
💾 Connected to database: data/pzem_data.db

📊 Database Statistics:
========================================
📁 Database Size: 2.45 MB
📊 Total Measurements: 12,345
🔌 Total Sensors: 3
📅 Oldest Measurement: 2025-01-01 10:00:00
📅 Newest Measurement: 2025-01-15 15:30:00
⏱️  Data Span: 14 days, 5 hours
```

#### 2. Xem thông tin sensors
```bash
python tools/query_database.py --sensors
```

Output:
```
📊 Sensor Summary:
================================================================================
🔌 Port: /dev/ttyUSB0
   📍 Device Address: 0xF8 (248)
   📅 First Seen: 2025-01-01 10:00:00
   📅 Last Seen: 2025-01-15 15:30:00
   📊 Total Readings: 4,123
   📊 Total Measurements: 4,123
   📅 Last Measurement: 2025-01-15 15:30:00
----------------------------------------
🔌 Port: /dev/ttyUSB1
   📍 Device Address: 0xF8 (248)
   📅 First Seen: 2025-01-01 10:00:00
   📅 Last Seen: 2025-01-15 15:30:00
   📊 Total Readings: 4,123
   📊 Total Measurements: 4,123
   📅 Last Measurement: 2025-01-15 15:30:00
----------------------------------------
```

#### 3. Xuất dữ liệu ra CSV
```bash
# Xuất tất cả dữ liệu
python tools/query_database.py --export-csv all_data.csv

# Xuất dữ liệu 7 ngày gần đây
python tools/query_database.py --export-csv recent_data.csv --days 7

# Xuất dữ liệu từ sensor cụ thể
python tools/query_database.py --export-csv sensor1_data.csv --port /dev/ttyUSB0

# Xuất 1000 records gần nhất
python tools/query_database.py --export-csv latest_1000.csv --limit 1000
```

#### 4. Xuất dữ liệu ra JSON
```bash
# Xuất dữ liệu ra JSON
python tools/query_database.py --export-json data.json --days 30
```

#### 5. Dọn dẹp dữ liệu cũ
```bash
# Xóa dữ liệu cũ hơn 30 ngày
python tools/query_database.py --cleanup 30

# Xóa dữ liệu cũ hơn 60 ngày
python tools/query_database.py --cleanup 60
```

## 📊 So sánh CSV vs Database

| Tính năng | CSV | Database |
|-----------|-----|----------|
| **Hiệu suất** | Chậm với file lớn | Nhanh với indexes |
| **Truy vấn** | Không hỗ trợ | SQL queries mạnh mẽ |
| **Quản lý** | Phân mảnh | Tự động tối ưu |
| **Backup** | Nhiều file | 1 file duy nhất |
| **Thống kê** | Không có | Chi tiết |
| **Dọn dẹp** | Thủ công | Tự động |
| **Độ phức tạp** | Đơn giản | Phức tạp hơn |

## 🔄 Chuyển đổi từ CSV sang Database

Nếu bạn đã có dữ liệu CSV và muốn chuyển sang database:

### 1. Tạo script chuyển đổi

```python
import pandas as pd
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import PZEMDatabase

def migrate_csv_to_db(csv_file, db):
    """Migrate CSV data to database"""
    df = pd.read_csv(csv_file)
    
    for _, row in df.iterrows():
        sensor_data = {
            'port': row['port'],
            'voltage': float(row['voltage_v']),
            'current': float(row['current_a']),
            'power': float(row['power_w']),
            'energy': float(row['energy_wh']),
            'frequency': float(row['frequency_hz']),
            'power_factor': float(row['power_factor']),
            'alarm': row['alarm_status'] == 'ON',
            'timestamp': datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
        }
        
        db.save_measurement(sensor_data)
    
    print(f"Migrated {len(df)} records from {csv_file}")

# Usage
db = PZEMDatabase()
migrate_csv_to_db('data/csv_logs/pzem__dev_ttyUSB0.csv', db)
```

### 2. Chạy chuyển đổi

```bash
python migrate_csv_to_db.py
```

## 🛠️ Quản lý Database

### Backup Database

```bash
# Backup database
cp data/pzem_data.db data/pzem_data_backup_$(date +%Y%m%d_%H%M%S).db

# Hoặc sử dụng sqlite3
sqlite3 data/pzem_data.db ".backup data/pzem_data_backup.db"
```

### Restore Database

```bash
# Restore từ backup
cp data/pzem_data_backup.db data/pzem_data.db
```

### Kiểm tra Database

```bash
# Kiểm tra integrity
sqlite3 data/pzem_data.db "PRAGMA integrity_check;"

# Xem schema
sqlite3 data/pzem_data.db ".schema"

# Truy vấn trực tiếp
sqlite3 data/pzem_data.db "SELECT COUNT(*) FROM measurements;"
```

## 📈 Monitoring và Maintenance

### 1. Theo dõi kích thước database

```bash
# Xem kích thước database
ls -lh data/pzem_data.db

# Xem thống kê
make db-stats
```

### 2. Tự động dọn dẹp

Tạo cron job để tự động dọn dẹp:

```bash
# Thêm vào crontab (dọn dẹp hàng tuần)
0 2 * * 0 cd /path/to/ac_management && python tools/query_database.py --cleanup 30
```

### 3. Monitoring script

```bash
#!/bin/bash
# monitor_db.sh

DB_SIZE=$(du -m data/pzem_data.db | cut -f1)
if [ $DB_SIZE -gt 100 ]; then
    echo "Database size is ${DB_SIZE}MB, cleaning up old data..."
    python tools/query_database.py --cleanup 30
fi
```

## 🚨 Troubleshooting

### Lỗi thường gặp

#### 1. "Database is locked"
```bash
# Kiểm tra xem có process nào đang sử dụng database không
lsof data/pzem_data.db

# Restart monitoring script
pkill -f read_ac_sensor_db.py
```

#### 2. "No such table"
```bash
# Recreate database
rm data/pzem_data.db
python tools/read_ac_sensor_db.py
```

#### 3. "Permission denied"
```bash
# Cấp quyền cho thư mục data
chmod 755 data/
chmod 644 data/pzem_data.db
```

### Log và Debug

```bash
# Xem log của monitoring script
python tools/read_ac_sensor_db.py 2>&1 | tee monitor.log

# Debug database operations
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from src.database import PZEMDatabase
db = PZEMDatabase()
print(db.get_database_stats())
"
```

## 📚 Tài liệu tham khảo

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Database Schema](src/database.py)

---

**Lưu ý**: Database storage cung cấp hiệu suất và tính năng tốt hơn so với CSV, nhưng cũng phức tạp hơn. Nếu bạn chỉ cần lưu trữ đơn giản, CSV vẫn là lựa chọn tốt. 