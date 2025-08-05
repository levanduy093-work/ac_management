# Reading multiple PZEM-004T sensors concurrently using the new PZEM-004T library.
# The script automatically detects PL2303 USB-to-Serial adapters and reads from them.

import serial
import serial.tools.list_ports
import threading
import time
from tabulate import tabulate
import os
import pandas as pd
from datetime import datetime
import csv

# Import the new PZEM-004T library
from pzem import PZEM004T

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
    Connects to a PZEM sensor on a given port using the new PZEM004T library,
    reads its data, and returns it as a dictionary.
    Returns None if failed.
    """
    pzem = None
    try:
        # Instantiate the PZEM sensor from our new library
        pzem = PZEM004T(port=port, timeout=2.0)

        # Read all measurements from the sensor at once using the new API
        measurements = pzem.get_all_measurements()
        
        if measurements:
            # Convert energy from kWh to Wh for consistency with existing logic
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
            return sensor_data
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

def manage_log_size(log_dir="data/csv_logs", max_size_gb=5):
    """
    Manages the total size of the log directory. If the size exceeds the limit,
    it removes the oldest day's data from all CSV files until the size is
    below the limit.
    """
    max_size_bytes = max_size_gb * 1024 * 1024 * 1024
    
    # Calculate current directory size
    current_size = sum(
        os.path.getsize(os.path.join(log_dir, f))
        for f in os.listdir(log_dir)
        if os.path.isfile(os.path.join(log_dir, f)) and f.endswith('.csv')
    )

    # Loop until the size is under the limit
    while current_size > max_size_bytes:
        print(f"\nLog directory size ({current_size / (1024**3):.2f} GB) exceeds limit of {max_size_gb} GB. Pruning oldest data...")

        all_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.csv')]
        if not all_files:
            print("No CSV files found to prune.")
            return

        # Use pandas to find the oldest date across all files
        oldest_date = None
        all_dfs = {}

        for f in all_files:
            try:
                df = pd.read_csv(f)
                if not df.empty:
                    # Convert 'datetime' to datetime objects for comparison
                    df['datetime_obj'] = pd.to_datetime(df['datetime'])
                    all_dfs[f] = df
                    
                    min_date_in_file = df['datetime_obj'].min()
                    if oldest_date is None or min_date_in_file < oldest_date:
                        oldest_date = min_date_in_file
                else:
                    all_dfs[f] = None # Placeholder for empty files
            except (pd.errors.EmptyDataError, FileNotFoundError, KeyError):
                # Ignore empty files, non-existent files, or files without 'datetime'
                all_dfs[f] = None
                continue
        
        if oldest_date is None:
            print("Could not determine the oldest date. No data to prune.")
            return

        oldest_date_str = oldest_date.strftime('%Y-%m-%d')
        print(f"Found oldest date: {oldest_date_str}. Removing all entries for this date.")

        # Remove the oldest day from each dataframe and rewrite the CSV
        new_total_size = 0
        for f, df in all_dfs.items():
            if df is not None and not df.empty:
                # Keep rows that are NOT from the oldest date
                rows_before = len(df)
                df_pruned = df[df['datetime_obj'].dt.date > oldest_date.date()]
                rows_after = len(df_pruned)
                
                # Drop the temporary datetime object column before saving
                df_pruned = df_pruned.drop(columns=['datetime_obj'])
                
                # Overwrite the original file
                df_pruned.to_csv(f, index=False)
                
                if rows_before > rows_after:
                    print(f"  - Pruned {rows_before - rows_after} rows from {os.path.basename(f)}")

                new_total_size += os.path.getsize(f)
            elif os.path.exists(f):
                 new_total_size += os.path.getsize(f)

        current_size = new_total_size
        print(f"New log directory size: {current_size / (1024**3):.2f} GB")

def main():
    """
    Main function to run the PZEM sensor monitoring
    """
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

            # Manage log size after displaying data
            manage_log_size(log_dir="data/csv_logs", max_size_gb=5)

            # Wait for 5 seconds before the next reading cycle (increased for better readability)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(1)  # Wait before continuing

if __name__ == "__main__":
    main()