# Reading multiple PZEM-004t sensors (v3.0) concurrently using Modbus-RTU
# The script automatically detects PL2303 USB-to-Serial adapters and reads from them every second.

import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial.tools.list_ports
import threading
import time
from tabulate import tabulate
import os
import pandas as pd
from datetime import datetime
import csv

def find_pzem_ports():
    """
    Scans for and returns a list of serial ports that appear to be connected to
    PZEM-004t sensors via a USB-to-Serial adapter (like PL2303, CH340, etc.).
    """
    pzem_ports = []
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Make the check case-insensitive and more general.
        desc_lower = port.description.lower() if port.description else ""
        device_lower = port.device.lower()
        hwid_lower = port.hwid.lower() if port.hwid else ""

        # Add more keywords if your adapter has a different description
        keywords = ["pl2303", "usb-serial", "usb serial", "ch340"]
        
        if any(keyword in desc_lower for keyword in keywords) or \
           any(keyword in device_lower for keyword in keywords) or \
           "vid:067b" in hwid_lower:  # Check for Prolific Vendor ID
            pzem_ports.append(port.device)
            
    return pzem_ports

def get_csv_filename(port):
    """
    Generate CSV filename based on port name
    """
    # Remove special characters from port name for filename
    port_clean = port.replace('/', '_').replace('\\', '_').replace(':', '_')
    return f"data/csv_logs/pzem_{port_clean}.csv"

def ensure_csv_headers(filename):
    """
    Ensure CSV file exists with proper headers
    """
    headers = [
        'datetime',
        'port',
        'voltage_v',
        'current_a', 
        'power_w',
        'energy_wh',
        'frequency_hz',
        'power_factor',
        'alarm_status'
    ]
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Check if file exists and has headers
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
        print(f"Created new CSV file: {filename}")
    else:
        # Check if file is empty or missing headers
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                first_row = next(reader)
                if first_row != headers:
                    # Backup existing file and recreate with headers
                    backup_name = filename.replace('.csv', '_backup.csv')
                    os.rename(filename, backup_name)
                    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(headers)
                    print(f"Updated CSV headers for: {filename}")
            except StopIteration:
                # File is empty, add headers
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)

def save_to_csv(sensor_data):
    """
    Save sensor data to individual CSV file
    """
    if sensor_data is None:
        return
    
    filename = get_csv_filename(sensor_data['port'])
    ensure_csv_headers(filename)
    
    # Prepare data row
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row = [
        current_time,
        sensor_data['port'],
        f"{sensor_data['voltage']:.1f}",
        f"{sensor_data['current']:.3f}",
        f"{sensor_data['power']:.1f}",
        sensor_data['energy'],
        f"{sensor_data['frequency']:.1f}",
        f"{sensor_data['power_factor']:.2f}",
        "ON" if sensor_data['alarm'] else "OFF"
    ]
    
    # Append to CSV file
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def read_pzem_data(port):
    """
    Connects to a PZEM sensor on a given port, reads its data, and returns it.
    Returns a dictionary with sensor data or None if failed.
    """
    master = None
    sensor = None
    try:
        # Connect to the sensor with improved settings for Raspberry Pi
        sensor = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            xonxoff=0,
            timeout=2.0,  # Increased timeout for Raspberry Pi
            write_timeout=2.0,  # Add write timeout
            inter_byte_timeout=0.1  # Add inter-byte timeout
        )
        
        # Wait a bit for the port to stabilize
        time.sleep(0.1)
        
        # Clear any existing data in buffers
        sensor.reset_input_buffer()
        sensor.reset_output_buffer()

        master = modbus_rtu.RtuMaster(sensor)
        master.set_timeout(3.0)  # Increased timeout
        # master.set_interframe_delay(0.01)  # Not available in this version
        # master.set_verbose(True) # Uncomment for detailed Modbus communication logging

        # Wait a bit more before reading
        time.sleep(0.05)
        
        # Try reading with retry mechanism
        max_retries = 3
        data = None
        
        for attempt in range(max_retries):
            try:
                # Read 10 registers starting from address 0
                data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
                break  # Success, exit retry loop
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed for {port}: {e}. Retrying...")
                    time.sleep(0.1)
                    # Clear buffers before retry
                    sensor.reset_input_buffer()
                    sensor.reset_output_buffer()
                else:
                    raise e  # Last attempt failed, re-raise the exception
        
        if data is None:
            raise Exception("Failed to read data after retries")

        # Unpack data according to the PZEM-004t v3.0 documentation
        voltage = data[0] / 10.0  # [V]
        current = (data[1] + (data[2] << 16)) / 1000.0  # [A]
        power = (data[3] + (data[4] << 16)) / 10.0  # [W]
        energy = data[5] + (data[6] << 16)  # [Wh]
        frequency = data[7] / 10.0  # [Hz]
        powerFactor = data[8] / 100.0
        alarm = data[9]  # 0 = no alarm, 1 = alarm

        # Return the collected data as a dictionary
        sensor_data = {
            'port': port,
            'voltage': voltage,
            'current': current,
            'power': power,
            'energy': energy,
            'frequency': frequency,
            'power_factor': powerFactor,
            'alarm': alarm,
            'timestamp': datetime.now()
        }
        
        return sensor_data

    except Exception as e:
        print(f"Could not read from {port}: {e}")
        return None

    finally:
        # Ensure the connection is always closed
        try:
            if master:
                master.close()
            if sensor and sensor.is_open:
                sensor.close()
        except Exception as e:
            # This can happen if the port was never opened, which is fine.
            pass

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
                f"{data['energy']}",
                f"{data['frequency']:.1f}",
                f"{data['power_factor']:.2f}",
                alarm_status
            ]
            table_data.append(row)
            total_power += data['power']
            total_energy += data['energy']
    
    # Display current timestamp
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=== PZEM Sensors Data - {current_time} ===")
    print(f"Found {len(table_data)} active sensor(s)")
    
    # Display the table
    print(tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".2f"))
    
    # Display summary
    if table_data:
        print(f"\n=== Summary ===")
        print(f"Total Power: {total_power:.1f} W")
        print(f"Total Energy: {total_energy} Wh")
        
        # Display CSV file information
        print(f"\n=== CSV Logging ===")
        for data in sensor_data_list:
            if data is not None:
                csv_file = get_csv_filename(data['port'])
                if os.path.exists(csv_file):
                    # Count lines in CSV (excluding header)
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for line in f) - 1  # Subtract header
                    file_size = os.path.getsize(csv_file)
                    print(f"  {data['port']}: {line_count} records, {file_size} bytes")
        
        print("=" * 50)

if __name__ == "__main__":
    try:
        while True:
            # Find all connected PZEM devices
            detected_ports = find_pzem_ports()
            
            if not detected_ports:
                print("No PZEM devices detected. Waiting...")
                time.sleep(2) # Wait before scanning again if no devices found
                continue
            
            print(f"Scanning {len(detected_ports)} PZEM device(s): {detected_ports}")
            
            # Collect data from all sensors
            sensor_data_list = []
            for port in detected_ports:
                data = read_pzem_data(port)
                if data is not None:
                    sensor_data_list.append(data)
                    # Save data to individual CSV file
                    save_to_csv(data)
                    print(f"Data saved to CSV for port: {port}")
                time.sleep(0.1)  # Small delay between readings
            
            # Display all sensor data in a table format
            display_sensors_table(sensor_data_list)

            # Wait for 5 seconds before the next reading cycle (increased for better readability)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(1)  # Wait before continuing