import serial
import time
import struct
import logging
from typing import Optional, Dict, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PZEM004T:
    """
    Python library for the PZEM-004T AC Power and Energy meter.
    
    This library implements the complete Modbus-RTU protocol for the PZEM-004T module,
    supporting all documented functions including measurement reading, parameter
    configuration, energy reset, and calibration.
    
    Features:
    - Read voltage, current, power, energy, frequency, power factor
    - Set power alarm threshold
    - Change device address
    - Reset energy counter
    - Calibration (factory use)
    - Comprehensive error handling
    - CRC validation
    
    Supported models:
    - PZEM-004T-10A: 0-10A range (built-in shunt)
    - PZEM-004T-100A: 0-100A range (external CT)
    """
    
    # Communication constants
    DEFAULT_ADDRESS = 0xF8
    BROADCAST_ADDRESS = 0x00
    CALIBRATION_ADDRESS = 0xF8
    BAUD_RATE = 9600
    DATA_BITS = 8
    STOP_BITS = 1
    PARITY = 'N'
    
    # Function codes
    READ_HOLDING_REGISTERS = 0x03
    READ_INPUT_REGISTERS = 0x04
    WRITE_SINGLE_REGISTER = 0x06
    CALIBRATION = 0x41
    RESET_ENERGY = 0x42
    
    # Register addresses for measurements
    REG_VOLTAGE = 0x0000
    REG_CURRENT_L = 0x0001
    REG_CURRENT_H = 0x0002
    REG_POWER_L = 0x0003
    REG_POWER_H = 0x0004
    REG_ENERGY_L = 0x0005
    REG_ENERGY_H = 0x0006
    REG_FREQUENCY = 0x0007
    REG_POWER_FACTOR = 0x0008
    REG_ALARM_STATUS = 0x0009
    
    # Register addresses for parameters
    REG_ALARM_THRESHOLD = 0x0001
    REG_DEVICE_ADDRESS = 0x0002
    
    # Calibration password
    CALIBRATION_PASSWORD = 0x3721
    
    # Error codes
    ERROR_ILLEGAL_FUNCTION = 0x01
    ERROR_ILLEGAL_ADDRESS = 0x02
    ERROR_ILLEGAL_DATA = 0x03
    ERROR_SLAVE_ERROR = 0x04
    
    # Resolution factors
    VOLTAGE_RESOLUTION = 0.1      # 1 LSB = 0.1V
    CURRENT_RESOLUTION = 0.001    # 1 LSB = 0.001A
    POWER_RESOLUTION = 0.1        # 1 LSB = 0.1W
    ENERGY_RESOLUTION = 1.0       # 1 LSB = 1Wh
    FREQUENCY_RESOLUTION = 0.1    # 1 LSB = 0.1Hz
    PF_RESOLUTION = 0.01          # 1 LSB = 0.01
    
    def __init__(self, port: str, address: int = DEFAULT_ADDRESS, timeout: float = 1.0):
        """
        Initialize PZEM-004T connection.
        
        Args:
            port (str): Serial port (e.g., '/dev/ttyUSB0', 'COM3')
            address (int): Device address (1-247, default 0xF8 for single device)
            timeout (float): Serial timeout in seconds
        """
        self.address = address
        self.port = port
        self.timeout = timeout
        self.serial = None
        self._connect()
        
        # Measurement data cache
        self._measurements = {
            'voltage': 0.0,
            'current': 0.0,
            'power': 0.0,
            'energy': 0.0,
            'frequency': 0.0,
            'power_factor': 0.0,
            'alarm_status': False
        }
        self._last_update = 0
        self._update_interval = 0.1  # Minimum time between updates
        
    def _connect(self):
        """Establish serial connection."""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.BAUD_RATE,
                bytesize=self.DATA_BITS,
                parity=self.PARITY,
                stopbits=self.STOP_BITS,
                timeout=self.timeout
            )
            logging.info(f"Connected to PZEM-004T on {self.port}")
        except serial.SerialException as e:
            logging.error(f"Failed to connect to {self.port}: {e}")
            raise
    
    def _crc16(self, data: bytes) -> bytes:
        """
        Calculate Modbus-RTU CRC16 checksum.
        
        Args:
            data (bytes): Data to calculate CRC for
            
        Returns:
            bytes: 2-byte CRC (little-endian)
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
    
    def _validate_crc(self, data: bytes) -> bool:
        """
        Validate CRC of received data.
        
        Args:
            data (bytes): Complete packet including CRC
            
        Returns:
            bool: True if CRC is valid
        """
        if len(data) < 2:
            return False
        
        packet_data = data[:-2]
        received_crc = data[-2:]
        calculated_crc = self._crc16(packet_data)
        
        return received_crc == calculated_crc
    
    def _send_command(self, function_code: int, register: int = 0, 
                     value: int = 0, register_count: int = 0) -> Optional[bytes]:
        """
        Send command to PZEM device.
        
        Args:
            function_code (int): Modbus function code
            register (int): Register address
            value (int): Value to write (for write commands)
            register_count (int): Number of registers to read
            
        Returns:
            bytes or None: Response data or None on error
        """
        if not self.serial or not self.serial.is_open:
            logging.error("Serial connection not available")
            return None
        
        # Build command packet
        if function_code in [self.READ_HOLDING_REGISTERS, self.READ_INPUT_REGISTERS]:
            # Read command: addr + func + reg_high + reg_low + count_high + count_low + crc
            packet = struct.pack('>BBHH', self.address, function_code, register, register_count)
        elif function_code == self.WRITE_SINGLE_REGISTER:
            # Write command: addr + func + reg_high + reg_low + val_high + val_low + crc
            packet = struct.pack('>BBHH', self.address, function_code, register, value)
        elif function_code == self.RESET_ENERGY:
            # Reset command: addr + func + crc
            packet = struct.pack('>BB', self.address, function_code)
        elif function_code == self.CALIBRATION:
            # Calibration command: addr + func + password_high + password_low + crc
            packet = struct.pack('>BBHH', self.address, function_code, 0x37, 0x21)
        else:
            logging.error(f"Unsupported function code: {function_code}")
            return None
        
        # Add CRC
        packet += self._crc16(packet)
        
        # Clear input buffer and send command
        self.serial.flushInput()
        self.serial.write(packet)
        
        # Read response
        if function_code in [self.READ_HOLDING_REGISTERS, self.READ_INPUT_REGISTERS]:
            # Read response: addr + func + byte_count + data + crc
            response = self.serial.read(3)  # Read header first
            if len(response) < 3:
                return None
            
            byte_count = response[2]
            data = self.serial.read(byte_count + 2)  # data + crc
            response += data
        elif function_code == self.WRITE_SINGLE_REGISTER:
            # Write response: addr + func + reg_high + reg_low + val_high + val_low + crc
            response = self.serial.read(8)
        elif function_code == self.RESET_ENERGY:
            # Reset response: addr + func + crc
            response = self.serial.read(4)
        elif function_code == self.CALIBRATION:
            # Calibration response: addr + func + password_high + password_low + crc
            response = self.serial.read(8)
        else:
            return None
        
        # Validate response
        if not self._validate_crc(response):
            logging.error("Invalid CRC in response")
            return None
        
        # Check for error response
        if len(response) >= 2 and response[1] & 0x80:
            error_code = response[2] if len(response) > 2 else 0
            self._handle_error(error_code)
            return None
        
        return response
    
    def _handle_error(self, error_code: int):
        """Handle Modbus error codes."""
        error_messages = {
            self.ERROR_ILLEGAL_FUNCTION: "Illegal function",
            self.ERROR_ILLEGAL_ADDRESS: "Illegal data address",
            self.ERROR_ILLEGAL_DATA: "Illegal data value",
            self.ERROR_SLAVE_ERROR: "Slave device failure"
        }
        message = error_messages.get(error_code, f"Unknown error {error_code}")
        logging.error(f"Modbus error: {message}")
    
    def read_measurements(self) -> Dict[str, Any]:
        """
        Read all measurement values from the device.
        
        Returns:
            dict: Dictionary containing all measurement values
        """
        # Check if we need to update (avoid too frequent reads)
        current_time = time.time()
        if current_time - self._last_update < self._update_interval:
            return self._measurements.copy()
        
        response = self._send_command(
            self.READ_INPUT_REGISTERS, 
            self.REG_VOLTAGE, 
            register_count=10
        )
        
        if not response or len(response) < 25:
            logging.error("Failed to read measurements")
            return self._measurements.copy()
        
        # Parse response data (20 bytes of measurement data)
        data = response[3:23]
        values = struct.unpack('>HHHHHHHHHH', data)
        
        # Convert raw values to physical units
        self._measurements['voltage'] = values[0] * self.VOLTAGE_RESOLUTION
        self._measurements['current'] = (values[1] + (values[2] << 16)) * self.CURRENT_RESOLUTION
        self._measurements['power'] = (values[3] + (values[4] << 16)) * self.POWER_RESOLUTION
        self._measurements['energy'] = (values[5] + (values[6] << 16)) * self.ENERGY_RESOLUTION
        self._measurements['frequency'] = values[7] * self.FREQUENCY_RESOLUTION
        self._measurements['power_factor'] = values[8] * self.PF_RESOLUTION
        self._measurements['alarm_status'] = values[9] != 0x0000
        
        self._last_update = current_time
        return self._measurements.copy()
    
    def get_voltage(self) -> float:
        """Get voltage in Volts."""
        measurements = self.read_measurements()
        return measurements['voltage']
    
    def get_current(self) -> float:
        """Get current in Amperes."""
        measurements = self.read_measurements()
        return measurements['current']
    
    def get_power(self) -> float:
        """Get active power in Watts."""
        measurements = self.read_measurements()
        return measurements['power']
    
    def get_energy(self) -> float:
        """Get total energy in kWh."""
        measurements = self.read_measurements()
        return measurements['energy']
    
    def get_frequency(self) -> float:
        """Get frequency in Hertz."""
        measurements = self.read_measurements()
        return measurements['frequency']
    
    def get_power_factor(self) -> float:
        """Get power factor."""
        measurements = self.read_measurements()
        return measurements['power_factor']
    
    def get_alarm_status(self) -> bool:
        """Get power alarm status."""
        measurements = self.read_measurements()
        return measurements['alarm_status']
    
    def set_power_alarm_threshold(self, watts: int) -> bool:
        """
        Set power alarm threshold.
        
        Args:
            watts (int): Alarm threshold in Watts (1-25000)
            
        Returns:
            bool: True on success
        """
        if not 1 <= watts <= 25000:
            raise ValueError("Power alarm threshold must be between 1 and 25000 Watts")
        
        response = self._send_command(
            self.WRITE_SINGLE_REGISTER,
            self.REG_ALARM_THRESHOLD,
            watts
        )
        
        return response is not None
    
    def get_power_alarm_threshold(self) -> Optional[int]:
        """
        Get current power alarm threshold.
        
        Returns:
            int or None: Alarm threshold in Watts
        """
        response = self._send_command(
            self.READ_HOLDING_REGISTERS,
            self.REG_ALARM_THRESHOLD,
            register_count=1
        )
        
        if not response or len(response) < 7:
            return None
        
        value = struct.unpack('>H', response[3:5])[0]
        return value
    
    def set_address(self, new_address: int) -> bool:
        """
        Change device address.
        
        Args:
            new_address (int): New address (1-247)
            
        Returns:
            bool: True on success
            
        Warning:
            This change is permanent. The device will only respond to the new address.
        """
        if not 1 <= new_address <= 247:
            raise ValueError("Address must be between 1 and 247")
        
        response = self._send_command(
            self.WRITE_SINGLE_REGISTER,
            self.REG_DEVICE_ADDRESS,
            new_address
        )
        
        if response:
            self.address = new_address
            logging.info(f"Device address changed to {new_address}")
            return True
        
        return False
    
    def get_address(self) -> Optional[int]:
        """
        Get current device address.
        
        Returns:
            int or None: Current device address
        """
        response = self._send_command(
            self.READ_HOLDING_REGISTERS,
            self.REG_DEVICE_ADDRESS,
            register_count=1
        )
        
        if not response or len(response) < 7:
            return None
        
        value = struct.unpack('>H', response[3:5])[0]
        return value
    
    def reset_energy(self) -> bool:
        """
        Reset energy counter to zero.
        
        Returns:
            bool: True on success
        """
        response = self._send_command(self.RESET_ENERGY)
        if response:
            logging.info("Energy counter reset successfully")
            # Clear cached energy value
            self._measurements['energy'] = 0.0
            return True
        
        return False
    
    def calibrate(self) -> bool:
        """
        Perform device calibration (factory use only).
        
        Returns:
            bool: True on success
            
        Warning:
            This function is for factory maintenance only.
            Incorrect calibration can affect measurement accuracy.
        """
        # Use calibration address
        original_address = self.address
        self.address = self.CALIBRATION_ADDRESS
        
        response = self._send_command(self.CALIBRATION)
        
        # Restore original address
        self.address = original_address
        
        if response:
            logging.info("Calibration command sent successfully")
            return True
        
        return False
    
    def get_all_measurements(self) -> Dict[str, Any]:
        """
        Get all measurement values in a single call.
        
        Returns:
            dict: Complete measurement data
        """
        return self.read_measurements()
    
    def print_measurements(self):
        """Print all current measurements in a formatted way."""
        measurements = self.read_measurements()
        
        print("=== PZEM-004T Measurements ===")
        print(f"Voltage:      {measurements['voltage']:6.1f} V")
        print(f"Current:      {measurements['current']:6.3f} A")
        print(f"Power:        {measurements['power']:6.1f} W")
        print(f"Energy:       {measurements['energy']:6.3f} kWh")
        print(f"Frequency:    {measurements['frequency']:6.1f} Hz")
        print(f"Power Factor: {measurements['power_factor']:6.2f}")
        print(f"Alarm Status: {'ON' if measurements['alarm_status'] else 'OFF'}")
        print("=" * 32)
    
    def close(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            logging.info("Serial connection closed")


# Legacy class name for backward compatibility
PZEM004Tv30 = PZEM004T


if __name__ == '__main__':
    # Example usage
    try:
        # Initialize PZEM-004T
        # Change port to match your system
        pzem = PZEM004T(port='/dev/ttyUSB0')
        
        # Read and display measurements
        pzem.print_measurements()
        
        # Example: Set power alarm threshold to 1000W
        # if pzem.set_power_alarm_threshold(1000):
        #     print("Power alarm threshold set to 1000W")
        
        # Example: Reset energy counter
        # if pzem.reset_energy():
        #     print("Energy counter reset")
        #     time.sleep(1)
        #     pzem.print_measurements()
        
        # Example: Get current alarm threshold
        # threshold = pzem.get_power_alarm_threshold()
        # if threshold:
        #     print(f"Current alarm threshold: {threshold}W")
        
        pzem.close()
        
    except Exception as e:
        print(f"Error: {e}")
