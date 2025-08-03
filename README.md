# 🔌 AC Management - PZEM-004t v3.0 Multi-Sensor Monitor

Một ứng dụng Python chuyên nghiệp để giám sát nhiều cảm biến công suất điện PZEM-004t v3.0 đồng thời sử dụng giao thức Modbus-RTU. Script tự động phát hiện và đọc dữ liệu từ các bộ chuyển đổi USB-to-Serial (PL2303, CH340, FTDI) mỗi giây một lần.

## 📊 Thông số giám sát

Script sẽ đọc và hiển thị các thông số điện quan trọng từ mỗi cảm biến:

| Thông số | Đơn vị | Mô tả |
|----------|---------|-------|
| **Voltage** | V | Điện áp AC hiện tại |
| **Current** | A | Dòng điện tiêu thụ |
| **Power** | W | Công suất tác dụng thực tế |
| **Energy** | Wh | Tổng điện năng tiêu thụ tích lũy |
| **Frequency** | Hz | Tần số nguồn điện (50/60Hz) |
| **Power Factor** | - | Hệ số công suất (0.0 - 1.0) |
| **Alarm** | ON/OFF | Trạng thái cảnh báo ngưỡng công suất |

## 🎯 Tính năng chính

- ✅ **Tự động phát hiện cảm biến**: Quét và kết nối tự động với các thiết bị PZEM-004t
- ✅ **Đa cảm biến**: Hỗ trợ đọc từ nhiều cảm biến cùng lúc
- ✅ **Cơ chế retry**: Tự động thử lại khi gặp lỗi kết nối
- ✅ **Tối ưu cho Raspberry Pi**: Cấu hình timeout và buffer phù hợp
- ✅ **Giao diện console thân thiện**: Hiển thị dữ liệu trực quan, dễ đọc
- ✅ **Xử lý lỗi robust**: Xử lý exception và tự phục hồi

## 🔧 Yêu cầu phần cứng

### Cảm biến
- **PZEM-004t v3.0** - Cảm biến công suất AC với giao tiếp Modbus-RTU
- Dải đo: 80-260V AC, 0-100A, 0-22kW
- Độ chính xác: ±0.5%

### Bộ chuyển đổi
- **USB-to-Serial adapters** được hỗ trợ:
  - PL2303 (Prolific)
  - CH340/CH341 (WCH)
  - CP2102/CP2104 (Silicon Labs)
  - FT232R (FTDI)

### Sơ đồ kết nối
```
PZEM-004t    USB-Serial    Computer
---------    ----------    --------
VCC     ──── 5V/3.3V
GND     ──── GND
TX      ──── RX
RX      ──── TX
                USB   ──── USB Port
```

## 📦 Cài đặt và thiết lập

### Bước 1: Clone repository
```bash
git clone https://github.com/levanduy093-work/ac_management.git
cd ac_management
```

### Bước 2: Cài đặt môi trường

#### Sử dụng pip (Khuyến nghị)
```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

#### Sử dụng Conda
```bash
# Tạo environment mới
conda create --name pzem_env python=3.9
conda activate pzem_env

# Cài đặt packages
conda install pyserial
pip install modbus-tk
```

### Bước 3: Cấp quyền truy cập Serial (Linux)
```bash
# Thêm user vào group dialout
sudo usermod -a -G dialout $USER

# Hoặc cấp quyền cho thiết bị cụ thể
sudo chmod 666 /dev/ttyUSB*
```

## 🚀 Sử dụng

### Chạy chương trình cơ bản
```bash
python3 pzem.py
```

### Tùy chọn chạy nền (background)
```bash
# Sử dụng nohup
nohup python3 pzem.py > pzem.log 2>&1 &

# Sử dụng screen
screen -S pzem
python3 pzem.py
# Ctrl+A, D để detach
```

## 📱 Giao diện và Output

### Màn hình chờ khi không có thiết bị
```
No PZEM devices detected. Waiting...
No PZEM devices detected. Waiting...
```

### Output khi phát hiện thiết bị
```
Found 2 PZEM device(s): ['/dev/ttyUSB0', '/dev/ttyUSB1']

--- Data from /dev/ttyUSB0 ---
  Voltage: 225.4 V
  Current: 0.830 A
  Power: 185.2 W
  Energy: 1547 Wh
  Frequency: 50.0 Hz
  Power Factor: 0.98
  Alarm: OFF
-----------------------------

--- Data from /dev/ttyUSB1 ---
  Voltage: 226.1 V
  Current: 2.150 A
  Power: 485.6 W
  Energy: 3842 Wh
  Frequency: 50.0 Hz
  Power Factor: 0.97
  Alarm: OFF
-----------------------------
```

### Thông báo lỗi và xử lý
```
Attempt 1 failed for /dev/ttyUSB0: [Error 5] Input/output error. Retrying...
Attempt 2 failed for /dev/ttyUSB0: [Error 5] Input/output error. Retrying...
Could not read from /dev/ttyUSB0: [Error 5] Input/output error
```

## ⚙️ Cấu hình nâng cao

### Tùy chỉnh tham số trong code

#### Thay đổi thời gian đọc dữ liệu
```python
# Trong main loop, thay đổi dòng:
time.sleep(1)  # Đọc mỗi 1 giây
# Thành:
time.sleep(5)  # Đọc mỗi 5 giây
```

#### Tùy chỉnh timeout và retry
```python
# Trong hàm read_pzem_data():
max_retries = 3      # Số lần thử lại
timeout=2.0          # Timeout serial
master.set_timeout(3.0)  # Timeout Modbus
```

#### Thêm USB adapter khác
```python
# Trong hàm find_pzem_ports(), thêm keyword:
keywords = ["pl2303", "usb-serial", "ch340", "cp210", "ftdi"]
```

### Cài đặt ngưỡng cảnh báo
```python
# Thêm vào hàm read_pzem_data() để set alarm threshold = 1000W:
# master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=1000)
```

## 🔧 Khắc phục sự cố

### Lỗi thường gặp và cách xử lý

#### 1. "No PZEM devices detected"
**Nguyên nhân:**
- USB adapter chưa được nhận diện
- Driver chưa được cài đặt
- Thiết bị không kết nối

**Giải pháp:**
```bash
# Kiểm tra USB devices
lsusb

# Kiểm tra serial ports
ls -la /dev/ttyUSB*

# Cài driver PL2303 (Ubuntu/Debian)
sudo apt-get install pl2303

# Kiểm tra dmesg khi cắm USB
dmesg | tail
```

#### 2. "Permission denied" trên /dev/ttyUSB*
```bash
# Cấp quyền tạm thời
sudo chmod 666 /dev/ttyUSB0

# Hoặc thêm user vào group dialout (cần logout/login)
sudo usermod -a -G dialout $USER
```

#### 3. "Input/output error" hoặc timeout
**Nguyên nhân:**
- Kết nối loose
- Nhiễu điện từ
- Cấu hình Modbus sai

**Giải pháp:**
- Kiểm tra lại dây kết nối TX/RX
- Sử dụng dây ngắn hơn, có shield
- Thêm capacitor lọc nhiễu
- Tăng timeout trong code

#### 4. Dữ liệu không chính xác
- Kiểm tra địa chỉ Modbus slave (mặc định = 1)
- Verify cảm biến là PZEM-004t v3.0 (không phải v1.0)
- Reset cảm biến về factory default

## 📈 Mở rộng và tùy biến

### Lưu dữ liệu vào file CSV
```python
import csv
from datetime import datetime

def log_to_csv(port, voltage, current, power, energy):
    with open(f'data_{port.replace("/dev/", "")}.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), voltage, current, power, energy])
```

### Gửi dữ liệu qua MQTT
```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mqtt_broker_ip", 1883, 60)

# Trong hàm read_pzem_data():
topic = f"pzem/{port}/voltage"
client.publish(topic, voltage)
```

### REST API endpoint
```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/sensors')
def get_sensors():
    return jsonify(sensor_data)
```

## 🏗️ Cấu trúc dự án

```
ac_management/
├── pzem.py           # Script chính
├── requirements.txt  # Dependencies
├── README.md        # Tài liệu này
└── .git/           # Git repository
```

## 🤝 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository này
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 🙋‍♂️ Liên hệ và hỗ trợ

- **Author**: levanduy093-work
- **Email**: levanduy093.work@gmail.com
- **GitHub**: [@levanduy093-work](https://github.com/levanduy093-work)

### Issues và Bug Reports
Nếu bạn gặp vấn đề, vui lòng tạo issue trên GitHub với thông tin:
- Hệ điều hành và phiên bản Python
- Model cảm biến PZEM chính xác
- Loại USB-Serial adapter
- Log lỗi đầy đủ

## 🔗 Tài liệu tham khảo

- [PZEM-004t v3.0 Datasheet](https://innovatorsguru.com/wp-content/uploads/2019/06/PZEM-004T-V3.0-Datasheet-User-Manual.pdf)
- [Modbus-RTU Protocol](https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf)
- [Python Serial Communication](https://pyserial.readthedocs.io/)
- [Modbus-tk Documentation](https://github.com/ljean/modbus-tk)

---

⭐ **Nếu dự án này hữu ích cho bạn, hãy cho một star trên GitHub!** ⭐