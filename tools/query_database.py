#!/usr/bin/env python3
"""
Database query tool for PZEM-004T data
Provides various ways to query and export data from the SQLite database
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
import csv
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import PZEMDatabase

def export_to_csv(db, output_file, port=None, days=None, limit=None):
    """
    Export data to CSV file
    
    Args:
        db: Database instance
        output_file: Output CSV file path
        port: Filter by specific port
        days: Number of days to look back
        limit: Maximum number of records
    """
    try:
        if port:
            data = db.get_measurements_by_port(port, limit or 1000)
        else:
            data = db.get_latest_measurements(limit or 1000)
        
        if not data:
            print("❌ No data found for export")
            return False
        
        # Filter by days if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            data = [row for row in data if datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date]
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'port', 'voltage', 'current', 'power', 'energy', 'frequency', 'power_factor', 'alarm_status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Exported {len(data)} records to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return False

def export_to_json(db, output_file, port=None, days=None, limit=None):
    """
    Export data to JSON file
    
    Args:
        db: Database instance
        output_file: Output JSON file path
        port: Filter by specific port
        days: Number of days to look back
        limit: Maximum number of records
    """
    try:
        if port:
            data = db.get_measurements_by_port(port, limit or 1000)
        else:
            data = db.get_latest_measurements(limit or 1000)
        
        if not data:
            print("❌ No data found for export")
            return False
        
        # Filter by days if specified
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            data = [row for row in data if datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date]
        
        # Write to JSON
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(data)} records to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting to JSON: {e}")
        return False

def show_sensor_summary(db):
    """Display sensor summary"""
    try:
        sensors = db.get_sensor_summary()
        
        if not sensors:
            print("❌ No sensors found in database")
            return
        
        print("\n📊 Sensor Summary:")
        print("=" * 80)
        
        for sensor in sensors:
            print(f"🔌 Port: {sensor['port']}")
            print(f"   📍 Device Address: 0x{sensor['device_address']:02X} ({sensor['device_address']})")
            print(f"   📅 First Seen: {sensor['first_seen']}")
            print(f"   📅 Last Seen: {sensor['last_seen']}")
            print(f"   📊 Total Readings: {sensor['total_readings']:,}")
            print(f"   📊 Total Measurements: {sensor['total_measurements']:,}")
            print(f"   📅 Last Measurement: {sensor['last_measurement'] or 'N/A'}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error getting sensor summary: {e}")

def show_database_stats(db):
    """Display database statistics"""
    try:
        stats = db.get_database_stats()
        
        print("\n📊 Database Statistics:")
        print("=" * 40)
        print(f"📁 Database Size: {stats['database_size_mb']} MB")
        print(f"📊 Total Measurements: {stats['total_measurements']:,}")
        print(f"🔌 Total Sensors: {stats['total_sensors']}")
        
        if stats['oldest_measurement'] and stats['newest_measurement']:
            print(f"📅 Oldest Measurement: {stats['oldest_measurement']}")
            print(f"📅 Newest Measurement: {stats['newest_measurement']}")
            
            # Calculate data span
            oldest = datetime.strptime(stats['oldest_measurement'], '%Y-%m-%d %H:%M:%S')
            newest = datetime.strptime(stats['newest_measurement'], '%Y-%m-%d %H:%M:%S')
            span = newest - oldest
            print(f"⏱️  Data Span: {span.days} days, {span.seconds // 3600} hours")
            
    except Exception as e:
        print(f"❌ Error getting database stats: {e}")

def show_latest_data(db, limit=10):
    """Display latest measurements"""
    try:
        data = db.get_latest_measurements(limit)
        
        if not data:
            print("❌ No data found in database")
            return
        
        print(f"\n📊 Latest {len(data)} Measurements:")
        print("=" * 100)
        
        for i, record in enumerate(data, 1):
            print(f"{i:2d}. {record['timestamp']} | {record['port']} | "
                  f"V:{record['voltage']:6.1f}V | I:{record['current']:6.3f}A | "
                  f"P:{record['power']:7.1f}W | E:{record['energy']:8.0f}Wh | "
                  f"F:{record['frequency']:4.1f}Hz | PF:{record['power_factor']:4.2f} | "
                  f"Alarm:{'ON' if record['alarm_status'] else 'OFF'}")
                  
    except Exception as e:
        print(f"❌ Error getting latest data: {e}")

def cleanup_database(db, days_to_keep):
    """Clean up old data"""
    try:
        deleted_count = db.cleanup_old_data(days_to_keep)
        print(f"🗑️  Cleaned up {deleted_count} old measurements (older than {days_to_keep} days)")
        
        # Show updated stats
        show_database_stats(db)
        
    except Exception as e:
        print(f"❌ Error cleaning up database: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Query and export PZEM-004T data from SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show database statistics
  python query_database.py --stats
  
  # Show sensor summary
  python query_database.py --sensors
  
  # Show latest 20 measurements
  python query_database.py --latest 20
  
  # Export last 7 days to CSV
  python query_database.py --export-csv data_export.csv --days 7
  
  # Export specific port to JSON
  python query_database.py --export-json /dev/ttyUSB0_data.json --port /dev/ttyUSB0
  
  # Clean up data older than 30 days
  python query_database.py --cleanup 30
        """
    )
    
    parser.add_argument('--stats', action='store_true', 
                       help='Show database statistics')
    parser.add_argument('--sensors', action='store_true',
                       help='Show sensor summary')
    parser.add_argument('--latest', type=int, metavar='N',
                       help='Show latest N measurements (default: 10)')
    parser.add_argument('--export-csv', metavar='FILE',
                       help='Export data to CSV file')
    parser.add_argument('--export-json', metavar='FILE',
                       help='Export data to JSON file')
    parser.add_argument('--port', metavar='PORT',
                       help='Filter by specific port (e.g., /dev/ttyUSB0)')
    parser.add_argument('--days', type=int, metavar='N',
                       help='Filter data from last N days')
    parser.add_argument('--limit', type=int, metavar='N',
                       help='Limit number of records to export')
    parser.add_argument('--cleanup', type=int, metavar='DAYS',
                       help='Clean up data older than N days')
    parser.add_argument('--db-path', metavar='PATH',
                       default='data/pzem_data.db',
                       help='Database file path (default: data/pzem_data.db)')
    
    args = parser.parse_args()
    
    # Check if any action is specified
    if not any([args.stats, args.sensors, args.latest, args.export_csv, 
                args.export_json, args.cleanup]):
        parser.print_help()
        return
    
    # Initialize database
    try:
        db = PZEMDatabase(args.db_path)
        print(f"💾 Connected to database: {db.db_path}")
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return
    
    # Execute requested actions
    if args.stats:
        show_database_stats(db)
    
    if args.sensors:
        show_sensor_summary(db)
    
    if args.latest:
        show_latest_data(db, args.latest)
    
    if args.export_csv:
        export_to_csv(db, args.export_csv, args.port, args.days, args.limit)
    
    if args.export_json:
        export_to_json(db, args.export_json, args.port, args.days, args.limit)
    
    if args.cleanup:
        cleanup_database(db, args.cleanup)

if __name__ == "__main__":
    main() 