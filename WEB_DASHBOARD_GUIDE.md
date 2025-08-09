# 🌐 PZEM-004T Web Dashboard - Hướng dẫn đầy đủ

## 📋 Tổng quan

Hệ thống web monitoring hoàn chỉnh cho PZEM-004T với dashboard hiện đại, API RESTful và khả năng real-time monitoring.

## ✨ Tính năng đã được triển khai

### 🎯 Dashboard chính (`/`)
- ✅ **Real-time monitoring cards**: Hiển thị tổng công suất, năng lượng, điện áp trung bình, số cảm biến
- ✅ **Interactive charts**: 
  - Biểu đồ công suất theo thời gian
  - Biểu đồ điện áp & dòng điện
  - Sử dụng Chart.js với time series
- ✅ **Date filtering**: Lọc dữ liệu theo khoảng thời gian
- ✅ **Sensor filtering**: Lọc theo cảm biến cụ thể
- ✅ **Real-time updates**: Tự động cập nhật mỗi 5 giây
- ✅ **Data table**: Bảng hiển thị measurements với pagination
- ✅ **Responsive design**: Tương thích mobile và desktop

### 📁 Export data (`/export`)
- ✅ **Multiple formats**: CSV và JSON
- ✅ **Advanced filtering**: Theo thời gian, cảm biến, số bản ghi
- ✅ **Preview function**: Xem trước dữ liệu trước khi xuất
- ✅ **Batch export**: Xuất riêng biệt theo cảm biến
- ✅ **Progress tracking**: Thanh tiến trình khi xuất

### ⚙️ Settings (`/settings`)
- ✅ **System health monitoring**: Kiểm tra trạng thái hệ thống
- ✅ **Database statistics**: Thống kê chi tiết database
- ✅ **Sensor management**: Quản lý và giám sát cảm biến
- ✅ **Data cleanup**: Dọn dẹp dữ liệu cũ
- ✅ **Backup functions**: Sao lưu dữ liệu
- ✅ **API information**: Thông tin endpoints cho mobile app

### 🔗 REST API (cho mobile app)
- ✅ `GET /api/stats` - Database statistics
- ✅ `GET /api/sensors` - Sensor summary  
- ✅ `GET /api/measurements` - Latest measurements với filtering
- ✅ `GET /api/measurements/range` - Measurements theo date range
- ✅ `GET /api/dashboard` - Complete dashboard data
- ✅ `GET /api/sensor/{id}/stats` - Individual sensor statistics
- ✅ `GET /api/export/csv` - Export CSV
- ✅ `GET /api/export/json` - Export JSON
- ✅ `DELETE /api/cleanup` - Cleanup old data
- ✅ `GET /api/health` - Health check
- ✅ `WS /ws/realtime` - WebSocket real-time updates

## 🚀 Cách sử dụng

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy web server

#### Cách đơn giản nhất
```bash
# Sử dụng script startup
python run_web.py

# Hoặc với Makefile
make run-web

# Development mode với auto-reload
make run-web-dev
```

#### Cách thủ công
```bash
cd web/
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Truy cập dashboard
- **Dashboard chính**: http://localhost:8000
- **Export dữ liệu**: http://localhost:8000/export
- **Cài đặt**: http://localhost:8000/settings
- **API Documentation**: http://localhost:8000/docs

## 📊 Demo với dữ liệu

### Nếu chưa có dữ liệu
```bash
# Chạy monitoring để tạo dữ liệu
python tools/read_ac_sensor_db.py

# Hoặc
make run-monitor-db
```

### Nếu đã có dữ liệu CSV muốn import
```bash
# Tạo script migrate đơn giản
python -c "
import sys, os, pandas as pd
sys.path.append('src')
from database import PZEMDatabase
from datetime import datetime

db = PZEMDatabase()
# Add sample data for demo
for i in range(100):
    data = {
        'port': '/dev/ttyUSB0',
        'timestamp': datetime.now(),
        'voltage': 220.0 + i*0.1,
        'current': 1.0 + i*0.01,
        'power': 220.0 + i*0.1,
        'energy': 1000 + i,
        'frequency': 50.0,
        'power_factor': 0.98,
        'alarm': False
    }
    db.save_measurement(data)
print('Added 100 sample measurements')
"
```

## 🎨 UI/UX Features

### 🌈 Design hiện đại
- **Bootstrap 5**: Framework UI hiện đại
- **Gradient backgrounds**: Màu sắc đẹp mắt
- **Smooth animations**: Hiệu ứng mượt mà
- **Card layouts**: Bố cục card đẹp
- **Responsive grid**: Responsive hoàn hảo

### 📊 Visualization
- **Chart.js**: Thư viện chart mạnh mẽ
- **Real-time charts**: Cập nhật real-time
- **Multiple chart types**: Line charts, time series
- **Interactive**: Zoom, hover, pan
- **Color coded**: Màu sắc phân biệt rõ ràng

### 🔄 Real-time features
- **WebSocket**: Kết nối real-time
- **Auto refresh**: Tự động làm mới
- **Live indicators**: Chỉ báo trạng thái live
- **Push updates**: Đẩy dữ liệu mới tự động

## 📱 Mobile API Usage

### Basic API calls
```javascript
// Get latest measurements
fetch('/api/measurements?limit=50')
  .then(response => response.json())
  .then(data => {
    console.log('Measurements:', data.data);
  });

// Get measurements for specific sensor
fetch('/api/measurements?port=/dev/ttyUSB0&limit=100')
  .then(response => response.json())
  .then(data => {
    console.log('Sensor data:', data.data);
  });

// Get date range data
fetch('/api/measurements/range?start_date=2025-01-01&end_date=2025-01-15')
  .then(response => response.json())
  .then(data => {
    console.log('Range data:', data.data);
  });
```

### WebSocket for real-time
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/realtime');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'measurement_update') {
        console.log('New measurement:', data.data);
        // Update mobile UI
    }
};

ws.onopen = function(event) {
    console.log('Connected to real-time updates');
};
```

### Error handling
```javascript
async function fetchWithErrorHandling(url) {
    try {
        const response = await fetch(url);
        const result = await response.json();
        
        if (result.success) {
            return result.data;
        } else {
            throw new Error(result.error || 'API Error');
        }
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}
```

## 🏗️ Kiến trúc hệ thống

```
PZEM-004T Hardware
       ↓
Serial Communication (Modbus-RTU)
       ↓  
Python PZEM Library (src/pzem.py)
       ↓
Database Storage (src/database.py)
       ↓
FastAPI Web Server (web/api.py)
    ↙        ↘
Web Dashboard    REST API
    ↓              ↓
Bootstrap UI    Mobile App
Chart.js        (Future)
```

## 🔧 Configuration

### Server configuration
```python
# Trong run_web.py
python run_web.py --host 0.0.0.0 --port 8000 --reload
```

### Database configuration
```python
# Trong web/api.py
db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'pzem_data.db')
database = PZEMDatabase(db_path)
```

### CORS configuration (for mobile)
```python
# Thêm vào web/api.py nếu cần
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚨 Troubleshooting

### Database issues
```bash
# Kiểm tra database
ls -la data/pzem_data.db

# Xem thống kê
make db-stats

# Tạo dữ liệu mẫu nếu cần
python tools/read_ac_sensor_db.py
```

### Port conflicts
```bash
# Sử dụng port khác
python run_web.py --port 8080
```

### Dependencies missing
```bash
# Cài đặt lại
pip install -r requirements.txt
```

### Permission errors
```bash
chmod 755 data/
chmod 644 data/pzem_data.db
chmod +x run_web.py
```

## 📈 Performance Tips

### Database optimization
- ✅ Indexes đã được tạo cho timestamp và sensor_id
- ✅ Connection pooling với SQLite
- ✅ Efficient queries with limits

### Frontend optimization  
- ✅ Chart.js với time series optimization
- ✅ API response caching (100ms)
- ✅ Lazy loading cho large datasets
- ✅ Responsive images và assets

### API optimization
- ✅ FastAPI async/await
- ✅ Pydantic validation
- ✅ Error handling
- ✅ WebSocket connection management

## 🔐 Security Considerations

### Current security
- ✅ Input validation với Pydantic
- ✅ SQL injection protection
- ✅ Error message sanitization
- ✅ File path validation

### Recommended for production
- [ ] Authentication (JWT tokens)
- [ ] HTTPS enforcement  
- [ ] Rate limiting
- [ ] API key management
- [ ] CORS configuration
- [ ] Security headers

## 🎯 Next Steps

### Immediate improvements
1. **Authentication system**: JWT cho mobile API
2. **Data aggregation**: Hourly/daily summaries
3. **Alert system**: Email/SMS notifications
4. **Export scheduling**: Tự động xuất theo lịch

### Advanced features
1. **Machine learning**: Dự đoán consumption patterns
2. **Multi-tenant**: Support multiple locations
3. **Mobile app**: React Native hoặc Flutter
4. **Cloud deployment**: Docker + Kubernetes

## 🤝 Integration với hệ thống hiện có

### Với database_gui.py
Web dashboard bao gồm tất cả chức năng của database_gui.py:
- ✅ View database stats → `/settings`
- ✅ View sensor summary → `/settings`  
- ✅ View latest measurements → Dashboard table
- ✅ Export data → `/export`
- ✅ Cleanup old data → `/settings`
- ✅ Advanced queries → Dashboard filtering

### Với monitoring scripts
- `read_ac_sensor_db.py` tạo dữ liệu
- Web dashboard hiển thị dữ liệu real-time
- API cung cấp dữ liệu cho mobile apps

### Với tools hiện có
- `query_database.py` → API endpoints
- `reset_energy_no_address_change.py` → Có thể integrate vào settings
- Migration tools → Có thể thêm vào settings

## 📞 Support

### Documentation
- **Web README**: `web/README.md`
- **API Docs**: http://localhost:8000/docs
- **Main README**: `README.md`

### Logs và debugging
```bash
# Chạy với debug logs
python run_web.py --reload

# Check API health
curl http://localhost:8000/api/health

# Test WebSocket
# Dùng browser dev tools để test ws://localhost:8000/ws/realtime
```

---

## 🎉 Kết luận

Hệ thống web dashboard đã được xây dựng hoàn chỉnh với:

1. **✅ Dashboard hiện đại** với real-time charts và monitoring
2. **✅ API RESTful đầy đủ** cho mobile applications  
3. **✅ Export functionality** với multiple formats
4. **✅ Settings management** cho system administration
5. **✅ Real-time updates** qua WebSocket
6. **✅ Responsive design** cho mobile và desktop
7. **✅ Documentation đầy đủ** cho developers

Hệ thống sẵn sàng để sử dụng và có thể mở rộng thêm các tính năng trong tương lai!

**🚀 Để bắt đầu:**
```bash
make run-monitor-db  # Terminal 1: Start data collection
make run-web         # Terminal 2: Start web dashboard
```

Sau đó truy cập http://localhost:8000 để sử dụng dashboard!
