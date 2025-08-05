#!/usr/bin/env python3
"""
Reset Energy Counter Tool for PZEM-004T Sensors
===============================================

Tool để reset bộ đếm năng lượng cho các cảm biến PZEM-004T.
Hỗ trợ reset cho nhiều thiết bị cùng lúc với xác nhận người dùng.

Tính năng:
- Tự động phát hiện các thiết bị PZEM-004T
- Reset bộ đếm năng lượng cho từng thiết bị
- Xác nhận trước khi reset
- Hiển thị trạng thái reset
- Hỗ trợ nhiều loại USB-to-Serial adapter
"""

import serial
import serial.tools.list_ports
import time
from pzem import PZEM004T

def find_pzem_ports():
    """
    Quét và trả về danh sách các cổng nối tiếp có vẻ như được kết nối với
    cảm biến PZEM-004T thông qua bộ chuyển đổi USB-to-Serial.
    """
    pzem_ports = []
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        # Kiểm tra không phân biệt chữ hoa chữ thường và tổng quát hơn.
        desc_lower = port.description.lower() if port.description else ""
        device_lower = port.device.lower()
        hwid_lower = port.hwid.lower() if port.hwid else ""

        # Hỗ trợ nhiều loại USB-to-Serial adapter
        keywords = ["pl2303", "usb-serial", "usb serial", "ch340", "cp210", "ftdi"]
        
        if any(keyword in desc_lower for keyword in keywords) or \
           any(keyword in device_lower for keyword in keywords) or \
           "vid:067b" in hwid_lower:  # Kiểm tra Prolific Vendor ID
            pzem_ports.append(port.device)
            
    return pzem_ports

def get_device_info(port):
    """
    Lấy thông tin thiết bị trước khi reset
    """
    pzem = None
    try:
        pzem = PZEM004T(port=port, timeout=2.0)
        
        # Đọc thông tin thiết bị
        measurements = pzem.get_all_measurements()
        address = pzem.get_address()
        
        if measurements:
            return {
                'address': address,
                'energy': measurements['energy'],
                'power': measurements['power'],
                'voltage': measurements['voltage'],
                'current': measurements['current']
            }
        else:
            return None
            
    except Exception as e:
        print(f"Không thể đọc thông tin từ {port}: {e}")
        return None
    finally:
        if pzem:
            pzem.close()

def reset_pzem_energy(port, confirm=True):
    """
    Kết nối với cảm biến PZEM trên một cổng nhất định và reset lại bộ đếm năng lượng của nó.
    
    Args:
        port (str): Cổng serial của thiết bị
        confirm (bool): Có yêu cầu xác nhận không
    
    Returns:
        bool: True nếu reset thành công, False nếu thất bại
    """
    pzem = None
    try:
        # Lấy thông tin thiết bị trước khi reset
        device_info = get_device_info(port)
        
        if device_info:
            print(f"\nThông tin thiết bị {port}:")
            print(f"  Địa chỉ: {device_info['address']}")
            print(f"  Năng lượng hiện tại: {device_info['energy']:.3f} kWh")
            print(f"  Công suất: {device_info['power']:.1f} W")
            print(f"  Điện áp: {device_info['voltage']:.1f} V")
            print(f"  Dòng điện: {device_info['current']:.3f} A")
            
            if confirm:
                response = input(f"\nBạn có chắc muốn reset bộ đếm năng lượng trên {port}? (y/N): ")
                if response.lower() != 'y':
                    print(f"Bỏ qua reset cho {port}")
                    return False
        
        # Thực hiện reset
        pzem = PZEM004T(port=port, timeout=2.0)
        
        if pzem.reset_energy():
            print(f"✅ Đã reset thành công bộ đếm năng lượng trên {port}")
            
            # Đọc lại thông tin sau khi reset
            time.sleep(1)
            new_measurements = pzem.get_all_measurements()
            if new_measurements:
                print(f"   Năng lượng sau reset: {new_measurements['energy']:.3f} kWh")
            
            return True
        else:
            print(f"❌ Không thể reset bộ đếm năng lượng trên {port}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi kết nối hoặc reset {port}: {e}")
        return False
    finally:
        if pzem:
            pzem.close()

def reset_all_devices(confirm_each=True, confirm_all=True):
    """
    Reset tất cả thiết bị PZEM được phát hiện
    
    Args:
        confirm_each (bool): Xác nhận cho từng thiết bị
        confirm_all (bool): Xác nhận trước khi reset tất cả
    """
    print("🔍 Đang tìm kiếm cảm biến PZEM-004T...")
    detected_ports = find_pzem_ports()
    
    if not detected_ports:
        print("❌ Không phát hiện thấy thiết bị PZEM nào.")
        print("💡 Vui lòng kiểm tra:")
        print("   - Kết nối USB-to-Serial adapter")
        print("   - Driver đã được cài đặt")
        print("   - Quyền truy cập cổng serial")
        return
    
    print(f"✅ Đã tìm thấy {len(detected_ports)} thiết bị PZEM: {detected_ports}")
    
    if confirm_all and len(detected_ports) > 1:
        print(f"\n⚠️  Bạn sắp reset {len(detected_ports)} thiết bị:")
        for i, port in enumerate(detected_ports, 1):
            print(f"   {i}. {port}")
        
        response = input(f"\nBạn có chắc muốn reset tất cả {len(detected_ports)} thiết bị? (y/N): ")
        if response.lower() != 'y':
            print("❌ Đã hủy reset tất cả thiết bị.")
            return
    
    # Reset từng thiết bị
    success_count = 0
    for i, port in enumerate(detected_ports, 1):
        print(f"\n📊 [{i}/{len(detected_ports)}] Đang xử lý thiết bị {port}...")
        
        if reset_pzem_energy(port, confirm=confirm_each):
            success_count += 1
        
        time.sleep(0.5)  # Độ trễ nhỏ giữa các thiết bị
    
    # Tóm tắt kết quả
    print(f"\n📋 Tóm tắt kết quả:")
    print(f"   Tổng thiết bị: {len(detected_ports)}")
    print(f"   Reset thành công: {success_count}")
    print(f"   Reset thất bại: {len(detected_ports) - success_count}")

def main():
    """
    Hàm chính với menu tương tác
    """
    print("🔌 PZEM-004T Energy Reset Tool")
    print("=" * 40)
    
    while True:
        print("\n📋 Menu:")
        print("1. Reset tất cả thiết bị (có xác nhận)")
        print("2. Reset tất cả thiết bị (không xác nhận)")
        print("3. Reset từng thiết bị (xác nhận từng cái)")
        print("4. Quét lại thiết bị")
        print("5. Thoát")
        
        try:
            choice = input("\nChọn tùy chọn (1-5): ").strip()
            
            if choice == '1':
                reset_all_devices(confirm_each=True, confirm_all=True)
            elif choice == '2':
                reset_all_devices(confirm_each=False, confirm_all=True)
            elif choice == '3':
                reset_all_devices(confirm_each=True, confirm_all=False)
            elif choice == '4':
                detected_ports = find_pzem_ports()
                if detected_ports:
                    print(f"✅ Tìm thấy {len(detected_ports)} thiết bị: {detected_ports}")
                else:
                    print("❌ Không tìm thấy thiết bị nào.")
            elif choice == '5':
                print("👋 Tạm biệt!")
                break
            else:
                print("❌ Tùy chọn không hợp lệ. Vui lòng chọn 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")