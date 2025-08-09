# 🌐 PZEM-004T Web Dashboard

Giao diện web hiện đại để giám sát và trực quan hóa dữ liệu từ cảm biến PZEM-004T.

## ✨ Tính năng

### 📊 Dashboard chính
- **Real-time monitoring**: Hiển thị dữ liệu thời gian thực
- **Interactive charts**: Biểu đồ tương tác với Chart.js
- **Statistics cards**: Thống kê tổng quan (công suất, năng lượng, điện áp, số cảm biến)
- **Data filtering**: Lọc dữ liệu theo ngày và cảm biến
- **Responsive design**: Tương thích với mobile và desktop

### 📁 Xuất dữ liệu
- **Multiple formats**: Xuất CSV và JSON
- **Advanced filtering**: Lọc theo thời gian, cảm biến, số bản ghi
- **Preview function**: Xem trước dữ liệu trước khi xuất
- **Batch export**: Xuất theo cảm biến riêng biệt

### ⚙️ Quản lý hệ thống
- **System health**: Kiểm tra trạng thái hệ thống
- **Database stats**: Thống kê database chi tiết
- **Sensor management**: Quản lý và giám sát cảm biến
- **Data cleanup**: Dọn dẹp dữ liệu cũ tự động
- **API information**: Thông tin API endpoints

### 🔗 REST API
- **RESTful endpoints**: API hoàn chỉnh cho mobile app
- **Real-time WebSocket**: Cập nhật dữ liệu real-time
- **Comprehensive documentation**: Tài liệu API tự động với FastAPI
- **CORS support**: Hỗ trợ cross-origin requests

## 🚀 Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy web server

#### Cách 1: Sử dụng script startup (Khuyến nghị)
```bash
# Chạy với cài đặt mặc định
python run_web.py

# Chạy với custom port
python run_web.py --port 8080

# Chạy với auto-reload (development)
python run_web.py --reload

# Chạy mà không kiểm tra database
python run_web.py --skip-checks
```

#### Cách 2: Chạy trực tiếp với uvicorn
```bash
cd web/
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

#### Cách 3: Sử dụng Makefile (nếu có)
```bash
make run-web
```

### 3. Truy cập dashboard
- **Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Export Page**: http://localhost:8000/export  
- **Settings**: http://localhost:8000/settings

## 📡 API Endpoints

### Dashboard & Stats
- `GET /api/stats` - Database statistics
- `GET /api/sensors` - Sensor summary
- `GET /api/dashboard` - Complete dashboard data
- `GET /api/health` - System health check

### Measurements
- `GET /api/measurements` - Latest measurements with pagination
- `GET /api/measurements/range` - Measurements in date range
- `GET /api/sensor/{id}/stats` - Individual sensor statistics

### Export
- `GET /api/export/csv` - Export data to CSV
- `GET /api/export/json` - Export data to JSON

### Management
- `DELETE /api/cleanup` - Cleanup old data

### Real-time
- `WS /ws/realtime` - WebSocket for real-time updates

### Query Parameters

#### Measurements endpoint
- `limit`: Number of records (default: 100)
- `port`: Filter by sensor port
- `days`: Filter by last N days
- `sensor_id`: Filter by sensor ID

#### Date range endpoint
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)
- `port`: Filter by sensor port

#### Export endpoints
- `port`: Filter by sensor port
- `days`: Filter by last N days
- `limit`: Limit number of records

## 🏗️ Cấu trúc

```
web/
├── api.py              # FastAPI server chính
├── templates/          # HTML templates
│   ├── dashboard.html  # Dashboard chính
│   ├── export.html     # Trang xuất dữ liệu
│   └── settings.html   # Trang cài đặt
├── static/            # Static files (CSS, JS)
└── README.md          # Tài liệu này
```

## 🎨 Giao diện

### Dashboard
- **Modern UI**: Thiết kế hiện đại với Bootstrap 5
- **Dark/Light theme**: Tự động theo system preference
- **Interactive charts**: 
  - Power consumption over time
  - Voltage & Current monitoring
  - Real-time updates every 5 seconds
- **Data table**: Sortable, searchable measurement table

### Export Page
- **Format selection**: CSV vs JSON with preview
- **Advanced filtering**: Date range, sensor selection, record limits
- **Batch operations**: Export all sensors separately
- **Progress tracking**: Real-time export progress

### Settings Page
- **System monitoring**: Health checks, database stats
- **Sensor management**: View and manage connected sensors
- **Data maintenance**: Cleanup old data, backup functions
- **Danger zone**: Advanced operations with confirmations

## 🔧 Development

### Running in development mode
```bash
python run_web.py --reload
```

### API Documentation
FastAPI tự động generate API documentation tại:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Adding new endpoints
1. Thêm function vào `api.py` 
2. Sử dụng FastAPI decorators (`@app.get`, `@app.post`, etc.)
3. Documentation tự động được generate

### Customizing UI
- Templates sử dụng Jinja2 trong `templates/`
- Static files (CSS, JS) trong `static/`
- Bootstrap 5 và Chart.js đã được include

## 📱 Mobile API

API được thiết kế để hỗ trợ mobile applications:

### Authentication
Hiện tại chưa có authentication. Có thể thêm JWT hoặc API key authentication.

### Response format
```json
{
  "success": true,
  "data": {...},
  "count": 100,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Error handling
```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### Real-time updates
WebSocket endpoint `/ws/realtime` cung cấp updates real-time cho mobile apps.

## 🚨 Troubleshooting

### Database not found
```bash
# Chạy monitoring để tạo dữ liệu
python tools/read_ac_sensor_db.py
```

### Permission errors
```bash
# Đảm bảo quyền ghi vào thư mục data
chmod 755 data/
chmod 644 data/pzem_data.db
```

### Port already in use
```bash
# Sử dụng port khác
python run_web.py --port 8080
```

### Missing packages
```bash
# Cài đặt lại requirements
pip install -r requirements.txt
```

## 📈 Performance

### Optimization tips
- Database indexes đã được tối ưu
- Chart.js sử dụng time series optimization
- API responses được cache trong 100ms
- WebSocket connections được manage hiệu quả

### Scaling
- FastAPI hỗ trợ async/await cho high concurrency
- Database có thể migrate sang PostgreSQL cho production
- Static files có thể serve qua CDN
- API có thể scale horizontal với load balancer

## 🔐 Security

### Current security features
- Input validation với Pydantic models
- SQL injection protection với parameterized queries
- CORS configuration
- Error message sanitization

### Recommended for production
- Add authentication (JWT tokens)
- HTTPS enforcement
- Rate limiting
- API key management
- Input sanitization
- Security headers

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add features/fixes
4. Test thoroughly
5. Submit pull request

---

**Lưu ý**: Dashboard này được thiết kế để làm việc với database SQLite hiện có từ hệ thống PZEM-004T monitoring. Đảm bảo đã chạy `read_ac_sensor_db.py` để có dữ liệu hiển thị.
