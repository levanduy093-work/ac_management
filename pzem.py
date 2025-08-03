# Reading multiple PZEM-004t sensors (v3.0) concurrently using Modbus-RTU
# The script automatically detects PL2303 USB-to-Serial adapters and reads from them every second.

import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial.tools.list_ports
import threading
import time

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

def read_pzem_data(port):
    """
    Connects to a PZEM sensor on a given port, reads its data, and prints it.
    This function is designed to be run in a separate thread for each sensor.
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

        # Print the collected data in a structured format
        print(f"--- Data from {port} ---")
        print(f"  Voltage: {voltage:.1f} V")
        print(f"  Current: {current:.3f} A")
        print(f"  Power: {power:.1f} W")
        print(f"  Energy: {energy} Wh")
        print(f"  Frequency: {frequency:.1f} Hz")
        print(f"  Power Factor: {powerFactor:.2f}")
        print(f"  Alarm: {'ON' if alarm else 'OFF'}")
        print("-" * (20 + len(port)))

    except Exception as e:
        print(f"Could not read from {port}: {e}")

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

if __name__ == "__main__":
    try:
        while True:
            # Find all connected PZEM devices
            detected_ports = find_pzem_ports()
            
            if not detected_ports:
                print("No PZEM devices detected. Waiting...")
                time.sleep(2) # Wait before scanning again if no devices found
                continue
            
            print(f"Found {len(detected_ports)} PZEM device(s): {detected_ports}")
            
            # Read from ports sequentially instead of concurrently to avoid conflicts on Raspberry Pi
            # This is more reliable for resource-constrained systems
            for port in detected_ports:
                read_pzem_data(port)
                time.sleep(0.1)  # Small delay between readings

            # Wait for 1 second before the next reading cycle
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(1)  # Wait before continuing