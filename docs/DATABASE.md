# 📊 Database Management Guide

Comprehensive guide cho SQLite database system của PZEM-004T, bao gồm CLI tools, GUI management, và web dashboard integration.

## 🎯 Tổng quan

Dự án đã được mở rộng để hỗ trợ lưu trữ dữ liệu trong SQLite database thay vì file CSV. Điều này mang lại nhiều lợi ích:

### ✅ Database System Advantages

- **🚀 Performance**: Optimized queries với indexes, faster than CSV
- **🎯 Modern Access**: Web dashboard, CLI tools, GUI management  
- **🔧 Auto-Management**: Self-cleanup, maintenance, optimization
- **📊 Rich Analytics**: Statistics, trends, monitoring dashboards
- **💾 Single File**: Easy backup, deployment, migration
- **📱 API Ready**: REST endpoints cho mobile integration
- **🔄 Real-time**: WebSocket updates, live monitoring

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

## 🚀 Database Access Methods

### 🌐 Method 1: Web Dashboard (Recommended) ⭐

```bash
# Start data collection + web dashboard
make run-monitor-db  # Terminal 1
make run-web         # Terminal 2

# Access: http://localhost:8000
# Features: Real-time monitoring, export, system management
```

**Web Dashboard provides:**
- 📊 **Live monitoring** với interactive charts
- 📁 **Advanced export** với filtering options  
- ⚙️ **System management** với health monitoring
- 📱 **Mobile-ready** API và responsive UI

### 🖥️ Method 2: GUI Tool (Desktop)

```bash
# Interactive database management
make db-gui
```

**GUI Tool features:**
- 📋 **Menu-driven interface** không cần commands
- 📊 **Database statistics** và sensor summary
- 📁 **Export functionality** với overwrite options  
- 🔍 **Advanced queries** và cleanup tools

### ⌨️ Method 3: Command Line (Automation)

```bash
# Database monitoring
make run-monitor-db

# Statistics và management  
make db-stats     # Database statistics
make db-sensors   # Sensor information
make db-latest    # Latest measurements
make db-cleanup   # Data cleanup
```

### 📱 Method 4: API Access (Mobile Development)

```bash
# RESTful API endpoints
curl http://localhost:8000/api/measurements
curl http://localhost:8000/api/sensors
curl http://localhost:8000/api/stats

# WebSocket real-time updates  
ws://localhost:8000/ws/realtime
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
- 📁 Xuất dữ liệu (CSV/JSON - file đơn hoặc theo port riêng biệt)
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
# Xuất tất cả dữ liệu (file đơn)
python tools/query_database.py --export-csv all_data.csv

# Xuất dữ liệu 7 ngày gần đây (file đơn)
python tools/query_database.py --export-csv recent_data.csv --days 7

# Xuất dữ liệu từ sensor cụ thể (file đơn)
python tools/query_database.py --export-csv sensor1_data.csv --port /dev/ttyUSB0

# 🆕 Xuất dữ liệu theo port riêng biệt (nhiều file)
python tools/query_database.py --export-csv-separate --days 7
```

#### 4. Xuất dữ liệu ra JSON
```bash
# Xuất dữ liệu ra JSON (file đơn)
python tools/query_database.py --export-json data.json --days 30

# 🆕 Xuất dữ liệu theo port riêng biệt (nhiều file)
python tools/query_database.py --export-json-separate --days 30
```

#### 5. Dọn dẹp dữ liệu cũ
```bash
# Xóa dữ liệu cũ hơn 30 ngày
python tools/query_database.py --cleanup 30

# Xóa dữ liệu cũ hơn 60 ngày
python tools/query_database.py --cleanup 60
```

## 📊 Storage Method Comparison

| Feature | CSV Files | SQLite Database | Web Dashboard |
|---------|-----------|-----------------|---------------|
| **Performance** | Slow with large files | Fast with indexes | Real-time optimized |
| **User Interface** | None | CLI/GUI tools | Modern web UI |
| **Remote Access** | Manual copy | File sharing | HTTP access |
| **Real-time** | No | No | ✅ WebSocket |
| **Mobile Support** | No | No | ✅ API + responsive |
| **Backup** | Multiple files | Single file | Single file |
| **Maintenance** | Manual | Semi-automatic | Fully automatic |
| **Collaboration** | File sharing | File sharing | ✅ Multi-user web |
| **Analytics** | External tools | Built-in stats | ✅ Interactive charts |
| **Export** | Native format | Multiple formats | ✅ Advanced filtering |

**Recommendation**: Use **Web Dashboard** cho production, **Database tools** cho automation, **CSV** cho legacy compatibility.

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