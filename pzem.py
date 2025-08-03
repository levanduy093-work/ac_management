# Reading PZEM-004t power sensor (new version v3.0) through Modbus-RTU protocol over TTL UART
# Run as:
# python pzem.py

# To install dependencies in your conda environment: 
# conda install pyserial
# pip install modbus-tk

import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# --- CONFIGURATION ---
# NOTE: You might need to change the port to the correct one for your device.
# On your system, it could be '/dev/cu.PL2303-USBtoUART110' or '/dev/cu.usbserial-110'
# Use the command `python -m serial.tools.list_ports` to find the correct port.
PORT = '/dev/cu.PL2303-USBtoUART110' 

master = None
sensor = None

try:
    # Connect to the sensor
    sensor = serial.Serial(
        port=PORT,
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=0
    )

    master = modbus_rtu.RtuMaster(sensor)
    master.set_timeout(2.0)
    master.set_verbose(True)

    print("Reading data from sensor...")
    # Read 10 registers starting from 0
    data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)

    voltage = data[0] / 10.0 # [V]
    current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
    power = (data[3] + (data[4] << 16)) / 10.0 # [W]
    energy = data[5] + (data[6] << 16) # [Wh]
    frequency = data[7] / 10.0 # [Hz]
    powerFactor = data[8] / 100.0
    alarm = data[9] # 0 = no alarm

    print('Voltage [V]: ', voltage)
    print('Current [A]: ', current)
    print('Power [W]: ', power) # active power (V * I * power factor)
    print('Energy [Wh]: ', energy)
    print('Frequency [Hz]: ', frequency)
    print('Power factor []: ', powerFactor)
    print('Alarm : ', alarm)

    # Changing power alarm value to 100 W
    # print("Setting alarm threshold to 100W")
    # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    try:
        if master:
            master.close()
        if sensor and sensor.is_open:
            sensor.close()
            print("Sensor connection closed.")
    except Exception as e:
        print(f"Error while closing connection: {e}")