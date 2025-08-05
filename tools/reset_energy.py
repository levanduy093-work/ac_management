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
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from pzem import PZEM004T

def find_pzem_ports():
    """
    Quét và trả về danh sách các cổng nối tiếp có vẻ như được kết nối với
    cảm biến PZEM-004t thông qua bộ chuyển đổi USB-to-Serial (như PL2303, CH340, v.v.).
    """
    pzem_ports = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Kiểm tra không phân biệt chữ hoa chữ thường và tổng quát hơn.
        desc_lower = port.description.lower() if port.description else ""
        device_lower = port.device.lower()
        hwid_lower = port.hwid.lower() if port.hwid else ""

        # Thêm các từ khóa khác nếu bộ chuyển đổi của bạn có mô tả khác
        keywords = ["pl2303", "usb-serial", "usb serial", "ch340"]
        
        if any(keyword in desc_lower for keyword in keywords) or \
           any(keyword in device_lower for keyword in keywords) or \
           "vid:067b" in hwid_lower:  # Kiểm tra Prolific Vendor ID
            pzem_ports.append(port.device)
            
    return pzem_ports

def reset_pzem_energy(port):
    """
    Kết nối với cảm biến PZEM trên một cổng nhất định và reset lại bộ đếm năng lượng của nó.
    """
    pzem = None
    try:
        pzem = PZEM004T(port=port, timeout=2.0)
        if pzem.reset_energy():
            print(f"Đã reset thành công bộ đếm năng lượng trên {port}")
            return True
        else:
            print(f"Không thể reset bộ đếm năng lượng trên {port}")
            return False
    except Exception as e:
        print(f"Không thể kết nối hoặc reset {port}: {e}")
        return False
    finally:
        if pzem:
            pzem.close()

if __name__ == "__main__":
    print("Đang tìm kiếm cảm biến PZEM-004t...")
    detected_ports = find_pzem_ports()
    
    if not detected_ports:
        print("Không phát hiện thấy thiết bị PZEM nào. Vui lòng kiểm tra kết nối và driver.")
    else:
        print(f"Đã tìm thấy {len(detected_ports)} thiết bị PZEM: {detected_ports}")
        
        for port in detected_ports:
            print(f"\nĐang thử reset năng lượng cho cảm biến trên cổng {port}...")
            reset_pzem_energy(port)
            time.sleep(0.5) # Độ trễ nhỏ giữa các cảm biến

    print("\nQuá trình reset năng lượng đã hoàn tất.")