# Reading multiple PZEM-004T sensors concurrently using database storage
# This script uses SQLite database instead of CSV files for better data management

import serial
import serial.tools.list_ports
import threading
import time
from tabulate import tabulate
import os
from datetime import datetime
import sys

# Import the PZEM-004T library and database module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from pzem import PZEM004T
from database import PZEMDatabase

def find_pzem_ports():
    """
    Scans for and returns a list of serial ports that appear to be connected to
    PZEM-004T sensors via a USB-to-Serial adapter (like PL2303, CH340, etc.).
    """
    pzem_ports = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Make the check case-insensitive and more general.
        desc_lower = port.description.lower() if port.description else ""
        device_lower = port.device.lower()
        hwid_lower = port.hwid.lower() if port.hwid else ""

        # Add more keywords if your adapter has a different description
        keywords = ["pl2303", "usb-serial", "usb serial", "ch340", "cp210", "ftdi"]
        
        if any(keyword in desc_lower for keyword in keywords) or \
           any(keyword in device_lower for keyword in keywords) or \
           "vid:067b" in hwid_lower:  # Check for Prolific Vendor ID
            pzem_ports.append(port.device)
            
    return pzem_ports

def read_pzem_data(port, db):
    """
    Connects to a PZEM sensor on a given port using the PZEM004T library,
    reads its data, saves to database, and returns it as a dictionary.
    Returns None if failed.
    """
    pzem = None
    try:
        # Instantiate the PZEM sensor from our library
        pzem = PZEM004T(port=port, timeout=2.0)

        # Read all measurements from the sensor at once using the API
        measurements = pzem.get_all_measurements()
        
        if measurements:
            # Convert energy from kWh to Wh for consistency
            energy_wh = measurements['energy'] * 1000

            sensor_data = {
                'port': port,
                'voltage': measurements['voltage'],
                'current': measurements['current'],
                'power': measurements['power'],
                'energy': energy_wh,
                'frequency': measurements['frequency'],
                'power_factor': measurements['power_factor'],
                'alarm': measurements['alarm_status'],
                'timestamp': datetime.now()
            }
            
            # Save to database
            if db.save_measurement(sensor_data):
                return sensor_data
            else:
                print(f"Failed to save data to database for {port}")
                return None
        else:
            print(f"Could not read from {port}: Failed to get measurements.")
            return None

    except Exception as e:
        print(f"Could not read from {port}: {e}")
        return None

    finally:
        # Ensure the connection is always closed
        if pzem:
            pzem.close()

def display_sensors_table(sensor_data_list):
    """
    Display sensor data in a formatted table
    """
    if not sensor_data_list:
        print("No sensor data available.")
        return
    
    # Clear screen for better visibility
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Prepare table headers
    headers = [
        "Port", 
        "Voltage (V)", 
        "Current (A)", 
        "Power (W)", 
        "Energy (Wh)", 
        "Frequency (Hz)", 
        "Power Factor", 
        "Alarm"
    ]
    
    # Prepare table data
    table_data = []
    total_power = 0
    total_energy = 0
    
    for data in sensor_data_list:
        if data is not None:
            alarm_status = "ON" if data['alarm'] else "OFF"
            row = [
                data['port'],
                f"{data['voltage']:.1f}",
                f"{data['current']:.3f}",
                f"{data['power']:.1f}",
                f"{data['energy']:.0f}",
                f"{data['frequency']:.1f}",
                f"{data['power_factor']:.2f}",
                alarm_status
            ]
            table_data.append(row)
            total_power += data['power']
            total_energy += data['energy']
    
    # Display the table
    print("\n" + "="*100)
    print(f"🔌 PZEM-004T Power Monitoring - Database Storage")
    print(f"📊 Total Sensors: {len(table_data)} | Total Power: {total_power:.1f}W | Total Energy: {total_energy:.0f}Wh")
    print(f"🕐 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100)
    
    if table_data:
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\n📈 Summary: Total Power: {total_power:.1f}W | Total Energy: {total_energy:.0f}Wh")
    else:
        print("❌ No sensor data available")
    
    print("\n💾 Data is being saved to SQLite database: data/pzem_data.db")
    print("🔄 Press Ctrl+C to stop monitoring")

def display_database_stats(db):
    """
    Display database statistics
    """
    try:
        stats = db.get_database_stats()
        print(f"\n📊 Database Statistics:")
        print(f"   📁 Database Size: {stats['database_size_mb']} MB")
        print(f"   📊 Total Measurements: {stats['total_measurements']:,}")
        print(f"   🔌 Total Sensors: {stats['total_sensors']}")
        if stats['oldest_measurement'] and stats['newest_measurement']:
            print(f"   📅 Data Range: {stats['oldest_measurement']} to {stats['newest_measurement']}")
    except Exception as e:
        print(f"Error getting database stats: {e}")

def cleanup_old_data(db, days_to_keep=30):
    """
    Clean up old data to manage database size
    """
    try:
        deleted_count = db.cleanup_old_data(days_to_keep)
        if deleted_count > 0:
            print(f"🗑️  Cleaned up {deleted_count} old measurements (older than {days_to_keep} days)")
    except Exception as e:
        print(f"Error cleaning up old data: {e}")

def main():
    """
    Main function to run the PZEM monitoring with database storage
    """
    print("🔌 PZEM-004T Power Monitoring with Database Storage")
    print("="*60)
    
    # Initialize database
    db = PZEMDatabase()
    print(f"💾 Database initialized: {db.db_path}")
    
    # Find PZEM ports
    pzem_ports = find_pzem_ports()
    
    if not pzem_ports:
        print("❌ No PZEM devices detected!")
        print("\nTroubleshooting:")
        print("1. Check USB connections")
        print("2. Ensure drivers are installed (PL2303, CH340, CP210, FTDI)")
        print("3. Check device permissions")
        print("4. Try: lsusb and ls -la /dev/ttyUSB*")
        return
    
    print(f"✅ Found {len(pzem_ports)} PZEM device(s): {', '.join(pzem_ports)}")
    
    # Display initial database stats
    display_database_stats(db)
    
    # Clean up old data (keep last 30 days)
    cleanup_old_data(db, days_to_keep=30)
    
    print(f"\n🚀 Starting monitoring... Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        while True:
            # Read data from all sensors concurrently
            sensor_data_list = []
            threads = []
            
            # Create threads for each sensor
            for port in pzem_ports:
                thread = threading.Thread(
                    target=lambda p=port: sensor_data_list.append(read_pzem_data(p, db))
                )
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Display results
            display_sensors_table(sensor_data_list)
            
            # Wait before next reading
            time.sleep(5)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Monitoring stopped by user")
        print(f"💾 Final database statistics:")
        display_database_stats(db)
        print(f"\n📁 Database file: {db.db_path}")
        print(f"📊 You can query the database using SQLite tools or the provided API")

if __name__ == "__main__":
    main() 