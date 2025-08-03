# Đọc dữ liệu cảm biến PZEM-004t v3.0 với Python

Đây là một script Python để đọc các thông số điện từ cảm biến công suất PZEM-004t (phiên bản v3.0) sử dụng giao thức Modbus-RTU qua kết nối nối tiếp (serial).

## Các thông số đọc được

Script sẽ đọc và hiển thị các thông số sau từ cảm biến:

-   **`Voltage [V]`**: Điện áp (đơn vị Volt).
-   **`Current [A]`**: Dòng điện (đơn vị Ampe).
-   **`Power [W]`**: Công suất tác dụng (đơn vị Watt). Đây là công suất thực tế được tiêu thụ.
-   **`Energy [Wh]`**: Điện năng tiêu thụ (đơn vị Watt-giờ). Đây là tổng lượng điện đã sử dụng theo thời gian.
-   **`Frequency [Hz]`**: Tần số của dòng điện xoay chiều (đơn vị Hertz).
-   **`Power factor []`**: Hệ số công suất. Tỷ lệ giữa công suất tác dụng và công suất biểu kiến. Giá trị từ 0 đến 1.
-   **`Alarm`**: Trạng thái cảnh báo công suất. `0` là bình thường, `1` là có cảnh báo (khi công suất vượt ngưỡng đã cài đặt).

## Yêu cầu phần cứng

1.  Cảm biến [PZEM-004t v3.0](https://www.emall.vn/products/module-do-cong-suat-ac-pzem-004t-v3-0-100a-giao-tiep-modbus-rtu).
2.  Mạch chuyển USB to TTL Serial (ví dụ: PL2303, CP2102, FTDI) để kết nối cảm biến với máy tính.

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

## Cấu hình

1.  Mở file `pzem.py`.
2.  Tìm đến dòng `PORT = '...'`.
3.  Thay đổi giá trị của `PORT` thành cổng serial của bạn.

    Để tìm cổng serial, bạn có thể chạy lệnh sau trong terminal (với môi trường ảo đã được kích hoạt):
    ```bash
    python -m serial.tools.list_ports
    ```
    Kết quả sẽ liệt kê các cổng có sẵn. Chọn cổng tương ứng với mạch chuyển USB to TTL của bạn (ví dụ: `/dev/cu.usbserial-110` trên macOS, `COM3` trên Windows, hoặc `/dev/ttyUSB0` trên Linux).

    Ví dụ:
    ```python
    PORT = '/dev/cu.PL2303-USBtoUART110'
    ```

## Sử dụng

Sau khi đã cài đặt và cấu hình, kết nối cảm biến với máy tính và chạy script bằng lệnh:

```bash
python pzem.py
```

### Ví dụ đầu ra

```
Reading data from sensor...
Voltage [V]:  225.5
Current [A]:  0.23
Power [W]:  45.8
Energy [Wh]:  1567
Frequency [Hz]:  50.0
Power factor []:  0.95
Alarm :  0
Sensor connection closed.
```

## Chức năng nâng cao

### Thay đổi ngưỡng cảnh báo công suất

Script có một đoạn mã đã được chú thích để thay đổi ngưỡng cảnh báo công suất. Để sử dụng, hãy bỏ chú thích các dòng sau trong file `pzem.py`:

```python
# print("Setting alarm threshold to 100W")
# master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)
```

Thay đổi `output_value=100` thành giá trị công suất (W) bạn muốn đặt làm ngưỡng. Sau khi chạy script một lần với đoạn mã này, ngưỡng sẽ được lưu lại trong bộ nhớ của cảm biến. Bạn có thể chú thích lại đoạn mã này trong các lần chạy sau.
