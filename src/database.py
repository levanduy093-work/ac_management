"""
Database module for PZEM-004T data logging
Provides SQLite database operations for storing sensor data
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

class PZEMDatabase:
    """SQLite database manager for PZEM-004T sensor data"""
    
    def __init__(self, db_path: str = "data/pzem_data.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_directory()
        self._create_tables()
    
    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create sensors table to track sensor information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    port TEXT UNIQUE NOT NULL,
                    device_address INTEGER DEFAULT 248,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_readings INTEGER DEFAULT 0
                )
            ''')
            
            # Create measurements table for sensor data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    voltage REAL,
                    current REAL,
                    power REAL,
                    energy REAL,
                    frequency REAL,
                    power_factor REAL,
                    alarm_status BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                )
            ''')
            
            # Create indexes for better query performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_measurements_timestamp 
                ON measurements(timestamp)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_measurements_sensor_id 
                ON measurements(sensor_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sensors_port 
                ON sensors(port)
            ''')
            
            conn.commit()
    
    def get_or_create_sensor(self, port: str, device_address: int = 248) -> int:
        """
        Get existing sensor ID or create new sensor record
        
        Args:
            port: Serial port name
            device_address: PZEM device address (default 248 = 0xF8)
            
        Returns:
            Sensor ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Try to get existing sensor
            cursor.execute(
                'SELECT id FROM sensors WHERE port = ?',
                (port,)
            )
            result = cursor.fetchone()
            
            if result:
                sensor_id = result[0]
                # Update last_seen and increment total_readings
                cursor.execute('''
                    UPDATE sensors 
                    SET last_seen = CURRENT_TIMESTAMP, 
                        total_readings = total_readings + 1
                    WHERE id = ?
                ''', (sensor_id,))
                return sensor_id
            else:
                # Create new sensor
                cursor.execute('''
                    INSERT INTO sensors (port, device_address, first_seen, last_seen, total_readings)
                    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
                ''', (port, device_address))
                return cursor.lastrowid
    
    def save_measurement(self, sensor_data: Dict) -> bool:
        """
        Save sensor measurement to database
        
        Args:
            sensor_data: Dictionary containing sensor data
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Get or create sensor record
            sensor_id = self.get_or_create_sensor(sensor_data['port'])
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO measurements 
                    (sensor_id, timestamp, voltage, current, power, energy, 
                     frequency, power_factor, alarm_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sensor_id,
                    sensor_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    sensor_data['voltage'],
                    sensor_data['current'],
                    sensor_data['power'],
                    sensor_data['energy'],
                    sensor_data['frequency'],
                    sensor_data['power_factor'],
                    sensor_data['alarm']
                ))
                
                # Update sensor last_seen timestamp when new measurement is added
                cursor.execute('''
                    UPDATE sensors 
                    SET last_seen = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (sensor_id,))
                
                return True
                
        except Exception as e:
            logging.error(f"Error saving measurement to database: {e}")
            return False
    
    def get_latest_measurements(self, limit: int = 100) -> List[Dict]:
        """
        Get latest measurements from all sensors
        
        Args:
            limit: Maximum number of measurements to return
            
        Returns:
            List of measurement dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    s.port,
                    m.timestamp,
                    m.voltage,
                    m.current,
                    m.power,
                    m.energy,
                    m.frequency,
                    m.power_factor,
                    m.alarm_status
                FROM measurements m
                JOIN sensors s ON m.sensor_id = s.id
                ORDER BY m.timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            
            return [
                {
                    'port': row[0],
                    'timestamp': row[1],
                    'voltage': row[2] if row[2] is not None else 0.0,
                    'current': row[3] if row[3] is not None else 0.0,
                    'power': row[4] if row[4] is not None else 0.0,
                    'energy': row[5] if row[5] is not None else 0.0,
                    'frequency': row[6] if row[6] is not None else 0.0,
                    'power_factor': row[7] if row[7] is not None else 0.0,
                    'alarm_status': bool(row[8]) if row[8] is not None else False
                }
                for row in results
            ]
    
    def get_sensor_summary(self) -> List[Dict]:
        """
        Get summary statistics for all sensors
        
        Returns:
            List of sensor summary dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    s.port,
                    s.device_address,
                    s.first_seen,
                    s.last_seen,
                    s.total_readings,
                    COUNT(m.id) as total_measurements,
                    MAX(m.timestamp) as last_measurement
                FROM sensors s
                LEFT JOIN measurements m ON s.id = m.sensor_id
                GROUP BY s.id
                ORDER BY s.last_seen DESC
            ''')
            
            results = cursor.fetchall()
            
            return [
                {
                    'port': row[0],
                    'device_address': row[1],
                    'first_seen': row[2],
                    'last_seen': row[3],
                    'total_readings': row[4],
                    'total_measurements': row[5],
                    'last_measurement': row[6]
                }
                for row in results
            ]
    
    def get_measurements_by_port(self, port: str, limit: int = 100) -> List[Dict]:
        """
        Get measurements for a specific sensor port
        
        Args:
            port: Serial port name
            limit: Maximum number of measurements to return
            
        Returns:
            List of measurement dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    s.port,
                    m.timestamp,
                    m.voltage,
                    m.current,
                    m.power,
                    m.energy,
                    m.frequency,
                    m.power_factor,
                    m.alarm_status
                FROM measurements m
                JOIN sensors s ON m.sensor_id = s.id
                WHERE s.port = ?
                ORDER BY m.timestamp DESC
                LIMIT ?
            ''', (port, limit))
            
            results = cursor.fetchall()
            
            return [
                {
                    'port': row[0],
                    'timestamp': row[1],
                    'voltage': row[2] if row[2] is not None else 0.0,
                    'current': row[3] if row[3] is not None else 0.0,
                    'power': row[4] if row[4] is not None else 0.0,
                    'energy': row[5] if row[5] is not None else 0.0,
                    'frequency': row[6] if row[6] is not None else 0.0,
                    'power_factor': row[7] if row[7] is not None else 0.0,
                    'alarm_status': bool(row[8]) if row[8] is not None else False
                }
                for row in results
            ]
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> int:
        """
        Remove old measurements to manage database size
        
        Args:
            days_to_keep: Number of days of data to keep
            
        Returns:
            Number of records deleted
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM measurements 
                WHERE timestamp < datetime('now', '-{} days')
            '''.format(days_to_keep))
            
            deleted_count = cursor.rowcount
            conn.commit()
            
            return deleted_count
    
    def get_database_stats(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with database statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get total measurements
            cursor.execute('SELECT COUNT(*) FROM measurements')
            total_measurements = cursor.fetchone()[0]
            
            # Get total sensors
            cursor.execute('SELECT COUNT(*) FROM sensors')
            total_sensors = cursor.fetchone()[0]
            
            # Get database size from actual file size
            try:
                db_size = os.path.getsize(self.db_path)
            except OSError:
                # Fallback to SQLite pragma if file size cannot be read
                cursor.execute('SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()')
                db_size = cursor.fetchone()[0]
            
            # Get oldest and newest measurements
            cursor.execute('''
                SELECT MIN(timestamp), MAX(timestamp) FROM measurements
            ''')
            time_range = cursor.fetchone()
            
            return {
                'total_measurements': total_measurements,
                'total_sensors': total_sensors,
                'database_size_bytes': db_size,
                'database_size_mb': round(db_size / (1024 * 1024), 2),
                'oldest_measurement': time_range[0],
                'newest_measurement': time_range[1]
            } 