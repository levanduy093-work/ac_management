#!/usr/bin/env python3
"""
Quick Start Script for PZEM-004T Power Monitoring

This script demonstrates the basic functionality of the PZEM-004T library.
"""

import sys
import os
import time
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from pzem import PZEM004T
except ImportError:
    print("❌ Error: Could not import PZEM004T library")
    print("Make sure you have installed the library: pip install -e .")
    sys.exit(1)

def find_pzem_ports():
    """Find available PZEM ports"""
    import serial.tools.list_ports
    
    pzem_ports = []
    for port in serial.tools.list_ports.comports():
        if any(keyword in port.description.lower() for keyword in 
               ['pzem', 'pl2303', 'ch340', 'cp210', 'ftdi', 'usb serial']):
            pzem_ports.append(port.device)
    
    return pzem_ports

def demo_basic_reading():
    """Demonstrate basic reading functionality"""
    print("🔍 Looking for PZEM devices...")
    ports = find_pzem_ports()
    
    if not ports:
        print("❌ No PZEM devices found!")
        print("Please connect a PZEM-004T device and try again.")
        return False
    
    print(f"✅ Found {len(ports)} device(s): {ports}")
    
    # Try to read from the first device
    port = ports[0]
    print(f"\n📊 Reading from {port}...")
    
    try:
        pzem = PZEM004T(port=port, timeout=2.0)
        
        # Read all measurements
        measurements = pzem.get_all_measurements()
        
        if measurements:
            print("✅ Successfully read measurements:")
            print(f"   Voltage: {measurements['voltage']:.1f} V")
            print(f"   Current: {measurements['current']:.3f} A")
            print(f"   Power: {measurements['power']:.1f} W")
            print(f"   Energy: {measurements['energy']:.3f} kWh")
            print(f"   Frequency: {measurements['frequency']:.1f} Hz")
            print(f"   Power Factor: {measurements['power_factor']:.2f}")
            print(f"   Alarm Status: {'ON' if measurements['alarm_status'] else 'OFF'}")
            
            pzem.close()
            return True
        else:
            print("❌ Failed to read measurements")
            pzem.close()
            return False
            
    except Exception as e:
        print(f"❌ Error reading from {port}: {e}")
        return False

def demo_continuous_monitoring():
    """Demonstrate continuous monitoring"""
    print("\n🔄 Starting continuous monitoring (5 seconds)...")
    
    ports = find_pzem_ports()
    if not ports:
        print("❌ No devices found for monitoring")
        return False
    
    try:
        pzem = PZEM004T(port=ports[0], timeout=2.0)
        
        start_time = time.time()
        while time.time() - start_time < 5:
            measurements = pzem.get_all_measurements()
            if measurements:
                print(f"\r⏱️  {datetime.now().strftime('%H:%M:%S')} - "
                      f"V: {measurements['voltage']:.1f}V, "
                      f"I: {measurements['current']:.3f}A, "
                      f"P: {measurements['power']:.1f}W, "
                      f"E: {measurements['energy']:.3f}kWh", end='', flush=True)
            time.sleep(1)
        
        print("\n✅ Continuous monitoring completed")
        pzem.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error during monitoring: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 PZEM-004T Power Monitoring - Quick Start Demo")
    print("=" * 50)
    
    # Demo 1: Basic reading
    print("\n1️⃣  Basic Reading Demo")
    print("-" * 20)
    if not demo_basic_reading():
        print("❌ Basic reading demo failed")
        return
    
    # Demo 2: Continuous monitoring
    print("\n2️⃣  Continuous Monitoring Demo")
    print("-" * 20)
    demo_continuous_monitoring()
    
    print("\n🎉 Demo completed successfully!")
    print("\n📚 Next steps:")
    print("   - Run 'python examples/example_usage.py' for more examples")
    print("   - Run 'python tools/read_ac_sensor.py' for multi-sensor monitoring")
    print("   - Run 'python tools/reset_energy.py' to reset energy counters")
    print("   - Check 'docs/PZEM004T.md' for detailed documentation")

if __name__ == "__main__":
    main() 