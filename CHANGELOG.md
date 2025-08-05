# Changelog

Tất cả các thay đổi quan trọng trong dự án này sẽ được ghi lại trong file này.

## [2.0.0] - 2025-08-05

### 🎉 Major Release - Complete Library Rewrite

#### ✨ Added
- **Thư viện PZEM-004T hoàn chỉnh** với triển khai đầy đủ Modbus-RTU protocol
- **API đầy đủ** hỗ trợ tất cả function codes và register mapping
- **Xử lý lỗi toàn diện** với CRC validation, error handling, retry mechanism
- **Cache thông minh** để tối ưu hiệu suất (0.1s interval)
- **Tương thích ngược** với tên class cũ `PZEM004Tv30`
- **Tính năng verify reset** để kiểm tra reset thật
- **Cấu trúc dự án chuyên nghiệp** với thư mục src/, tools/, docs/
- **Makefile** để quản lý dự án (84 dòng)
- **Documentation chi tiết** trong docs/ (572 + 114 dòng)
- **Thông số kỹ thuật chính xác** theo tài liệu PZEM-004T datasheet
- **Quy tắc hiển thị** tuân thủ datasheet cho công suất và năng lượng
- **Phương thức format_measurements()** để format dữ liệu theo datasheet
- **Quản lý file size** tự động dọn dẹp file CSV khi quá lớn

#### 🔄 Changed
- **Cải thiện reset energy** với approach đơn giản hơn, tương thích với nhiều thiết bị
- **Cập nhật read_ac_sensor.py** sử dụng thư viện mới với hiệu suất tốt hơn (362 dòng)
- **Cập nhật reset_energy.py** với giao diện đơn giản và xác nhận an toàn (82 dòng)
- **Tổ chức lại cấu trúc file** theo chuẩn Python package
- **Cập nhật thông số kỹ thuật** theo datasheet chính thức PZEM-004T
- **Cải thiện hiển thị dữ liệu** theo quy tắc datasheet
- **Hỗ trợ adapter mở rộng** thêm CP210, FTDI ngoài PL2303, CH340

#### 🐛 Fixed
- **Lỗi reset energy** với thiết bị không gửi response
- **Timing issues** trong serial communication
- **Import paths** sau khi tổ chức lại cấu trúc
- **Error handling** trong multi-sensor monitoring

#### 📚 Documentation
- **docs/PZEM004T.md** - Hướng dẫn chi tiết thư viện (572 dòng)
- **README.md** - Cập nhật với cấu trúc mới và thông số kỹ thuật chính xác (407 dòng)
- **docs/DATA_LOGGING.md** - Hướng dẫn CSV logging (114 dòng)
- **PROJECT_STRUCTURE.md** - Tài liệu cấu trúc dự án chi tiết (227 dòng)

#### 🔧 Technical Specifications Update
- **Voltage**: 80-260V, resolution 0.1V, accuracy ±0.5%
- **Current**: 0-10A (10A model) / 0-100A (100A model), resolution 0.001A, accuracy ±0.5%
- **Power**: 0-2.3kW (10A) / 0-23kW (100A), resolution 0.1W, accuracy ±0.5%
- **Energy**: 0-9999.99kWh, resolution 1Wh, accuracy ±0.5%
- **Frequency**: 45-65Hz, resolution 0.1Hz, accuracy ±0.5%
- **Power Factor**: 0.00-1.00, resolution 0.01, accuracy ±1%
- **Starting thresholds**: Current 0.01A/0.02A, Power 0.4W
- **Display rules**: Power <1000W shows decimal, ≥1000W shows integer; Energy <10kWh shows Wh, ≥10kWh shows kWh

#### 📊 Data Management
- **CSV logging system** với cấu trúc chuẩn và timestamp chính xác
- **File size management** tự động dọn dẹp khi vượt quá kích thước
- **Multi-sensor support** với threading và error handling
- **Real-time monitoring** với cache optimization

## [1.0.0] - 2025-08-04

### 🎉 Initial Release

#### ✨ Added
- **Thư viện PZEM-004T cơ bản** với các chức năng đọc dữ liệu
- **Ứng dụng giám sát đa cảm biến** với CSV logging
- **Tool reset energy** cơ bản
- **Documentation** và examples

#### 🔧 Features
- Đọc voltage, current, power, energy, frequency, power factor
- Ghi dữ liệu CSV với timestamp
- Hiển thị dạng bảng cho nhiều cảm biến
- Reset energy counter
- Hỗ trợ nhiều loại USB-to-Serial adapter

---

## Format

Dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
và dự án này tuân theo [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Categories
- **Added** - Tính năng mới
- **Changed** - Thay đổi trong tính năng hiện có
- **Deprecated** - Tính năng sẽ bị loại bỏ
- **Removed** - Tính năng đã bị loại bỏ
- **Fixed** - Sửa lỗi
- **Security** - Cải thiện bảo mật 