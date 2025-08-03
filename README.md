# Đọc dữ liệu từ nhiều cảm biến PZEM-004t v3.0 với Python

Đây là một script Python để đọc đồng thời các thông số điện từ nhiều cảm biến công suất PZEM-004t (phiên bản v3.0) sử dụng giao thức Modbus-RTU qua kết nối nối tiếp (serial). Script sẽ tự động phát hiện các bộ chuyển đổi USB-to-Serial (như PL2303, CH340) và đọc dữ liệu từ mỗi cảm biến mỗi giây một lần.

## Các thông số đọc được

Script sẽ đọc và hiển thị các thông số sau từ mỗi cảm biến:

-   **`Voltage [V]`**: Điện áp (đơn vị Volt).
-   **`Current [A]`**: Dòng điện (đơn vị Ampe).
-   **`Power [W]`**: Công suất tác dụng (đơn vị Watt). Đây là công suất thực tế được tiêu thụ.
-   **`Energy [Wh]`**: Điện năng tiêu thụ (đơn vị Watt-giờ). Đây là tổng lượng điện đã sử dụng theo thời gian.
-   **`Frequency [Hz]`**: Tần số của dòng điện xoay chiều (đơn vị Hertz).
-   **`Power factor []`**: Hệ số công suất. Tỷ lệ giữa công suất tác dụng và công suất biểu kiến. Giá trị từ 0 đến 1.
-   **`Alarm`**: Trạng thái cảnh báo công suất. `ON` là có cảnh báo, `OFF` là bình thường.

## Yêu cầu phần cứng

1.  Một hoặc nhiều cảm biến [PZEM-004t v3.0](https://www.emall.vn/products/module-do-cong-suat-ac-pzem-004t-v3-0-100a-giao-tiep-modbus-rtu).
2.  Các mạch chuyển USB to TTL Serial tương ứng (ví dụ: PL2303, CP2102, FTDI) để kết nối mỗi cảm biến với máy tính.

## Cài đặt môi trường

Script này yêu cầu Python 3. Khuyến khích sử dụng môi trường ảo để quản lý các thư viện.

### Sử dụng Conda (Khuyến nghị)

1.  Tạo và kích hoạt môi trường mới (tùy chọn nhưng được khuyến nghị):
    ```bash
    conda create --name pzem_env python=3.9
    conda activate pzem_env
    ```

2.  Cài đặt các thư viện cần thiết:
    ```bash
    conda install pyserial
    pip install modbus-tk
    ```

### Sử dụng venv

1.  Tạo và kích hoạt môi trường ảo:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # Trên Windows, dùng: venv\Scripts\activate
    ```

2.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install pyserial modbus-tk
    ```

## Sử dụng

Sau khi đã cài đặt môi trường, kết nối các cảm biến với máy tính và chạy script bằng lệnh:

```bash
python pzem.py
```

Script sẽ tự động quét và tìm các cổng serial có kết nối với bộ chuyển đổi USB-to-Serial và bắt đầu đọc dữ liệu từ chúng.

### Ví dụ đầu ra

```
Starting PZEM-004t multi-sensor monitoring script...
Press Ctrl+C to stop.
Scanning for available serial ports...
  - Found port: /dev/ttyS0, desc: ttyS0, hwid: PNP0501
  - Found port: /dev/ttyUSB0, desc: USB-Serial Controller, hwid: USB VID:PID=067B:2303 SER= LOCATION=1-1.2:1.0
  - Found port: /dev/ttyUSB1, desc: USB-Serial Controller, hwid: USB VID:PID=067B:2303 SER= LOCATION=1-1.4:1.0
    -> Matched PZEM-like device: /dev/ttyUSB0
    -> Matched PZEM-like device: /dev/ttyUSB1

Found devices on ports: /dev/ttyUSB0, /dev/ttyUSB1
--- Data from /dev/ttyUSB0 ---
  Voltage: 225.5 V
  Current: 0.230 A
  Power: 45.8 W
  Energy: 1567 Wh
  Frequency: 50.0 Hz
  Power Factor: 0.95
  Alarm: OFF
----------------------------------
--- Data from /dev/ttyUSB1 ---
  Voltage: 226.1 V
  Current: 1.510 A
  Power: 330.2 W
  Energy: 2450 Wh
  Frequency: 50.0 Hz
  Power Factor: 0.97
  Alarm: OFF
----------------------------------
```

## Chức năng nâng cao

### Thay đổi ngưỡng cảnh báo công suất

Script gốc có một đoạn mã đã được chú thích để thay đổi ngưỡng cảnh báo công suất. Trong phiên bản đa cảm biến này, bạn sẽ cần sửa đổi hàm `read_pzem_data` để gửi lệnh ghi tới một cảm biến cụ thể.

Ví dụ, để đặt ngưỡng 100W cho cảm biến trên cổng `port`:
```python
# master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)
```
Bạn có thể thêm logic để chỉ thực hiện việc này một lần hoặc dựa trên một điều kiện nhất định bên trong