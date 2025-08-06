#!/usr/bin/env python3
"""
Test Multi-Device PZEM Reset
============================

Script test để demo việc reset energy với nhiều thiết bị PZEM-004T.
Script này sẽ:
1. Quét tất cả thiết bị PZEM
2. Hiển thị thông tin từng thiết bị
3. Kiểm tra xung đột địa chỉ
4. Thực hiện reset energy
5. Báo cáo kết quả
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from reset_energy import find_pzem_ports, get_pzem_info, reset_pzem_energy_specific
from change_address import scan_devices, auto_assign_addresses

def test_multi_device_reset():
    """
    Test reset energy với nhiều thiết bị PZEM.
    """
    print("🧪 Test Multi-Device PZEM Reset")
    print("=" * 50)
    
    # Bước 1: Quét thiết bị
    print("\n1️⃣ Quét thiết bị PZEM...")
    detected_ports = find_pzem_ports()
    
    if not detected_ports:
        print("❌ Không phát hiện thấy thiết bị PZEM nào.")
        return
    
    print(f"✅ Đã tìm thấy {len(detected_ports)} thiết bị: {detected_ports}")
    
    # Bước 2: Thu thập thông tin thiết bị
    print("\n2️⃣ Thu thập thông tin thiết bị...")
    devices_info = []
    for port in detected_ports:
        print(f"\nĐang kiểm tra {port}...")
        address, energy, is_valid = get_pzem_info(port)
        if is_valid:
            devices_info.append({
                'port': port,
                'address': address,
                'energy': energy
            })
            print(f"  ✅ Địa chỉ: {address}, Năng lượng: {energy:.3f} kWh")
        else:
            print(f"  ❌ Không thể kết nối với {port}")
    
    if not devices_info:
        print("❌ Không có thiết bị PZEM hợp lệ nào.")
        return
    
    # Bước 3: Kiểm tra xung đột địa chỉ
    print("\n3️⃣ Kiểm tra xung đột địa chỉ...")
    addresses = [dev['address'] for dev in devices_info]
    duplicate_addresses = [addr for addr in set(addresses) if addresses.count(addr) > 1]
    
    if duplicate_addresses:
        print(f"⚠️  Phát hiện xung đột địa chỉ: {duplicate_addresses}")
        print("🔄 Đang tự động gán địa chỉ duy nhất...")
        auto_assign_addresses()
        
        # Thu thập lại thông tin sau khi thay đổi địa chỉ
        print("\n🔄 Thu thập lại thông tin sau khi thay đổi địa chỉ...")
        devices_info = []
        for port in detected_ports:
            address, energy, is_valid = get_pzem_info(port)
            if is_valid:
                devices_info.append({
                    'port': port,
                    'address': address,
                    'energy': energy
                })
                print(f"  {port} - Địa chỉ: {address}, Năng lượng: {energy:.3f} kWh")
    else:
        print("✅ Không có xung đột địa chỉ.")
    
    # Bước 4: Thực hiện reset energy
    print("\n4️⃣ Thực hiện reset energy...")
    success_count = 0
    
    for device in devices_info:
        print(f"\n--- Reset thiết bị trên {device['port']} (địa chỉ: {device['address']}) ---")
        if reset_pzem_energy_specific(device['port'], device['address']):
            success_count += 1
    
    # Bước 5: Báo cáo kết quả
    print("\n5️⃣ Báo cáo kết quả")
    print("=" * 30)
    print(f"📊 Tổng thiết bị: {len(devices_info)}")
    print(f"✅ Reset thành công: {success_count}")
    print(f"❌ Reset thất bại: {len(devices_info) - success_count}")
    
    if success_count == len(devices_info):
        print("\n🎉 Tất cả thiết bị đã được reset thành công!")
    elif success_count > 0:
        print(f"\n⚠️  {success_count}/{len(devices_info)} thiết bị được reset thành công.")
    else:
        print("\n❌ Không có thiết bị nào được reset thành công.")

def test_single_device_reset(port):
    """
    Test reset energy cho một thiết bị cụ thể.
    """
    print(f"🧪 Test Single Device Reset - {port}")
    print("=" * 40)
    
    # Kiểm tra thông tin thiết bị
    address, energy, is_valid = get_pzem_info(port)
    if not is_valid:
        print(f"❌ Không thể kết nối với {port}")
        return False
    
    print(f"📋 Thông tin thiết bị:")
    print(f"  Cổng: {port}")
    print(f"  Địa chỉ: {address}")
    print(f"  Năng lượng hiện tại: {energy:.3f} kWh")
    
    # Thực hiện reset
    print(f"\n🔄 Đang reset...")
    success = reset_pzem_energy_specific(port, address)
    
    if success:
        print(f"✅ Reset thành công cho {port}")
    else:
        print(f"❌ Reset thất bại cho {port}")
    
    return success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Test một thiết bị cụ thể
        port = sys.argv[1]
        test_single_device_reset(port)
    else:
        # Test tất cả thiết bị
        test_multi_device_reset() 