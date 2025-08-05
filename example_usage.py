#!/usr/bin/env python3
"""
Ví dụ sử dụng thư viện PZEM-004T
==================================

File này chứa các ví dụ thực tế về cách sử dụng thư viện PZEM-004T
cho việc đọc dữ liệu đo điện, cấu hình thiết bị và giám sát.

Các ví dụ bao gồm:
1. Đọc dữ liệu cơ bản
2. Giám sát liên tục với cảnh báo
3. Ghi log dữ liệu
4. Quản lý nhiều thiết bị
5. Cấu hình thiết bị
"""

import time
import csv
import logging
from datetime import datetime
from pzem import PZEM004T

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def example_basic_reading():
    """
    Ví dụ 1: Đọc dữ liệu cơ bản từ PZEM-004T
    """
    print("\n=== Ví dụ 1: Đọc dữ liệu cơ bản ===")
    
    try:
        # Khởi tạo kết nối
        pzem = PZEM004T(port='/dev/ttyUSB0')
        
        # Đọc và hiển thị tất cả giá trị
        pzem.print_measurements()
        
        # Đọc từng giá trị riêng lẻ
        print("\nĐọc từng giá trị:")
        print(f"Điện áp: {pzem.get_voltage():.1f}V")
        print(f"Dòng điện: {pzem.get_current():.3f}A")
        print(f"Công suất: {pzem.get_power():.1f}W")
        print(f"Năng lượng: {pzem.get_energy():.3f}kWh")
        print(f"Tần số: {pzem.get_frequency():.1f}Hz")
        print(f"Hệ số công suất: {pzem.get_power_factor():.2f}")
        print(f"Trạng thái cảnh báo: {'ON' if pzem.get_alarm_status() else 'OFF'}")
        
        pzem.close()
        
    except Exception as e:
        print(f"Lỗi: {e}")

def example_continuous_monitoring():
    """
    Ví dụ 2: Giám sát liên tục với cảnh báo
    """
    print("\n=== Ví dụ 2: Giám sát liên tục ===")
    
    try:
        pzem = PZEM004T(port='/dev/ttyUSB0')
        
        # Thiết lập ngưỡng cảnh báo 1000W
        if pzem.set_power_alarm_threshold(1000):
            print("Đã thiết lập ngưỡng cảnh báo 1000W")
        
        print("Bắt đầu giám sát (Nhấn Ctrl+C để dừng)...")
        
        while True:
            measurements = pzem.get_all_measurements()
            
            # Hiển thị thông tin cơ bản
            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Power: {measurements['power']:6.1f}W | "
                  f"Current: {measurements['current']:5.2f}A | "
                  f"Voltage: {measurements['voltage']:5.1f}V", end='')
            
            # Kiểm tra cảnh báo
            if measurements['alarm_status']:
                print(f"\n⚠️  CẢNH BÁO: Công suất vượt ngưỡng! ({measurements['power']:.1f}W)")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nDừng giám sát...")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if 'pzem' in locals():
            pzem.close()

def example_data_logging():
    """
    Ví dụ 3: Ghi log dữ liệu vào file CSV
    """
    print("\n=== Ví dụ 3: Ghi log dữ liệu ===")
    
    try:
        pzem = PZEM004T(port='/dev/ttyUSB0')
        
        # Tạo file CSV
        filename = f"power_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Timestamp', 'Voltage(V)', 'Current(A)', 'Power(W)', 
                'Energy(kWh)', 'Frequency(Hz)', 'Power_Factor', 'Alarm_Status'
            ])
            
            print(f"Bắt đầu ghi log vào file: {filename}")
            print("Nhấn Ctrl+C để dừng...")
            
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
                        measurements['power_factor'],
                        'ON' if measurements['alarm_status'] else 'OFF'
                    ])
                    file.flush()  # Đảm bảo ghi ngay lập tức
                    
                    print(f"\r[{timestamp}] Power: {measurements['power']:.1f}W", end='')
                    time.sleep(5)  # Ghi log mỗi 5 giây
                    
            except KeyboardInterrupt:
                print(f"\nDừng ghi log. Dữ liệu đã được lưu vào: {filename}")
        
        pzem.close()
        
    except Exception as e:
        print(f"Lỗi: {e}")

def example_multiple_devices():
    """
    Ví dụ 4: Quản lý nhiều thiết bị PZEM-004T
    """
    print("\n=== Ví dụ 4: Quản lý nhiều thiết bị ===")
    
    # Danh sách các thiết bị (thay đổi theo hệ thống của bạn)
    devices_config = [
        {'name': 'Device1', 'port': '/dev/ttyUSB0', 'address': 0x01},
        {'name': 'Device2', 'port': '/dev/ttyUSB1', 'address': 0x02},
        # {'name': 'Device3', 'port': '/dev/ttyUSB2', 'address': 0x03},
    ]
    
    devices = {}
    
    try:
        # Khởi tạo các thiết bị
        for config in devices_config:
            try:
                device = PZEM004T(port=config['port'], address=config['address'])
                devices[config['name']] = device
                print(f"Đã kết nối {config['name']} trên {config['port']}")
            except Exception as e:
                print(f"Lỗi kết nối {config['name']}: {e}")
        
        if not devices:
            print("Không có thiết bị nào được kết nối!")
            return
        
        print(f"\nBắt đầu giám sát {len(devices)} thiết bị...")
        print("Nhấn Ctrl+C để dừng...")
        
        while True:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
            print("-" * 50)
            
            for name, device in devices.items():
                try:
                    measurements = device.get_all_measurements()
                    print(f"{name:10}: Power: {measurements['power']:6.1f}W | "
                          f"Current: {measurements['current']:5.2f}A | "
                          f"Energy: {measurements['energy']:6.3f}kWh")
                except Exception as e:
                    print(f"{name:10}: Lỗi đọc dữ liệu: {e}")
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nDừng giám sát...")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        # Đóng tất cả kết nối
        for device in devices.values():
            try:
                device.close()
            except:
                pass

def example_device_configuration():
    """
    Ví dụ 5: Cấu hình thiết bị
    """
    print("\n=== Ví dụ 5: Cấu hình thiết bị ===")
    
    try:
        pzem = PZEM004T(port='/dev/ttyUSB0')
        
        # Kiểm tra thông tin hiện tại
        print("Thông tin thiết bị hiện tại:")
        current_addr = pzem.get_address()
        current_threshold = pzem.get_power_alarm_threshold()
        
        print(f"Địa chỉ: {current_addr}")
        print(f"Ngưỡng cảnh báo: {current_threshold}W" if current_threshold else "Ngưỡng cảnh báo: Chưa thiết lập")
        
        # Hiển thị menu cấu hình
        while True:
            print("\nMenu cấu hình:")
            print("1. Thay đổi địa chỉ thiết bị")
            print("2. Thiết lập ngưỡng cảnh báo")
            print("3. Reset bộ đếm năng lượng")
            print("4. Xem thông tin thiết bị")
            print("5. Thoát")
            
            choice = input("\nChọn tùy chọn (1-5): ").strip()
            
            if choice == '1':
                try:
                    new_addr = int(input("Nhập địa chỉ mới (1-247): "))
                    if pzem.set_address(new_addr):
                        print(f"Đã thay đổi địa chỉ thành {new_addr}")
                    else:
                        print("Lỗi thay đổi địa chỉ")
                except ValueError:
                    print("Địa chỉ không hợp lệ")
                    
            elif choice == '2':
                try:
                    threshold = int(input("Nhập ngưỡng cảnh báo (1-25000W): "))
                    if pzem.set_power_alarm_threshold(threshold):
                        print(f"Đã thiết lập ngưỡng cảnh báo {threshold}W")
                    else:
                        print("Lỗi thiết lập ngưỡng cảnh báo")
                except ValueError:
                    print("Ngưỡng cảnh báo không hợp lệ")
                    
            elif choice == '3':
                confirm = input("Bạn có chắc muốn reset bộ đếm năng lượng? (y/N): ")
                if confirm.lower() == 'y':
                    if pzem.reset_energy():
                        print("Đã reset bộ đếm năng lượng")
                    else:
                        print("Lỗi reset bộ đếm năng lượng")
                        
            elif choice == '4':
                print("\nThông tin thiết bị:")
                pzem.print_measurements()
                
            elif choice == '5':
                break
                
            else:
                print("Tùy chọn không hợp lệ")
        
        pzem.close()
        
    except Exception as e:
        print(f"Lỗi: {e}")

def example_energy_monitoring():
    """
    Ví dụ 6: Giám sát năng lượng tiêu thụ
    """
    print("\n=== Ví dụ 6: Giám sát năng lượng tiêu thụ ===")
    
    try:
        pzem = PZEM004T(port='/dev/ttyUSB0')
        
        # Lấy giá trị năng lượng ban đầu
        initial_energy = pzem.get_energy()
        start_time = time.time()
        
        print(f"Năng lượng ban đầu: {initial_energy:.3f}kWh")
        print("Bắt đầu giám sát (Nhấn Ctrl+C để dừng)...")
        
        while True:
            current_energy = pzem.get_energy()
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Tính năng lượng tiêu thụ
            consumed_energy = current_energy - initial_energy
            
            # Tính công suất trung bình
            avg_power = (consumed_energy * 1000) / (elapsed_time / 3600) if elapsed_time > 0 else 0
            
            print(f"\r[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Consumed: {consumed_energy:6.3f}kWh | "
                  f"Current: {current_energy:6.3f}kWh | "
                  f"Avg Power: {avg_power:6.1f}W", end='')
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print(f"\nDừng giám sát. Tổng năng lượng tiêu thụ: {consumed_energy:.3f}kWh")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if 'pzem' in locals():
            pzem.close()

def main():
    """
    Menu chính để chọn ví dụ
    """
    print("PZEM-004T Library Examples")
    print("=" * 40)
    
    examples = [
        ("Đọc dữ liệu cơ bản", example_basic_reading),
        ("Giám sát liên tục", example_continuous_monitoring),
        ("Ghi log dữ liệu", example_data_logging),
        ("Quản lý nhiều thiết bị", example_multiple_devices),
        ("Cấu hình thiết bị", example_device_configuration),
        ("Giám sát năng lượng", example_energy_monitoring),
    ]
    
    while True:
        print("\nChọn ví dụ:")
        for i, (name, _) in enumerate(examples, 1):
            print(f"{i}. {name}")
        print("0. Thoát")
        
        try:
            choice = int(input("\nChọn (0-6): "))
            
            if choice == 0:
                print("Tạm biệt!")
                break
            elif 1 <= choice <= len(examples):
                examples[choice - 1][1]()
            else:
                print("Tùy chọn không hợp lệ")
                
        except ValueError:
            print("Vui lòng nhập số")
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break

if __name__ == "__main__":
    main() 