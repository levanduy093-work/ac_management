# 🔌 AC Management - PZEM-004t v3.0 Multi-Sensor Monitor & Data Logger

Một ứng dụng Python chuyên nghiệp để giám sát và ghi dữ liệu từ nhiều cảm biến công suất điện PZEM-004t v3.0 đồng thời sử dụng giao thức Modbus-RTU. Script tự động phát hiện, đọc dữ liệu và lưu trữ vào các file CSV riêng biệt cho từng cảm biến với timestamp chính xác.

## 📊 Thông số giám sát

Script sẽ đọc và hiển thị các thông số điện quan trọng từ mỗi cảm biến:

| Thông số | Đơn vị | Mô tả |
|----------|---------|-------|
| **Voltage** | V | Điện áp AC hiện tại |
| **Current** | A | Dòng điện tiêu thụ |
| **Power** | W | Công suất tác dụng thực tế |
| **Energy** | Wh | Tổng điện năng tiêu thụ tích lũy (không tự reset) |
| **Frequency** | Hz | Tần số nguồn điện (50/60Hz) |
| **Power Factor** | - | Hệ số công suất (0.0 - 1.0) |
| **Alarm** | ON/OFF | Trạng thái cảnh báo ngưỡng công suất |

## 🎯 Tính năng chính

### Giám sát Real-time
- ✅ **Tự động phát hiện cảm biến**: Quét và kết nối tự động với các thiết bị PZEM-004t
- ✅ **Đa cảm biến**: Hỗ trợ đọc từ nhiều cảm biến cùng lúc
- ✅ **Hiển thị dạng bảng**: Dữ liệu từ tất cả cảm biến hiển thị trong bảng thống nhất
- ✅ **Thông tin tổng hợp**: Tính tổng công suất và năng lượng của tất cả cảm biến
- ✅ **Cơ chế retry**: Tự động thử lại khi gặp lỗi kết nối
- ✅ **Tối ưu cho Raspberry Pi**: Cấu hình timeout và buffer phù hợp

### Ghi dữ liệu CSV
- 📝 **File CSV riêng biệt**: Mỗi cảm biến có file CSV riêng với tên dựa trên cổng
- 🕐 **Timestamp chính xác**: Ghi thời gian đo với định dạng YYYY-MM-DD HH:MM:SS
- 📊 **Dữ liệu đầy đủ**: Ghi tất cả thông số bao gồm datetime, port và các giá trị đo
- 🗂️ **Tổ chức khoa học**: Dữ liệu được lưu trong thư mục `data/csv_logs/`
- 📈 **Thống kê real-time**: Hiển thị số lượng records và kích thước file

### Xử lý lỗi & Ổn định
- ✅ **Xử lý lỗi robust**: Xử lý exception và tự phục hồi
- ✅ **Auto-create headers**: Tự động tạo header CSV với format chuẩn
- ✅ **Clear screen**: Làm sạch màn hình mỗi lần cập nhật để dễ theo dõi

## 🗂️ Cấu trúc dự án

```
ac_management/
├── 📜 pzem.py                 # Script chính
├── 📋 requirements.txt        # Dependencies
├── 📖 README.md              # Tài liệu này
├── 📝 DATA_LOGGING.md        # Hướng dẫn chi tiết về CSV logging
└── 📁 data/                  # Thư mục dữ liệu
    └── 📁 csv_logs/          # File CSV logs
        ├── 📊 pzem_dev_ttyUSB0.csv
        ├── 📊 pzem_dev_ttyUSB1.csv
        └── 📊 pzem_dev_ttyUSB2.csv
```

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

## 📱 Giao diện và Output

### Giao diện hiển thị bảng mới (Updated)
```
=== PZEM Sensors Data - 2025-08-04 10:30:15 ===
Found 3 active sensor(s)

┌─────────────────┬──────────────┬──────────────┬───────────┬──────────────┬─────────────────┬──────────────┬───────┐
│ Port            │ Voltage (V)  │ Current (A)  │ Power (W) │ Energy (Wh)  │ Frequency (Hz)  │ Power Factor │ Alarm │
├─────────────────┼──────────────┼──────────────┼───────────┼──────────────┼─────────────────┼──────────────┼───────┤
│ /dev/ttyUSB0    │ 225.4        │ 0.830        │ 185.2     │ 1547         │ 50.0            │ 0.98         │ OFF   │
│ /dev/ttyUSB1    │ 226.1        │ 2.150        │ 485.6     │ 3842         │ 50.0            │ 0.97         │ OFF   │
│ /dev/ttyUSB2    │ 224.8        │ 1.240        │ 278.3     │ 2156         │ 50.1            │ 0.99         │ OFF   │
└─────────────────┴──────────────┴──────────────┴───────────┴──────────────┴─────────────────┴──────────────┴───────┘

=== Summary ===
Total Power: 949.1 W
Total Energy: 7545 Wh

=== CSV Logging ===
  /dev/ttyUSB0: 145 records, 12543 bytes
  /dev/ttyUSB1: 142 records, 12108 bytes
  /dev/ttyUSB2: 144 records, 12387 bytes
==================================================
```

### Màn hình chờ khi không có thiết bị
```
No PZEM devices detected. Waiting...
No PZEM devices detected. Waiting...
```

### Thông báo CSV logging
```
Data saved to CSV for port: /dev/ttyUSB0
Data saved to CSV for port: /dev/ttyUSB1
Data saved to CSV for port: /dev/ttyUSB2
```

### Thông báo lỗi và xử lý
```
Attempt 1 failed for /dev/ttyUSB0: [Error 5] Input/output error. Retrying...
Attempt 2 failed for /dev/ttyUSB0: [Error 5] Input/output error. Retrying...
Could not read from /dev/ttyUSB0: [Error 5] Input/output error
```

## 📊 Quản lý dữ liệu CSV

### Cấu trúc file CSV
Mỗi cảm biến có file CSV riêng với format:
```csv
datetime,port,voltage_v,current_a,power_w,energy_wh,frequency_hz,power_factor,alarm_status
2025-08-04 10:30:00,/dev/ttyUSB0,225.4,0.830,185.2,1547,50.0,0.98,OFF
2025-08-04 10:30:05,/dev/ttyUSB0,225.6,0.835,186.1,1547,50.0,0.98,OFF
2025-08-04 10:30:10,/dev/ttyUSB0,225.2,0.828,184.8,1548,50.0,0.98,OFF
```

### Xem dữ liệu CSV
```bash
# Xem 10 dòng cuối của file CSV
tail -10 data/csv_logs/pzem_dev_ttyUSB0.csv

# Xem toàn bộ file
cat data/csv_logs/pzem_dev_ttyUSB0.csv

# Đếm số dòng dữ liệu (trừ header)
wc -l data/csv_logs/pzem_dev_ttyUSB0.csv
```

### Phân tích dữ liệu với pandas
```python
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu CSV
df = pd.read_csv('data/csv_logs/pzem_dev_ttyUSB0.csv')
df['datetime'] = pd.to_datetime(df['datetime'])

# Thống kê cơ bản
print(df.describe())

# Vẽ biểu đồ công suất theo thời gian
plt.figure(figsize=(12, 6))
plt.plot(df['datetime'], df['power_w'])
plt.title('Power Consumption Over Time')
plt.xlabel('Time')
plt.ylabel('Power (W)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Tính tổng năng lượng tiêu thụ trong ngày
daily_energy = df.groupby(df['datetime'].dt.date)['power_w'].mean() * 24 / 1000  # kWh
print("Daily Energy Consumption (kWh):")
print(daily_energy)
```

### Backup và quản lý dữ liệu
```bash
# Tạo backup dữ liệu với timestamp
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/

# Xóa dữ liệu cũ hơn 30 ngày
find data/csv_logs/ -name "*.csv" -mtime +30 -delete

# Nén dữ liệu cũ
gzip data/csv_logs/*.csv
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
## ⚙️ Cấu hình nâng cao

### Tùy chỉnh tham số trong code

#### Thay đổi thời gian đọc dữ liệu
```python
# Trong main loop, thay đổi dòng:
time.sleep(5)  # Đọc mỗi 5 giây (mặc định)
# Thành:
time.sleep(1)  # Đọc mỗi 1 giây (nhanh hơn)
# hoặc:
time.sleep(10) # Đọc mỗi 10 giây (chậm hơn)
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

### Tùy chỉnh định dạng CSV
```python
# Thay đổi trong hàm ensure_csv_headers() để thêm cột mới:
headers = [
    'datetime', 'port', 'voltage_v', 'current_a', 'power_w',
    'energy_wh', 'frequency_hz', 'power_factor', 'alarm_status',
    'power_kw',  # Thêm cột công suất tính bằng kW
    'daily_cost' # Thêm cột chi phí hàng ngày
]
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

#### 5. File CSV không tạo được
**Nguyên nhân:**
- Không có quyền ghi vào thư mục
- Dung lượng ổ cứng đầy

**Giải pháp:**
```bash
# Kiểm tra quyền thư mục
ls -la data/csv_logs/

# Tạo thư mục với quyền phù hợp
mkdir -p data/csv_logs
chmod 755 data/csv_logs

# Kiểm tra dung lượng ổ cứng
df -h
```

## 📈 Mở rộng và tùy biến

### Thêm tính năng reset Energy
```python
def reset_pzem_energy(port):
    """Reset energy counter của PZEM sensor"""
    try:
        sensor = serial.Serial(port, 9600, timeout=2.0)
        master = modbus_rtu.RtuMaster(sensor)
        # Reset energy register (0x0042 cho PZEM-004t v3.0)
        master.execute(1, cst.WRITE_SINGLE_REGISTER, 0x0042, 1)
        print(f"Energy reset successful for {port}")
        sensor.close()
    except Exception as e:
        print(f"Failed to reset energy for {port}: {e}")
```

### Thêm cảnh báo qua email
```python
import smtplib
from email.mime.text import MIMEText

def send_alert_email(sensor_data):
    """Gửi email cảnh báo khi công suất vượt ngưỡng"""
    if sensor_data['power'] > 1000:  # Ngưỡng 1000W
        msg = MIMEText(f"CẢNH BÁO: Công suất {sensor_data['port']} = {sensor_data['power']}W")
        msg['Subject'] = 'PZEM Power Alert'
        msg['From'] = 'your_email@gmail.com'
        msg['To'] = 'admin@company.com'
        
        # Gửi email (cần cấu hình SMTP)
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.send_message(msg)
```

### Tích hợp với InfluxDB
```python
from influxdb import InfluxDBClient

def save_to_influxdb(sensor_data):
    """Lưu dữ liệu vào InfluxDB để visualize với Grafana"""
    client = InfluxDBClient('localhost', 8086, 'user', 'password', 'pzem_db')
    
    json_body = [{
        "measurement": "power_consumption",
        "tags": {"port": sensor_data['port']},
        "time": sensor_data['timestamp'],
        "fields": {
            "voltage": sensor_data['voltage'],
            "current": sensor_data['current'],
            "power": sensor_data['power'],
            "energy": sensor_data['energy'],
            "frequency": sensor_data['frequency'],
            "power_factor": sensor_data['power_factor']
        }
    }]
    
## 🤝 Đóng góp và phát triển

### Cấu trúc code
- `find_pzem_ports()`: Tự động phát hiện cảm biến PZEM
- `read_pzem_data()`: Đọc dữ liệu từ một cảm biến
- `save_to_csv()`: Lưu dữ liệu vào file CSV riêng biệt
- `display_sensors_table()`: Hiển thị dữ liệu dạng bảng
- `ensure_csv_headers()`: Đảm bảo format CSV đúng chuẩn

### Đóng góp
1. Fork repository này
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

### Roadmap
- [ ] Web interface với Flask/Django
- [ ] Database integration (PostgreSQL, MySQL)
- [ ] REST API endpoints
- [ ] Mobile app companion
- [ ] Advanced analytics và machine learning
- [ ] Multi-site monitoring
- [ ] Cloud integration (AWS IoT, Azure IoT)

## 📄 License

Dự án này được phân phối dưới MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Liên hệ và hỗ trợ

- **Developer**: Lê Văn Duy
- **Email**: levanduy093.work@gmail.com  
- **GitHub**: [@levanduy093-work](https://github.com/levanduy093-work)
- **Repository**: [ac_management](https://github.com/levanduy093-work/ac_management)

### Báo lỗi (Bug Reports)
Nếu bạn gặp lỗi, vui lòng tạo [GitHub Issue](https://github.com/levanduy093-work/ac_management/issues) với thông tin:
- OS và phiên bản Python
- Model USB-to-Serial adapter
- Log lỗi chi tiết
- Các bước tái tạo lỗi

### Feature Requests
Có ý tưởng tính năng mới? Tạo [GitHub Issue](https://github.com/levanduy093-work/ac_management/issues) với label `enhancement`.

---

**⭐ Nếu dự án này hữu ích, đừng quên star repository để ủng hộ developer! ⭐**
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