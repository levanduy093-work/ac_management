import serial
import time
import struct
import logging

# Configure logging to show only errors
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants from the C++ library
_PZEM_DEFAULT_ADDR = 0xF8
_PZEM_BAUD_RATE = 9600

# Register and command definitions
_REG_VOLTAGE = 0x0000
_REG_CURRENT_L = 0x0001
_REG_POWER_L = 0x0003
_REG_ENERGY_L = 0x0005
_REG_FREQUENCY = 0x0007
_REG_PF = 0x0008
_REG_ALARM = 0x0009

_CMD_RIR = 0x04  # Read Input Registers
_CMD_WSR = 0x06  # Write Single Register
_CMD_REST = 0x42 # Reset Energy

_WREG_ALARM_THR = 0x0001
_WREG_ADDR = 0x0002

_READ_TIMEOUT = 100  # ms

class PZEM004Tv30:
    """
    Python library for the PZEM-004T v3.0 Power and Energy meter.
    Communicates using Modbus RTU protocol over a serial connection.
    """

    def __init__(self, port, address=_PZEM_DEFAULT_ADDR, timeout=1.0):
        """
        Initializes the PZEM-004T v3.0 sensor.
        Args:
            port (str): The serial port (e.g., '/dev/ttyUSB0' or 'COM3').
            address (int): The slave address of the device (default is 0xF8).
            timeout (float): The serial communication timeout in seconds.
        """
        self.address = address
        try:
            self.serial = serial.Serial(
                port=port,
                baudrate=_PZEM_BAUD_RATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=timeout
            )
            logging.info(f"Successfully connected to port {port}")
        except serial.SerialException as e:
            logging.error(f"Failed to open serial port {port}: {e}")
            raise

        self.last_read_time = 0
        self.values = {
            'voltage': 0.0,
            'current': 0.0,
            'power': 0.0,
            'energy': 0.0,
            'frequency': 0.0,
            'pf': 0.0,
            'alarms': 0
        }

    def _crc16(self, data: bytes) -> bytes:
        """
        Calculates the CRC16 checksum for the given data.
        Args:
            data (bytes): The data to calculate the checksum for.
        Returns:
            bytes: The CRC16 checksum as a 2-byte little-endian value.
        """
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return struct.pack('<H', crc)

    def _send_command(self, command, register, value):
        """
        Sends a command to the PZEM module.
        Args:
            command (int): The command code (e.g., _CMD_WSR).
            register (int): The register address.
            value (int): The value to write.
        Returns:
            bytes or None: The response from the device, or None on failure.
        """
        packet = struct.pack('>BBHH', self.address, command, register, value)
        packet += self._crc16(packet)

        self.serial.flushInput()
        self.serial.write(packet)
        
        response = self.serial.read(len(packet))
        if len(response) != len(packet):
            logging.warning("Received response with incorrect length.")
            return None
        
        if not self._validate_response(response):
            logging.warning("Invalid response received.")
            return None
            
        return response

    def _validate_response(self, response: bytes) -> bool:
        """
        Validates the CRC of a response packet.
        Args:
            response (bytes): The full response packet from the device.
        Returns:
            bool: True if the CRC is valid, False otherwise.
        """
        if len(response) < 2:
            return False
        
        data_part = response[:-2]
        received_crc = response[-2:]
        calculated_crc = self._crc16(data_part)
        
        return received_crc == calculated_crc

    def update_values(self) -> bool:
        """
        Reads all measurement registers from the device and updates internal values.
        This is the primary method to get data from the sensor.
        Returns:
            bool: True on success, False on failure.
        """
        packet = struct.pack('>BBHH', self.address, _CMD_RIR, 0x0000, 0x000A)
        packet += self._crc16(packet)

        self.serial.flushInput()
        self.serial.write(packet)

        # Expected response: addr(1) + cmd(1) + byte_count(1) + data(20) + crc(2) = 25 bytes
        response = self.serial.read(25)

        if len(response) != 25 or not self._validate_response(response):
            logging.error("Failed to read values or invalid response.")
            return False

        # Unpack the 20 bytes of data
        raw_values = struct.unpack('>HHHHHHHHHH', response[3:23])

        self.values['voltage'] = raw_values[0] / 10.0
        self.values['current'] = (raw_values[1] + (raw_values[2] << 16)) / 1000.0
        self.values['power'] = (raw_values[3] + (raw_values[4] << 16)) / 10.0
        self.values['energy'] = (raw_values[5] + (raw_values[6] << 16)) / 1000.0
        self.values['frequency'] = raw_values[7] / 10.0
        self.values['pf'] = raw_values[8] / 100.0
        self.values['alarms'] = raw_values[9]
        
        self.last_read_time = time.time()
        logging.info(f"Updated values: {self.values}")
        return True

    def voltage(self) -> float:
        """Returns the voltage in Volts."""
        if not self.update_values():
            return float('nan')
        return self.values['voltage']

    def current(self) -> float:
        """Returns the current in Amperes."""
        if not self.update_values():
            return float('nan')
        return self.values['current']

    def power(self) -> float:
        """Returns the active power in Watts."""
        if not self.update_values():
            return float('nan')
        return self.values['power']

    def energy(self) -> float:
        """Returns the total energy in kWh."""
        if not self.update_values():
            return float('nan')
        return self.values['energy']

    def frequency(self) -> float:
        """Returns the frequency in Hertz."""
        if not self.update_values():
            return float('nan')
        return self.values['frequency']

    def power_factor(self) -> float:
        """Returns the power factor."""
        if not self.update_values():
            return float('nan')
        return self.values['pf']

    def get_power_alarm(self) -> bool:
        """Checks if the power alarm is triggered."""
        if not self.update_values():
            return False
        return self.values['alarms'] != 0x0000

    def set_power_alarm(self, watts: int) -> bool:
        """
        Sets the power alarm threshold.
        Args:
            watts (int): The alarm threshold in Watts (1 to 25000).
        Returns:
            bool: True on success, False on failure.
        """
        if not 1 <= watts <= 25000:
            raise ValueError("Watts must be between 1 and 25000.")
        
        response = self._send_command(_CMD_WSR, _WREG_ALARM_THR, watts)
        return response is not None

    def reset_energy(self) -> bool:
        """
        Resets the energy counter on the device.
        Returns:
            bool: True on success, False on failure.
        """
        packet = struct.pack('>BB', self.address, _CMD_REST)
        packet += self._crc16(packet)
        
        self.serial.flushInput()
        self.serial.write(packet)
        
        # The device may not send a response to the reset command.
        # A small delay to allow the command to be processed.
        time.sleep(0.1)
        return True # Assuming success as there's no direct confirmation

    def set_address(self, new_address: int) -> bool:
        """
        Sets a new slave address for the device.
        Warning: This is permanent. The device will only respond to the new address.
        Args:
            new_address (int): The new address (1 to 247).
        Returns:
            bool: True on success, False on failure.
        """
        if not 1 <= new_address <= 247:
            raise ValueError("Address must be between 1 and 247.")
            
        response = self._send_command(_CMD_WSR, _WREG_ADDR, new_address)
        if response:
            self.address = new_address
            return True
        return False

    def close(self):
        """Closes the serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            logging.info("Serial port closed.")

if __name__ == '__main__':
    # This is an example of how to use the library.
    # You need to change '/dev/ttyUSB0' to your actual serial port.
    try:
        # For Linux: '/dev/ttyUSB0', '/dev/ttyS0', etc.
        # For Windows: 'COM3', 'COM4', etc.
        pzem = PZEM004Tv30(port='/dev/ttyUSB0')

        print("--- Reading PZEM-004T v3.0 Values ---")
        
        voltage = pzem.voltage()
        if not voltage == float('nan'):
            print(f"Voltage: {voltage:.1f}V")
            
            current = pzem.current()
            print(f"Current: {current:.3f}A")
            
            power = pzem.power()
            print(f"Power: {power:.1f}W")
            
            energy = pzem.energy()
            print(f"Energy: {energy:.3f}kWh")
            
            frequency = pzem.frequency()
            print(f"Frequency: {frequency:.1f}Hz")
            
            pf = pzem.power_factor()
            print(f"Power Factor: {pf}")

            alarm = pzem.get_power_alarm()
            print(f"Power Alarm: {'ON' if alarm else 'OFF'}")
        else:
            print("Could not read values from the sensor.")

        # Example of setting the power alarm to 100W
        # print("\nSetting power alarm to 100W...")
        # if pzem.set_power_alarm(100):
        #     print("Power alarm set successfully.")
        # else:
        #     print("Failed to set power alarm.")

        # Example of resetting energy
        # print("\nResetting energy counter...")
        # if pzem.reset_energy():
        #     print("Energy counter reset.")
        #     time.sleep(1)
        #     print(f"New Energy: {pzem.energy():.3f}kWh")
        # else:
        #     print("Failed to reset energy.")

        pzem.close()

    except Exception as e:
        print(f"An error occurred: {e}")
