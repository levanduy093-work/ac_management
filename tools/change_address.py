#!/usr/bin/env python3
"""
Change PZEM-004T Device Address Tool
====================================

Tool để thay đổi địa chỉ của các thiết bị PZEM-004T để tránh xung đột
khi có nhiều thiết bị được kết nối cùng lúc.

Tính năng:
- Tự động phát hiện các thiết bị PZEM-004T
- Hiển thị địa chỉ hiện tại của từng thiết bị
- Thay đổi địa chỉ cho từng thiết bị
- Tự động gán địa chỉ duy nhất
- Xác nhận trước khi thay đổi
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

def get_pzem_address(port):
    """
    Lấy địa chỉ hiện tại của thiết bị PZEM trên cổng nhất định.
    """
    pzem = None
    try:
        pzem = PZEM004T(port=port, timeout=2.0)
        address = pzem.get_address()
        if address is None:
            address = pzem.DEFAULT_ADDRESS
        return address
    except Exception as e:
        print(f"Không thể đọc địa chỉ từ {port}: {e}")
        return None
    finally:
        if pzem:
            pzem.close()

def change_pzem_address(port, old_address, new_address):
    """
    Thay đổi địa chỉ của thiết bị PZEM.
    """
    pzem = None
    try:
        # Kết nối với địa chỉ cũ
        pzem = PZEM004T(port=port, address=old_address, timeout=2.0)
        
        # Thay đổi địa chỉ
        if pzem.set_address(new_address):
            print(f"✅ Đã thay đổi địa chỉ từ {old_address} thành {new_address} trên {port}")
            
            # Đóng kết nối cũ và thử kết nối với địa chỉ mới
            pzem.close()
            time.sleep(0.5)
            
            # Thử kết nối với địa chỉ mới để xác nhận
            pzem = PZEM004T(port=port, address=new_address, timeout=2.0)
            current_address = pzem.get_address()
            if current_address == new_address:
                print(f"✅ Xác nhận: Địa chỉ mới {new_address} hoạt động trên {port}")
                return True
            else:
                print(f"❌ Lỗi: Không thể xác nhận địa chỉ mới trên {port}")
                return False
        else:
            print(f"❌ Không thể thay đổi địa chỉ trên {port}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi thay đổi địa chỉ trên {port}: {e}")
        return False
    finally:
        if pzem:
            pzem.close()

def scan_devices():
    """
    Quét và hiển thị thông tin tất cả các thiết bị PZEM.
    """
    print("Đang quét các thiết bị PZEM-004T...")
    detected_ports = find_pzem_ports()
    
    if not detected_ports:
        print("Không phát hiện thấy thiết bị PZEM nào.")
        return []
    
    print(f"Đã tìm thấy {len(detected_ports)} thiết bị:")
    
    devices_info = []
    for i, port in enumerate(detected_ports, 1):
        address = get_pzem_address(port)
        if address is not None:
            devices_info.append({
                'port': port,
                'address': address
            })
            print(f"  {i}. {port} - Địa chỉ: {address}")
        else:
            print(f"  {i}. {port} - Không thể đọc địa chỉ")
    
    return devices_info

def auto_assign_addresses():
    """
    Tự động gán địa chỉ duy nhất cho tất cả thiết bị.
    """
    devices_info = scan_devices()
    if not devices_info:
        return
    
    # Kiểm tra xung đột địa chỉ
    addresses = [dev['address'] for dev in devices_info]
    duplicate_addresses = [addr for addr in set(addresses) if addresses.count(addr) > 1]
    
    if not duplicate_addresses:
        print("\n✅ Không có xung đột địa chỉ. Tất cả thiết bị đã có địa chỉ duy nhất.")
        return
    
    print(f"\n⚠️  Phát hiện xung đột địa chỉ: {duplicate_addresses}")
    print("Đang tự động gán địa chỉ duy nhất...")
    
    # Danh sách địa chỉ có thể sử dụng (1-247, trừ 248 là địa chỉ mặc định)
    available_addresses = list(range(1, 248))
    available_addresses.remove(248)  # Loại bỏ địa chỉ mặc định
    
    # Loại bỏ các địa chỉ đã được sử dụng
    used_addresses = set(addresses)
    for addr in used_addresses:
        if addr in available_addresses:
            available_addresses.remove(addr)
    
    # Gán địa chỉ mới cho các thiết bị có xung đột
    success_count = 0
    for device in devices_info:
        if device['address'] in duplicate_addresses:
            if available_addresses:
                new_address = available_addresses.pop(0)
                print(f"\nĐang thay đổi địa chỉ cho {device['port']}...")
                if change_pzem_address(device['port'], device['address'], new_address):
                    success_count += 1
                    device['address'] = new_address
                time.sleep(1.0)  # Đợi giữa các thay đổi
            else:
                print(f"❌ Không còn địa chỉ khả dụng cho {device['port']}")
    
    print(f"\n📊 Kết quả: {success_count} thiết bị được thay đổi địa chỉ thành công")
    
    # Hiển thị thông tin cuối cùng
    print("\nThông tin thiết bị sau khi thay đổi:")
    for device in devices_info:
        print(f"  {device['port']} - Địa chỉ: {device['address']}")

def manual_change_address():
    """
    Thay đổi địa chỉ thủ công cho một thiết bị cụ thể.
    """
    devices_info = scan_devices()
    if not devices_info:
        return
    
    print(f"\nCác thiết bị có sẵn:")
    for i, device in enumerate(devices_info, 1):
        print(f"  {i}. {device['port']} - Địa chỉ hiện tại: {device['address']}")
    
    try:
        choice = int(input("\nChọn thiết bị (số): ")) - 1
        if choice < 0 or choice >= len(devices_info):
            print("Lựa chọn không hợp lệ.")
            return
        
        device = devices_info[choice]
        new_address = int(input(f"Nhập địa chỉ mới (1-247, hiện tại: {device['address']}): "))
        
        if new_address < 1 or new_address > 247:
            print("Địa chỉ phải từ 1 đến 247.")
            return
        
        if new_address == device['address']:
            print("Địa chỉ mới giống địa chỉ hiện tại.")
            return
        
        confirm = input(f"Xác nhận thay đổi địa chỉ từ {device['address']} thành {new_address}? (y/N): ")
        if confirm.lower() == 'y':
            if change_pzem_address(device['port'], device['address'], new_address):
                print("✅ Thay đổi địa chỉ thành công!")
            else:
                print("❌ Thay đổi địa chỉ thất bại!")
        else:
            print("Đã hủy thay đổi địa chỉ.")
            
    except ValueError:
        print("Giá trị không hợp lệ.")
    except KeyboardInterrupt:
        print("\nĐã hủy thao tác.")

def interactive_menu():
    """
    Menu tương tác cho người dùng.
    """
    while True:
        print("\n" + "="*50)
        print("🔧 PZEM-004T Address Management Tool")
        print("="*50)
        print("📋 Menu:")
        print("1. Quét và hiển thị thiết bị")
        print("2. Tự động gán địa chỉ duy nhất")
        print("3. Thay đổi địa chỉ thủ công")
        print("4. Thoát")
        
        choice = input("\nChọn tùy chọn (1-4): ").strip()
        
        if choice == '1':
            scan_devices()
            
        elif choice == '2':
            auto_assign_addresses()
            
        elif choice == '3':
            manual_change_address()
            
        elif choice == '4':
            print("Tạm biệt!")
            break
            
        else:
            print("Tùy chọn không hợp lệ. Vui lòng chọn 1-4.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Chế độ command line
        if sys.argv[1] == "--scan":
            scan_devices()
        elif sys.argv[1] == "--auto":
            auto_assign_addresses()
        elif sys.argv[1] == "--change" and len(sys.argv) > 3:
            port = sys.argv[2]
            try:
                new_address = int(sys.argv[3])
                old_address = get_pzem_address(port)
                if old_address is not None:
                    change_pzem_address(port, old_address, new_address)
                else:
                    print(f"Không thể đọc địa chỉ từ {port}")
            except ValueError:
                print("Địa chỉ phải là số nguyên.")
        else:
            print("Sử dụng:")
            print("  python change_address.py --scan                    # Quét thiết bị")
            print("  python change_address.py --auto                    # Tự động gán địa chỉ")
            print("  python change_address.py --change PORT ADDRESS    # Thay đổi địa chỉ")
    else:
        # Chế độ tương tác
        interactive_menu() 