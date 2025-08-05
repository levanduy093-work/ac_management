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
    
    Technical Specifications (from datasheet):
    - Voltage: 80-260V, resolution 0.1V, accuracy ±0.5%
    - Current: 0-10A (10A model) / 0-100A (100A model), resolution 0.001A, accuracy ±0.5%
    - Power: 0-2.3kW (10A) / 0-23kW (100A), resolution 0.1W, accuracy ±0.5%
    - Energy: 0-9999.99kWh, resolution 1Wh, accuracy ±0.5%
    - Frequency: 45-65Hz, resolution 0.1Hz, accuracy ±0.5%
    - Power Factor: 0.00-1.00, resolution 0.01, accuracy ±1%
    - Starting current: 0.01A (10A model) / 0.02A (100A model)
    - Starting power: 0.4W
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
    
    # Resolution factors (from datasheet)
    VOLTAGE_RESOLUTION = 0.1      # 1 LSB = 0.1V
    CURRENT_RESOLUTION = 0.001    # 1 LSB = 0.001A
    POWER_RESOLUTION = 0.1        # 1 LSB = 0.1W
    ENERGY_RESOLUTION = 1.0       # 1 LSB = 1Wh
    FREQUENCY_RESOLUTION = 0.1    # 1 LSB = 0.1Hz
    PF_RESOLUTION = 0.01          # 1 LSB = 0.01
    
    # Measurement ranges (from datasheet)
    VOLTAGE_MIN = 80.0            # Minimum voltage (V)
    VOLTAGE_MAX = 260.0           # Maximum voltage (V)
    CURRENT_MIN_10A = 0.0         # Minimum current for 10A model (A)
    CURRENT_MAX_10A = 10.0        # Maximum current for 10A model (A)
    CURRENT_MIN_100A = 0.0        # Minimum current for 100A model (A)
    CURRENT_MAX_100A = 100.0      # Maximum current for 100A model (A)
    POWER_MIN = 0.0               # Minimum power (W)
    POWER_MAX_10A = 2300.0        # Maximum power for 10A model (W)
    POWER_MAX_100A = 23000.0      # Maximum power for 100A model (W)
    ENERGY_MIN = 0.0              # Minimum energy (kWh)
    ENERGY_MAX = 9999.99          # Maximum energy (kWh)
    FREQUENCY_MIN = 45.0          # Minimum frequency (Hz)
    FREQUENCY_MAX = 65.0          # Maximum frequency (Hz)
    PF_MIN = 0.00                 # Minimum power factor
    PF_MAX = 1.00                 # Maximum power factor
    
    # Starting measurement thresholds (from datasheet)
    STARTING_CURRENT_10A = 0.01   # Starting current for 10A model (A)
    STARTING_CURRENT_100A = 0.02  # Starting current for 100A model (A)
    STARTING_POWER = 0.4          # Starting power (W)
    
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
            # Reset command: addr + func + crc (4 bytes total)
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
            # Reset response: addr + func + crc (4 bytes total)
            # According to documentation: slave address + 0x42 + CRC check high byte + CRC check low byte
            response = self.serial.read(4)
            if len(response) < 4:
                logging.error(f"Reset energy response too short: {len(response)} bytes")
                return None
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
    
    def test_reset_support(self) -> bool:
        """
        Test if the device supports reset energy command.
        
        Returns:
            bool: True if device responds to reset command
        """
        try:
            # Clear input buffer
            self.serial.flushInput()
            
            # Send reset command
            packet = struct.pack('>BB', self.address, self.RESET_ENERGY)
            packet += self._crc16(packet)
            
            self.serial.write(packet)
            
            # Wait longer for device to process
            time.sleep(0.3)
            
            # Read response with timeout
            response = b''
            start_time = time.time()
            timeout = 1.0  # 1 second timeout
            
            while len(response) < 4 and (time.time() - start_time) < timeout:
                chunk = self.serial.read(1)
                if chunk:
                    response += chunk
                else:
                    time.sleep(0.01)
            
            if response and len(response) >= 2:
                # Check if device responded (even if it's an error)
                if response[1] in [0x42, 0xC2]:
                    return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Error testing reset support: {e}")
            return False
    
    def reset_energy(self, verify_reset: bool = True) -> bool:
        """
        Reset energy counter to zero.
        
        Args:
            verify_reset: If True, verify the reset by reading energy value after reset
            
        Note: Some PZEM devices may not send a response to the reset command.
        This method assumes success if the command is sent properly.
        
        Returns:
            bool: True on success
        """
        try:
            # Get current energy value before reset
            energy_before = None
            if verify_reset:
                measurements = self.get_all_measurements()
                if measurements:
                    energy_before = measurements['energy']
                    logging.debug(f"Energy before reset: {energy_before:.3f} kWh")
            
            # Clear input buffer before sending command
            if self.serial and self.serial.is_open:
                self.serial.flushInput()
            
            # Build reset command
            packet = struct.pack('>BB', self.address, self.RESET_ENERGY)
            packet += self._crc16(packet)
            
            logging.debug(f"Reset energy command: {packet.hex()}")
            
            # Send command
            self.serial.write(packet)
            
            # Wait for device to process the command
            time.sleep(0.1)
            
            # Try to read response (optional - device may not respond)
            response = self.serial.read(4)
            
            reset_confirmed = False
            
            if response and len(response) >= 2:
                logging.debug(f"Reset energy response: {response.hex()}")
                
                # If device responds, validate the response
                if len(response) >= 4 and self._validate_crc(response):
                    # Check for error response (0xC2)
                    if response[1] == 0xC2:
                        error_code = response[2] if len(response) > 2 else 0
                        self._handle_error(error_code)
                        return False
                    
                    # Check for success response (0x42)
                    if response[1] == 0x42:
                        logging.info("Energy counter reset successfully (confirmed)")
                        reset_confirmed = True
            
            # If no response or invalid response, assume success
            # (This is the behavior of the original library)
            if not reset_confirmed:
                logging.info("Energy counter reset (assumed success)")
            
            # Clear cached energy value
            self._measurements['energy'] = 0.0
            
            # Verify reset by reading energy value
            if verify_reset and energy_before is not None:
                time.sleep(0.5)  # Wait for device to update
                measurements = self.get_all_measurements()
                if measurements:
                    energy_after = measurements['energy']
                    logging.debug(f"Energy after reset: {energy_after:.3f} kWh")
                    
                    if energy_after < energy_before:
                        logging.info(f"Reset verified: Energy decreased from {energy_before:.3f} to {energy_after:.3f} kWh")
                        return True
                    elif energy_after == 0.0:
                        logging.info("Reset verified: Energy is now 0.0 kWh")
                        return True
                    else:
                        logging.warning(f"Reset may have failed: Energy is {energy_after:.3f} kWh (was {energy_before:.3f} kWh)")
                        return False
            
            return True
            
        except Exception as e:
            logging.error(f"Exception during reset energy: {e}")
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
    
    def format_measurements(self) -> Dict[str, str]:
        """
        Format measurements according to datasheet display rules.
        
        Returns:
            dict: Formatted measurement strings
        """
        measurements = self.read_measurements()
        
        # Format power according to datasheet rules
        power = measurements['power']
        if power < 1000:
            power_str = f"{power:.1f}W"
        else:
            power_str = f"{power:.0f}W"
        
        # Format energy according to datasheet rules
        energy = measurements['energy']
        if energy < 10:
            energy_str = f"{energy * 1000:.0f}Wh"  # Convert kWh to Wh
        else:
            energy_str = f"{energy:.2f}kWh"
        
        return {
            'voltage': f"{measurements['voltage']:.1f}V",
            'current': f"{measurements['current']:.3f}A",
            'power': power_str,
            'energy': energy_str,
            'frequency': f"{measurements['frequency']:.1f}Hz",
            'power_factor': f"{measurements['power_factor']:.2f}",
            'alarm_status': 'ON' if measurements['alarm_status'] else 'OFF'
        }
    
    def print_measurements(self):
        """Print all current measurements in a formatted way according to datasheet display rules."""
        measurements = self.read_measurements()
        
        # Format power according to datasheet rules
        power = measurements['power']
        if power < 1000:
            power_str = f"{power:.1f}"
        else:
            power_str = f"{power:.0f}"
        
        # Format energy according to datasheet rules
        energy = measurements['energy']
        if energy < 10:
            energy_str = f"{energy * 1000:.0f} Wh"  # Convert kWh to Wh
        else:
            energy_str = f"{energy:.2f} kWh"
        
        print("=== PZEM-004T Measurements ===")
        print(f"Voltage:      {measurements['voltage']:6.1f} V")
        print(f"Current:      {measurements['current']:6.3f} A")
        print(f"Power:        {power_str:>6} W")
        print(f"Energy:       {energy_str:>10}")
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
