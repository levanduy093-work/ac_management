# PZEM-004T Python Library Documentation

## Tổng quan

Thư viện Python hoàn chỉnh cho module đo điện PZEM-004T, hỗ trợ giao tiếp Modbus-RTU qua cổng serial. Thư viện này triển khai đầy đủ các tính năng theo tài liệu kỹ thuật của PZEM-004T.

### Tính năng chính

- ✅ Đọc điện áp, dòng điện, công suất, năng lượng, tần số, hệ số công suất
- ✅ Thiết lập ngưỡng cảnh báo công suất
- ✅ Thay đổi địa chỉ thiết bị
- ✅ Reset bộ đếm năng lượng
- ✅ Calibration (dành cho nhà máy)
- ✅ Xử lý lỗi toàn diện
- ✅ Kiểm tra CRC
- ✅ Cache dữ liệu để tối ưu hiệu suất

### Các model được hỗ trợ

- **PZEM-004T-10A**: Dải đo 0-10A (shunt tích hợp)
- **PZEM-004T-100A**: Dải đo 0-100A (CT ngoài)

## Cài đặt

### Yêu cầu hệ thống

```bash
pip install pyserial
```

### Cài đặt thư viện

Copy file `pzem.py` vào project của bạn hoặc cài đặt trực tiếp:

```python
from pzem import PZEM004T
```

## Kết nối phần cứng

### Sơ đồ kết nối

```
PZEM-004T Module:
┌─────────────────┐
│   TTL Interface │
├─────────────────┤
│ GND │ TX │ RX │ 5V │
└─────┴────┴────┴────┘
         │
         ▼
┌─────────────────┐
│ TTL to USB Cable│
└─────────────────┘
         │
         ▼
┌─────────────────┐
│      PC/USB     │
└─────────────────┘
```

### Kết nối điện

**PZEM-004T-10A:**
- Kết nối trực tiếp L, N vào module
- Tải được mắc nối tiếp với dây L

**PZEM-004T-100A:**
- Kết nối L, N vào module
- Sử dụng Current Transformer (CT) cho đo dòng điện
- CT được đặt quanh dây L của tải

### Lưu ý quan trọng

- **TTL Interface**: Là giao diện thụ động, cần nguồn 5V ngoài
- **Tất cả 4 chân phải được kết nối**: GND, TX, RX, 5V
- **Nếu không kết nối đủ 4 chân, thiết bị không thể giao tiếp**

## Sử dụng cơ bản

### Khởi tạo kết nối

```python
from pzem import PZEM004T

# Khởi tạo với địa chỉ mặc định (0xF8)
pzem = PZEM004T(port='/dev/ttyUSB0')

# Hoặc chỉ định địa chỉ cụ thể
pzem = PZEM004T(port='/dev/ttyUSB0', address=0x01)

# Đóng kết nối khi hoàn thành
pzem.close()
```

### Đọc các giá trị đo

```python
# Đọc từng giá trị riêng lẻ
voltage = pzem.get_voltage()      # V
current = pzem.get_current()      # A
power = pzem.get_power()          # W
energy = pzem.get_energy()        # kWh
frequency = pzem.get_frequency()  # Hz
pf = pzem.get_power_factor()      # Power Factor
alarm = pzem.get_alarm_status()   # Boolean

# Đọc tất cả giá trị cùng lúc
measurements = pzem.get_all_measurements()
print(f"Voltage: {measurements['voltage']}V")
print(f"Current: {measurements['current']}A")
print(f"Power: {measurements['power']}W")
print(f"Energy: {measurements['energy']}kWh")
print(f"Frequency: {measurements['frequency']}Hz")
print(f"Power Factor: {measurements['power_factor']}")
print(f"Alarm: {measurements['alarm_status']}")

# In tất cả giá trị theo định dạng đẹp
pzem.print_measurements()
```

## API Reference

### Constructor

```python
PZEM004T(port: str, address: int = 0xF8, timeout: float = 1.0)
```

**Tham số:**
- `port` (str): Cổng serial (ví dụ: '/dev/ttyUSB0', 'COM3')
- `address` (int): Địa chỉ thiết bị (1-247, mặc định 0xF8 cho thiết bị đơn)
- `timeout` (float): Timeout giao tiếp serial (giây)

### Phương thức đọc dữ liệu

#### `get_voltage() -> float`
Trả về điện áp tính bằng V.

#### `get_current() -> float`
Trả về dòng điện tính bằng A.

#### `get_power() -> float`
Trả về công suất tác dụng tính bằng W.

#### `get_energy() -> float`
Trả về tổng năng lượng tính bằng kWh.

#### `get_frequency() -> float`
Trả về tần số tính bằng Hz.

#### `get_power_factor() -> float`
Trả về hệ số công suất.

#### `get_alarm_status() -> bool`
Trả về trạng thái cảnh báo công suất (True = có cảnh báo).

#### `get_all_measurements() -> Dict[str, Any]`
Trả về tất cả giá trị đo trong một dictionary.

#### `read_measurements() -> Dict[str, Any]`
Đọc trực tiếp từ thiết bị và trả về tất cả giá trị đo.

### Phương thức cấu hình

#### `set_power_alarm_threshold(watts: int) -> bool`
Thiết lập ngưỡng cảnh báo công suất.

**Tham số:**
- `watts` (int): Ngưỡng cảnh báo tính bằng W (1-25000)

**Trả về:** True nếu thành công

#### `get_power_alarm_threshold() -> Optional[int]`
Lấy ngưỡng cảnh báo công suất hiện tại.

**Trả về:** Ngưỡng cảnh báo tính bằng W hoặc None nếu lỗi

#### `set_address(new_address: int) -> bool`
Thay đổi địa chỉ thiết bị.

**Tham số:**
- `new_address` (int): Địa chỉ mới (1-247)

**Cảnh báo:** Thay đổi này là vĩnh viễn. Thiết bị chỉ phản hồi địa chỉ mới.

#### `get_address() -> Optional[int]`
Lấy địa chỉ thiết bị hiện tại.

**Trả về:** Địa chỉ thiết bị hoặc None nếu lỗi

### Phương thức điều khiển

#### `reset_energy() -> bool`
Reset bộ đếm năng lượng về 0.

**Trả về:** True nếu thành công

#### `calibrate() -> bool`
Thực hiện calibration thiết bị (chỉ dành cho nhà máy).

**Cảnh báo:** Chỉ sử dụng cho bảo trì nhà máy. Calibration sai có thể ảnh hưởng độ chính xác đo.

### Phương thức tiện ích

#### `print_measurements()`
In tất cả giá trị đo theo định dạng đẹp.

#### `close()`
Đóng kết nối serial.

## Ví dụ sử dụng

### Ví dụ 1: Đọc và hiển thị dữ liệu cơ bản

```python
from pzem import PZEM004T
import time

try:
    pzem = PZEM004T(port='/dev/ttyUSB0')
    
    while True:
        pzem.print_measurements()
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nDừng chương trình...")
    pzem.close()
```

### Ví dụ 2: Giám sát công suất với cảnh báo

```python
from pzem import PZEM004T
import time

pzem = PZEM004T(port='/dev/ttyUSB0')

# Thiết lập ngưỡng cảnh báo 1000W
if pzem.set_power_alarm_threshold(1000):
    print("Đã thiết lập ngưỡng cảnh báo 1000W")

# Giám sát liên tục
while True:
    power = pzem.get_power()
    alarm = pzem.get_alarm_status()
    
    print(f"Công suất: {power:.1f}W")
    
    if alarm:
        print("⚠️  CẢNH BÁO: Công suất vượt ngưỡng!")
    
    time.sleep(2)
```

### Ví dụ 3: Ghi log dữ liệu

```python
from pzem import PZEM004T
import csv
import time
from datetime import datetime

pzem = PZEM004T(port='/dev/ttyUSB0')

# Tạo file CSV
with open('power_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Voltage(V)', 'Current(A)', 'Power(W)', 'Energy(kWh)', 'Frequency(Hz)', 'PF'])
    
    try:
        while True:
            measurements = pzem.get_all_measurements()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            writer.writerow([
                timestamp,
                measurements['voltage'],
                measurements['current'],
                measurements['power'],
                measurements['energy'],
                measurements['frequency'],
                measurements['power_factor']
            ])
            file.flush()  # Đảm bảo ghi ngay lập tức
            
            time.sleep(5)  # Ghi log mỗi 5 giây
            
    except KeyboardInterrupt:
        print("Dừng ghi log...")

pzem.close()
```

### Ví dụ 4: Quản lý nhiều thiết bị

```python
from pzem import PZEM004T
import time

# Khởi tạo nhiều thiết bị với địa chỉ khác nhau
devices = {
    'device1': PZEM004T(port='/dev/ttyUSB0', address=0x01),
    'device2': PZEM004T(port='/dev/ttyUSB1', address=0x02),
    'device3': PZEM004T(port='/dev/ttyUSB2', address=0x03)
}

try:
    while True:
        for name, device in devices.items():
            try:
                measurements = device.get_all_measurements()
                print(f"\n{name}:")
                print(f"  Power: {measurements['power']:.1f}W")
                print(f"  Energy: {measurements['energy']:.3f}kWh")
            except Exception as e:
                print(f"Lỗi đọc {name}: {e}")
        
        time.sleep(10)
        
except KeyboardInterrupt:
    print("Dừng chương trình...")
    for device in devices.values():
        device.close()
```

### Ví dụ 5: Thiết lập ban đầu thiết bị

```python
from pzem import PZEM004T

pzem = PZEM004T(port='/dev/ttyUSB0')

# Kiểm tra địa chỉ hiện tại
current_addr = pzem.get_address()
print(f"Địa chỉ hiện tại: {current_addr}")

# Thay đổi địa chỉ (nếu cần)
if current_addr != 0x01:
    if pzem.set_address(0x01):
        print("Đã thay đổi địa chỉ thành 0x01")
    else:
        print("Lỗi thay đổi địa chỉ")

# Thiết lập ngưỡng cảnh báo
if pzem.set_power_alarm_threshold(2000):
    print("Đã thiết lập ngưỡng cảnh báo 2000W")

# Reset bộ đếm năng lượng
if pzem.reset_energy():
    print("Đã reset bộ đếm năng lượng")

pzem.close()
```

## Thông số kỹ thuật

### Đặc điểm đo

| Thông số | Dải đo | Độ phân giải | Độ chính xác |
|----------|--------|--------------|--------------|
| Điện áp | 80-260V | 0.1V | ±0.5% |
| Dòng điện | 0-10A (10A) / 0-100A (100A) | 0.001A | ±0.5% |
| Công suất | 0-2.3kW (10A) / 0-23kW (100A) | 0.1W | ±0.5% |
| Năng lượng | 0-9999.99kWh | 1Wh | ±0.5% |
| Tần số | 45-65Hz | 0.1Hz | ±0.5% |
| Hệ số công suất | 0.00-1.00 | 0.01 | ±1% |

### Giao thức giao tiếp

- **Giao thức:** Modbus-RTU
- **Tốc độ baud:** 9600
- **Data bits:** 8
- **Stop bits:** 1
- **Parity:** None
- **Địa chỉ slave:** 1-247 (0xF8 cho thiết bị đơn)

### Function Codes hỗ trợ

| Function Code | Mô tả |
|---------------|-------|
| 0x03 | Read Holding Registers |
| 0x04 | Read Input Registers |
| 0x06 | Write Single Register |
| 0x41 | Calibration |
| 0x42 | Reset Energy |

## Xử lý lỗi

### Các lỗi thường gặp

#### 1. Lỗi kết nối serial

```python
try:
    pzem = PZEM004T(port='/dev/ttyUSB0')
except serial.SerialException as e:
    print(f"Lỗi kết nối: {e}")
    # Kiểm tra:
    # - Cổng serial có đúng không
    # - Thiết bị có được kết nối không
    # - Quyền truy cập cổng serial
```

#### 2. Lỗi CRC

```python
# Thư viện tự động kiểm tra CRC
# Nếu có lỗi, sẽ log và trả về None
measurements = pzem.get_all_measurements()
if not measurements:
    print("Lỗi đọc dữ liệu - kiểm tra kết nối")
```

#### 3. Lỗi Modbus

Thư viện tự động xử lý các lỗi Modbus:
- 0x01: Illegal function
- 0x02: Illegal data address
- 0x03: Illegal data value
- 0x04: Slave device failure

### Debug và logging

```python
import logging

# Bật debug logging
logging.basicConfig(level=logging.DEBUG)

# Hoặc chỉ log lỗi
logging.basicConfig(level=logging.ERROR)
```

## Troubleshooting

### Thiết bị không phản hồi

1. **Kiểm tra kết nối phần cứng:**
   - Đảm bảo tất cả 4 chân TTL được kết nối: GND, TX, RX, 5V
   - Kiểm tra nguồn 5V cho TTL interface

2. **Kiểm tra cổng serial:**
   ```bash
   # Linux
   ls /dev/ttyUSB*
   ls /dev/ttyACM*
   
   # Windows
   # Kiểm tra Device Manager > Ports
   ```

3. **Kiểm tra quyền truy cập:**
   ```bash
   # Linux - thêm user vào dialout group
   sudo usermod -a -G dialout $USER
   ```

### Dữ liệu đọc không chính xác

1. **Kiểm tra địa chỉ thiết bị:**
   ```python
   addr = pzem.get_address()
   print(f"Địa chỉ thiết bị: {addr}")
   ```

2. **Kiểm tra kết nối điện:**
   - Đảm bảo L, N được kết nối đúng
   - Với PZEM-004T-100A, kiểm tra CT

3. **Reset thiết bị:**
   ```python
   pzem.reset_energy()
   ```

### Hiệu suất chậm

1. **Sử dụng cache:**
   ```python
   # Thư viện tự động cache dữ liệu
   # Không cần gọi get_voltage() nhiều lần
   measurements = pzem.get_all_measurements()
   voltage = measurements['voltage']
   current = measurements['current']
   ```

2. **Tăng timeout nếu cần:**
   ```python
   pzem = PZEM004T(port='/dev/ttyUSB0', timeout=2.0)
   ```

## Tương thích ngược

Thư viện mới vẫn hỗ trợ tên class cũ:

```python
# Cả hai cách đều hoạt động
from pzem import PZEM004T
from pzem import PZEM004Tv30  # Tương thích ngược

pzem1 = PZEM004T(port='/dev/ttyUSB0')
pzem2 = PZEM004Tv30(port='/dev/ttyUSB0')  # Vẫn hoạt động
```

## Đóng góp

Nếu bạn tìm thấy lỗi hoặc muốn cải thiện thư viện, vui lòng:

1. Kiểm tra tài liệu này trước
2. Tạo issue với mô tả chi tiết
3. Đính kèm log lỗi nếu có

## License

Thư viện này được phát hành dưới MIT License.

---

**Lưu ý:** Thư viện này được phát triển dựa trên tài liệu kỹ thuật chính thức của PZEM-004T. Đảm bảo sử dụng đúng model và kết nối phần cứng theo hướng dẫn. 