# 🌐 PZEM-004T Web Dashboard - Complete Guide

## 📋 Tổng quan

**Production-ready web monitoring system** cho PZEM-004T với modern dashboard, comprehensive REST API, real-time updates và mobile-friendly interface. Được thiết kế để thay thế hoàn toàn GUI tools với web-based solution.

## ✨ Features Overview - Production Ready

### 🎯 Main Dashboard (`/`) - Real-time Monitoring ⭐
- 🎮 **Live monitoring cards**: 
  - Total power consumption across all sensors
  - Total energy accumulated  
  - Average voltage monitoring
  - Active sensor count với connectivity status
- 📊 **Interactive Charts** (Chart.js powered):
  - Power consumption timeline với zoom/pan
  - Voltage & Current monitoring graphs  
  - Real-time updates every 5 seconds
  - Time series optimization cho performance
- 🔍 **Advanced Filtering**:
  - Date range picker với preset options
  - Individual sensor selection
  - Auto-refresh controls
- 📋 **Smart Data Table**:
  - Latest measurements với sorting/pagination
  - Real-time row updates
  - Export selected data
- 📱 **Fully Responsive**: Perfect on mobile, tablet, desktop

### 📁 Export Center (`/export`) - Data Management ⭐
- 📄 **Multi-format Export**:
  - CSV với proper encoding
  - JSON với metadata
  - Excel-compatible formatting
- 🎛️ **Advanced Filtering Engine**:
  - Date range selection với calendar picker
  - Multi-sensor selection
  - Record limit controls  
  - Preview before download
- 🚀 **Batch Operations**:
  - Export all sensors separately
  - Bulk download với progress tracking
  - Background processing cho large datasets
- 👁️ **Data Preview**: Live preview với sample data

### ⚙️ System Settings (`/settings`) - Management Center ⭐  
- 💚 **Health Monitoring Dashboard**:
  - System status indicators
  - Database connectivity checks
  - API performance metrics
  - Real-time sensor connectivity
- 📊 **Database Analytics**:
  - Storage statistics và growth trends
  - Query performance metrics
  - Data integrity checks
- 🔌 **Sensor Management**:
  - Live sensor discovery
  - Connection status monitoring  
  - Device configuration view
- 🗑️ **Maintenance Tools**:
  - Automated cleanup scheduling
  - Database optimization
  - Backup management
- 🚨 **Danger Zone**: Advanced operations với confirmations

### 🔗 REST API Ecosystem - Mobile Ready ⭐

#### Core Data Endpoints
- `GET /api/dashboard` - Complete dashboard data aggregation
- `GET /api/measurements` - Paginated measurements với rich filtering
- `GET /api/measurements/range` - Date range queries với optimization
- `GET /api/sensors` - Sensor inventory với status
- `GET /api/sensor/{id}/stats` - Individual sensor analytics

#### Export & Management
- `GET /api/export/csv` - Streaming CSV export
- `GET /api/export/json` - JSON export với metadata
- `DELETE /api/cleanup` - Data lifecycle management
- `DELETE /api/measurements` - Bulk data removal
- `DELETE /api/database/reset` - Full database reset

#### System Operations  
- `GET /api/health` - System health checks
- `GET /api/stats` - Database statistics
- `GET /api/sensors/connectivity` - Real-time connectivity status
- `WS /ws/realtime` - WebSocket live updates
- `WS /ws` - General WebSocket connection

#### Advanced Features
- **Auto-documentation**: Swagger UI tại `/docs`
- **Error handling**: Consistent JSON error responses
- **CORS support**: Ready cho mobile development
- **Background tasks**: USB monitoring, cleanup scheduling

## 🚀 Setup & Deployment Guide

### 1. Quick Start (2 minutes) ⭐
```bash
# Clone và setup
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
pip install -r requirements.txt

# Start data collection (Terminal 1)
make run-monitor-db

# Start web dashboard (Terminal 2)
make run-web

# Access: http://localhost:8000
```

### 2. Production Deployment

#### Using run_web.py (Recommended) ⭐
```bash
# Production mode với health checks
python run_web.py --host 0.0.0.0 --port 8000

# Development mode với auto-reload
python run_web.py --reload

# Custom configuration
python run_web.py --host 192.168.1.100 --port 8080 --skip-checks
```

#### Using Makefile (Simplified)
```bash
# Production web server
make run-web

# Development mode với auto-reload  
make run-web-dev
```

#### Manual uvicorn (Advanced)
```bash
cd web/
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

### 3. Access Points ⭐
- **🏠 Main Dashboard**: http://localhost:8000
- **📁 Export Center**: http://localhost:8000/export  
- **⚙️ System Settings**: http://localhost:8000/settings
- **📚 API Documentation**: http://localhost:8000/docs
- **🔄 Health Check**: http://localhost:8000/api/health

### 4. Mobile Development
- **📱 Base API URL**: `http://localhost:8000/api/`
- **🔌 WebSocket**: `ws://localhost:8000/ws/realtime`
- **📖 Interactive Docs**: `http://localhost:8000/docs`

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

## 🔗 System Integration & Migration

### 🎯 Complete GUI Replacement 
Web dashboard provides **ALL functionality** of standalone tools với better UX:

| Legacy Tool | Web Equivalent | Benefits |
|-------------|----------------|----------|
| `database_gui.py` | `/settings` page | ✅ Remote access, better UX |
| `query_database.py` | `/export` page | ✅ Visual interface, preview |
| Manual monitoring | `/` dashboard | ✅ Real-time charts, mobile |
| CSV analysis | API endpoints | ✅ Programmatic access |

### 🏗️ Architecture Integration
```
PZEM Hardware → read_ac_sensor_db.py → SQLite → Web Dashboard → Users
                                              ↓
                                           REST API → Mobile App
```

### 📱 Mobile Development Ready
- ✅ **Complete REST API** với comprehensive endpoints
- ✅ **Real-time WebSocket** cho live updates  
- ✅ **CORS enabled** cho cross-origin requests
- ✅ **Auto-documentation** với Swagger UI
- ✅ **Consistent error handling** và response formats

### 🔄 Legacy Tool Compatibility
- **CSV exports** vẫn available cho existing workflows
- **CLI tools** remain functional cho automation scripts
- **Database schema** unchanged để maintain data continuity
- **Backward compatibility** với existing monitoring scripts

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

## 🎉 Conclusion - Production Ready System

**AC Management Web Dashboard** là một **production-ready monitoring solution** với:

### ✅ Complete Feature Set
1. **🎯 Modern Dashboard** với real-time monitoring và interactive charts
2. **📁 Advanced Export System** với filtering và batch operations  
3. **⚙️ System Management** với health monitoring và maintenance tools
4. **🔗 Comprehensive REST API** cho mobile development
5. **🔄 Real-time Updates** qua WebSocket integration
6. **📱 Mobile-Ready Design** với responsive UI và API
7. **📚 Auto-Generated Documentation** với Swagger UI

### 🏆 Production Benefits
- **🚀 Easy Deployment**: Single command setup với health checks
- **📈 Scalable Architecture**: FastAPI async foundation
- **🔒 Enterprise Ready**: Input validation, error handling, logging
- **🔧 Maintenance Friendly**: Built-in cleanup, monitoring, backup tools
- **📱 Mobile Integration**: Complete API ecosystem cho app development

### 🚀 Quick Start (1 minute)
```bash
# 1. Setup project
git clone <repo> && cd ac_management && pip install -r requirements.txt

# 2. Start monitoring (Terminal 1)
make run-monitor-db

# 3. Start web dashboard (Terminal 2) 
make run-web

# 4. Access: http://localhost:8000
```

### 📱 For Mobile Developers
- **📖 API Docs**: http://localhost:8000/docs  
- **🔌 WebSocket**: ws://localhost:8000/ws/realtime
- **🎯 Base URL**: http://localhost:8000/api/

---

**🌟 AC Management v2.1.0+** - From hardware monitoring đến production web dashboard, everything you need cho professional PZEM-004T power monitoring.
