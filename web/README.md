# 🌐 PZEM-004T Web Dashboard — Docs đã gộp

Tài liệu chi tiết của web dashboard đã được gộp vào `README.md` ở thư mục gốc để tránh trùng lặp. Dưới đây là mục lục rút gọn trỏ về các phần tương ứng trong README chính.

## ✨ Mục lục rút gọn (xem README chính)

### 📊 Dashboard chính
- Tính năng và giao diện: xem phần “🌐 Web Dashboard System” trong README

### 📁 Xuất dữ liệu
- Hướng dẫn và preview: xem “📁 Export Center” trong README

### ⚙️ Quản lý hệ thống
- Xem “⚙️ System Settings” trong README

### 🔗 REST API
- Danh sách endpoint và WebSocket: xem “📱 Mobile Development Ready → API Ecosystem”

## 🚀 Cài đặt và chạy

### 1. Cài đặt nhanh
Xem “🚀 Cài đặt và sử dụng” trong README (lệnh `pip install`, `make run-web`, `run_web.py`)

### 2. Khởi chạy
- `make run-web` hoặc `python run_web.py` — chi tiết xem README chính

### 3. Truy cập
- Dashboard, Export, Settings, Docs: xem “Truy cập nhanh” trong README

## 📡 API Endpoints (xem README chính)

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

## 🏗️ Cấu trúc (tham chiếu)

```
web/
├── api.py              # FastAPI server chính
├── templates/          # HTML templates
│   ├── dashboard.html  # Dashboard chính
│   ├── export.html     # Trang xuất dữ liệu
│   └── settings.html   # Trang cài đặt
├── static/            # Static files (CSS, JS)
└── README.md          # File định hướng (docs gộp ở README chính)
```

## 🎨 Giao diện (tóm tắt)

### Dashboard
- Bootstrap 5, responsive; biểu đồ realtime 5s, làm mượt, giữ ngữ cảnh cả ngày; bảng “Hiển thị thêm”

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

## 🔧 Development (tham chiếu)

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

## 📱 Mobile API (tham chiếu)

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

## 🚨 Troubleshooting (tham chiếu)

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

## 📈 Performance (tham chiếu)

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
