# Changelog

Tất cả các thay đổi quan trọng trong dự án này sẽ được ghi lại trong file này.

## [2.0.0] - 2025-08-05

### 🎉 Major Release - Complete Library Rewrite

#### ✨ Added
- **Thư viện PZEM-004T hoàn chỉnh** với triển khai đầy đủ Modbus-RTU protocol
- **API đầy đủ** hỗ trợ tất cả function codes và register mapping
- **Xử lý lỗi toàn diện** với CRC validation, error handling, retry mechanism
- **Cache thông minh** để tối ưu hiệu suất
- **Tương thích ngược** với tên class cũ `PZEM004Tv30`
- **Tính năng verify reset** để kiểm tra reset thật
- **Cấu trúc dự án chuyên nghiệp** với thư mục src/, tools/, examples/, docs/
- **Setup script** và Makefile để quản lý dự án
- **Quick start script** để demo nhanh
- **Documentation chi tiết** trong docs/

#### 🔄 Changed
- **Cải thiện reset energy** với approach đơn giản hơn, tương thích với nhiều thiết bị
- **Cập nhật read_ac_sensor.py** sử dụng thư viện mới với hiệu suất tốt hơn
- **Cập nhật reset_energy.py** với menu tương tác và xác nhận an toàn
- **Tổ chức lại cấu trúc file** theo chuẩn Python package

#### 🐛 Fixed
- **Lỗi reset energy** với thiết bị không gửi response
- **Timing issues** trong serial communication
- **Import paths** sau khi tổ chức lại cấu trúc

#### 📚 Documentation
- **PZEM004T.md** - Hướng dẫn chi tiết thư viện
- **README.md** - Cập nhật với cấu trúc mới
- **Example usage** - 6 ví dụ sử dụng thực tế

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