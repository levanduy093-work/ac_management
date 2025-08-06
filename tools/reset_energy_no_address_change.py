#!/usr/bin/env python3
"""
Reset Energy Counter Tool for PZEM-004T Sensors (No Address Change)
==================================================================

Tool để reset bộ đếm năng lượng cho các cảm biến PZEM-004T mà KHÔNG thay đổi địa chỉ.
Giải pháp này sử dụng cơ chế reset tuần tự và cô lập từng thiết bị để tránh xung đột.

Tính năng:
- Tự động phát hiện các thiết bị PZEM-004T
- Reset bộ đếm năng lượng cho từng thiết bị tuần tự
- KHÔNG thay đổi địa chỉ thiết bị
- Xác nhận trước khi reset
- Hiển thị trạng thái reset
- Hỗ trợ nhiều loại USB-to-Serial adapter
"""

import serial
import serial.tools.list_ports
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from pzem import PZEM004T

def find_pzem_ports():
    """
    Quét và trả về danh sách các cổng nối tiếp có vẻ như được kết nối với
    cảm biến PZEM-004t thông qua bộ chuyển đổi USB-to-Serial.
    """
    pzem_ports = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc_lower = port.description.lower() if port.description else ""
        device_lower = port.device.lower()
        hwid_lower = port.hwid.lower() if port.hwid else ""

        keywords = ["pl2303", "usb-serial", "usb serial", "ch340"]
        
        if any(keyword in desc_lower for keyword in keywords) or \
           any(keyword in device_lower for keyword in keywords) or \
           "vid:067b" in hwid_lower:
            pzem_ports.append(port.device)
            
    return pzem_ports

def get_pzem_info(port):
    """
    Lấy thông tin của thiết bị PZEM trên cổng nhất định.
    Trả về tuple (address, energy, is_valid)
    """
    pzem = None
    try:
        pzem = PZEM004T(port=port, timeout=2.0)
        
        # Thử đọc địa chỉ thiết bị
        address = pzem.get_address()
        if address is None:
            address = pzem.DEFAULT_ADDRESS
        
        # Thử đọc năng lượng hiện tại
        measurements = pzem.get_all_measurements()
        energy = measurements.get('energy', 0.0) if measurements else 0.0
        
        return (address, energy, True)
        
    except Exception as e:
        print(f"Không thể kết nối {port}: {e}")
        return (None, 0.0, False)
    finally:
        if pzem:
            pzem.close()

def reset_pzem_isolated(port, target_address=None):
    """
    Reset năng lượng cho thiết bị PZEM với cơ chế cô lập.
    Sử dụng timeout ngắn và retry để tránh xung đột với thiết bị khác.
    """
    pzem = None
    try:
        # Kết nối với timeout ngắn để tránh xung đột
        if target_address is not None:
            pzem = PZEM004T(port=port, address=target_address, timeout=1.0)
        else:
            pzem = PZEM004T(port=port, timeout=1.0)
        
        # Đọc năng lượng trước khi reset
        measurements_before = pzem.get_all_measurements()
        energy_before = measurements_before.get('energy', 0.0) if measurements_before else 0.0
        
        print(f"  Năng lượng trước reset: {energy_before:.3f} kWh")
        
        # Thực hiện reset với retry mechanism
        success = False
        for attempt in range(3):
            try:
                if pzem.reset_energy(verify_reset=False):  # Không verify ngay để tránh xung đột
                    success = True
                    break
                time.sleep(0.2)  # Đợi ngắn giữa các lần thử
            except Exception as e:
                print(f"    Lần thử {attempt + 1} thất bại: {e}")
                time.sleep(0.3)
        
        if not success:
            print(f"❌ Không thể reset sau 3 lần thử trên {port}")
            return False
        
        # Đợi lâu hơn trước khi đọc lại để tránh xung đột
        time.sleep(1.0)
        
        # Đọc lại năng lượng sau reset
        measurements_after = pzem.get_all_measurements()
        energy_after = measurements_after.get('energy', 0.0) if measurements_after else 0.0
        
        print(f"  Năng lượng sau reset: {energy_after:.3f} kWh")
        
        if energy_after < energy_before or energy_after == 0.0:
            print(f"✅ Đã reset thành công bộ đếm năng lượng trên {port} (địa chỉ: {pzem.address})")
            return True
        else:
            print(f"❌ Reset có thể thất bại trên {port} (địa chỉ: {pzem.address})")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi reset {port}: {e}")
        return False
    finally:
        if pzem:
            pzem.close()

def reset_all_pzems_sequential():
    """
    Reset tất cả các thiết bị PZEM theo thứ tự tuần tự để tránh xung đột.
    """
    print("Đang tìm kiếm cảm biến PZEM-004T...")
    detected_ports = find_pzem_ports()
    
    if not detected_ports:
        print("Không phát hiện thấy thiết bị PZEM nào. Vui lòng kiểm tra kết nối và driver.")
        return
    
    print(f"Đã tìm thấy {len(detected_ports)} thiết bị PZEM: {detected_ports}")
    
    # Thu thập thông tin từ tất cả thiết bị
    devices_info = []
    for port in detected_ports:
        print(f"\nĐang kiểm tra thiết bị trên {port}...")
        address, energy, is_valid = get_pzem_info(port)
        if is_valid:
            devices_info.append({
                'port': port,
                'address': address,
                'energy': energy
            })
            print(f"  Địa chỉ: {address}, Năng lượng: {energy:.3f} kWh")
        else:
            print(f"  Không thể kết nối với thiết bị trên {port}")
    
    if not devices_info:
        print("Không có thiết bị PZEM hợp lệ nào được tìm thấy.")
        return
    
    # Kiểm tra xung đột địa chỉ
    addresses = [dev['address'] for dev in devices_info]
    duplicate_addresses = [addr for addr in set(addresses) if addresses.count(addr) > 1]
    
    if duplicate_addresses:
        print(f"\n⚠️  Phát hiện xung đột địa chỉ: {duplicate_addresses}")
        print("Các thiết bị có cùng địa chỉ sẽ được reset tuần tự để tránh xung đột.")
        print("Lưu ý: KHÔNG thay đổi địa chỉ thiết bị để tránh ảnh hưởng đến cấu hình.")
        
        # Reset tuần tự với thời gian chờ dài hơn
        print("\n🔄 Thực hiện reset tuần tự...")
        success_count = 0
        
        for i, device in enumerate(devices_info, 1):
            print(f"\n--- [{i}/{len(devices_info)}] Reset thiết bị trên {device['port']} (địa chỉ: {device['address']}) ---")
            if reset_pzem_isolated(device['port'], device['address']):
                success_count += 1
            
            # Đợi lâu hơn giữa các thiết bị có cùng địa chỉ
            if device['address'] in duplicate_addresses:
                print(f"  ⏳ Đợi 2 giây trước khi reset thiết bị tiếp theo...")
                time.sleep(2.0)
            else:
                print(f"  ⏳ Đợi 1 giây trước khi reset thiết bị tiếp theo...")
                time.sleep(1.0)
        
        print(f"\n📊 Kết quả: {success_count}/{len(devices_info)} thiết bị được reset thành công")
        
    else:
        print("\n✅ Không có xung đột địa chỉ. Tiến hành reset tất cả thiết bị...")
        success_count = 0
        
        for i, device in enumerate(devices_info, 1):
            print(f"\n--- [{i}/{len(devices_info)}] Reset thiết bị trên {device['port']} (địa chỉ: {device['address']}) ---")
            if reset_pzem_isolated(device['port'], device['address']):
                success_count += 1
            time.sleep(0.5)  # Đợi ngắn hơn khi không có xung đột
        
        print(f"\n📊 Kết quả: {success_count}/{len(devices_info)} thiết bị được reset thành công")

def reset_single_pzem(port):
    """
    Reset một thiết bị PZEM cụ thể.
    """
    print(f"Đang reset thiết bị PZEM trên {port}...")
    
    # Kiểm tra thông tin thiết bị
    address, energy, is_valid = get_pzem_info(port)
    if not is_valid:
        print(f"Không thể kết nối với thiết bị trên {port}")
        return False
    
    print(f"Thông tin thiết bị:")
    print(f"  Cổng: {port}")
    print(f"  Địa chỉ: {address}")
    print(f"  Năng lượng hiện tại: {energy:.3f} kWh")
    
    # Xác nhận từ người dùng
    confirm = input(f"\nBạn có chắc chắn muốn reset thiết bị trên {port}? (y/N): ")
    if confirm.lower() != 'y':
        print("Đã hủy reset.")
        return False
    
    # Thực hiện reset
    return reset_pzem_isolated(port, address)

def interactive_menu():
    """
    Menu tương tác cho người dùng.
    """
    while True:
        print("\n" + "="*60)
        print("🔌 PZEM-004T Energy Reset Tool (No Address Change)")
        print("="*60)
        print("📋 Menu:")
        print("1. Reset tất cả thiết bị (có xác nhận)")
        print("2. Reset tất cả thiết bị (không xác nhận)")
        print("3. Reset từng thiết bị (xác nhận từng cái)")
        print("4. Quét lại thiết bị")
        print("5. Thoát")
        print("\n💡 Lưu ý: Tool này KHÔNG thay đổi địa chỉ thiết bị!")
        
        choice = input("\nChọn tùy chọn (1-5): ").strip()
        
        if choice == '1':
            confirm = input("Bạn có chắc chắn muốn reset TẤT CẢ thiết bị? (y/N): ")
            if confirm.lower() == 'y':
                reset_all_pzems_sequential()
            else:
                print("Đã hủy reset.")
                
        elif choice == '2':
            reset_all_pzems_sequential()
            
        elif choice == '3':
            detected_ports = find_pzem_ports()
            if not detected_ports:
                print("Không phát hiện thấy thiết bị PZEM nào.")
                continue
                
            print(f"\nCác thiết bị có sẵn: {detected_ports}")
            port_choice = input("Nhập cổng muốn reset (hoặc 'all' để reset tất cả): ").strip()
            
            if port_choice.lower() == 'all':
                for port in detected_ports:
                    reset_single_pzem(port)
            elif port_choice in detected_ports:
                reset_single_pzem(port_choice)
            else:
                print("Cổng không hợp lệ.")
                
        elif choice == '4':
            detected_ports = find_pzem_ports()
            print(f"Đã tìm thấy {len(detected_ports)} thiết bị: {detected_ports}")
            
        elif choice == '5':
            print("Tạm biệt!")
            break
            
        else:
            print("Tùy chọn không hợp lệ. Vui lòng chọn 1-5.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Chế độ command line
        if sys.argv[1] == "--all":
            reset_all_pzems_sequential()
        elif sys.argv[1] == "--port" and len(sys.argv) > 2:
            reset_single_pzem(sys.argv[2])
        else:
            print("Sử dụng:")
            print("  python reset_energy_no_address_change.py --all          # Reset tất cả thiết bị")
            print("  python reset_energy_no_address_change.py --port PORT    # Reset thiết bị cụ thể")
    else:
        # Chế độ tương tác
        interactive_menu() 