#!/usr/bin/env python3
"""
Database GUI Tool for PZEM-004T data
Simple interactive menu for database operations
"""

import sys
import os
from datetime import datetime, timedelta
import csv
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import PZEMDatabase

class DatabaseGUI:
    """Simple GUI for database operations"""
    
    def __init__(self, db_path="data/pzem_data.db"):
        """Initialize the GUI"""
        self.db_path = db_path
        self.db = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize database connection"""
        try:
            self.db = PZEMDatabase(self.db_path)
            print(f"✅ Connected to database: {self.db_path}")
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            sys.exit(1)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_header(self):
        """Show application header"""
        print("=" * 80)
        print("🔌 PZEM-004T Database Query Tool")
        print("=" * 80)
        print()
    
    def show_main_menu(self):
        """Show main menu options"""
        print("📋 Main Menu:")
        print("1. 📊 View Database Statistics")
        print("2. 🔌 View Sensor Summary")
        print("3. 📈 View Latest Measurements")
        print("4. 📁 Export Data")
        print("5. 🗑️  Cleanup Old Data")
        print("6. 🔍 Advanced Queries")
        print("0. ❌ Exit")
        print()
    
    def get_user_choice(self, min_choice=0, max_choice=6):
        """Get user choice with validation"""
        while True:
            try:
                choice = input("Enter your choice (0-6): ").strip()
                choice = int(choice)
                if min_choice <= choice <= max_choice:
                    return choice
                else:
                    print(f"❌ Please enter a number between {min_choice} and {max_choice}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def show_database_stats(self):
        """Show database statistics"""
        self.clear_screen()
        self.show_header()
        print("📊 Database Statistics")
        print("-" * 40)
        
        try:
            stats = self.db.get_database_stats()
            
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
        
        input("\nPress Enter to continue...")
    
    def show_sensor_summary(self):
        """Show sensor summary"""
        self.clear_screen()
        self.show_header()
        print("🔌 Sensor Summary")
        print("-" * 80)
        
        try:
            sensors = self.db.get_sensor_summary()
            
            if not sensors:
                print("❌ No sensors found in database")
            else:
                for i, sensor in enumerate(sensors, 1):
                    print(f"{i}. 🔌 Port: {sensor['port']}")
                    print(f"   📍 Device Address: 0x{sensor['device_address']:02X} ({sensor['device_address']})")
                    print(f"   📅 First Seen: {sensor['first_seen']}")
                    print(f"   📅 Last Seen: {sensor['last_seen']}")
                    print(f"   📊 Total Readings: {sensor['total_readings']:,}")
                    print(f"   📊 Total Measurements: {sensor['total_measurements']:,}")
                    print(f"   📅 Last Measurement: {sensor['last_measurement'] or 'N/A'}")
                    print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error getting sensor summary: {e}")
        
        input("\nPress Enter to continue...")
    
    def show_latest_measurements(self):
        """Show latest measurements"""
        self.clear_screen()
        self.show_header()
        print("📈 Latest Measurements")
        print("-" * 100)
        
        try:
            # Get number of records to show
            while True:
                try:
                    limit = input("How many latest measurements to show? (default: 10): ").strip()
                    if not limit:
                        limit = 10
                    else:
                        limit = int(limit)
                    if limit > 0:
                        break
                    else:
                        print("❌ Please enter a positive number")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            data = self.db.get_latest_measurements(limit)
            
            if not data:
                print("❌ No data found in database")
            else:
                print(f"📊 Latest {len(data)} Measurements:")
                print("=" * 100)
                
                for i, record in enumerate(data, 1):
                    print(f"{i:2d}. {record['timestamp']} | {record['port']} | "
                          f"V:{record['voltage']:6.1f}V | I:{record['current']:6.3f}A | "
                          f"P:{record['power']:7.1f}W | E:{record['energy']:8.0f}Wh | "
                          f"F:{record['frequency']:4.1f}Hz | PF:{record['power_factor']:4.2f} | "
                          f"Alarm:{'ON' if record['alarm_status'] else 'OFF'}")
            
        except Exception as e:
            print(f"❌ Error getting latest data: {e}")
        
        input("\nPress Enter to continue...")
    
    def export_data_menu(self):
        """Export data menu"""
        while True:
            self.clear_screen()
            self.show_header()
            print("📁 Export Data")
            print("-" * 40)
            print("1. 📊 Export to CSV")
            print("2. 📄 Export to JSON")
            print("3. 🔙 Back to Main Menu")
            print()
            
            choice = self.get_user_choice(1, 3)
            
            if choice == 1:
                self.export_to_csv()
            elif choice == 2:
                self.export_to_json()
            elif choice == 3:
                break
    
    def export_to_csv(self):
        """Export data to CSV"""
        self.clear_screen()
        self.show_header()
        print("📊 Export to CSV")
        print("-" * 40)
        
        try:
            # Get export parameters
            filename = input("Enter output filename (default: export.csv): ").strip()
            if not filename:
                filename = "export.csv"
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            # Get port filter
            port = input("Enter port to filter (e.g., /dev/ttyUSB0) or press Enter for all: ").strip()
            if not port:
                port = None
            
            # Get days filter
            days = input("Enter number of days to look back (press Enter for all): ").strip()
            if days:
                try:
                    days = int(days)
                except ValueError:
                    days = None
            else:
                days = None
            
            # Get limit
            limit = input("Enter maximum records to export (press Enter for 1000): ").strip()
            if limit:
                try:
                    limit = int(limit)
                except ValueError:
                    limit = 1000
            else:
                limit = 1000
            
            print(f"\n🔄 Exporting data...")
            
            # Get data
            if port:
                data = self.db.get_measurements_by_port(port, limit)
            else:
                data = self.db.get_latest_measurements(limit)
            
            if not data:
                print("❌ No data found for export")
                input("\nPress Enter to continue...")
                return
            
            # Filter by days if specified
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                data = [row for row in data if datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date]
            
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'port', 'voltage', 'current', 'power', 'energy', 'frequency', 'power_factor', 'alarm_status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✅ Successfully exported {len(data)} records to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
        
        input("\nPress Enter to continue...")
    
    def export_to_json(self):
        """Export data to JSON"""
        self.clear_screen()
        self.show_header()
        print("📄 Export to JSON")
        print("-" * 40)
        
        try:
            # Get export parameters
            filename = input("Enter output filename (default: export.json): ").strip()
            if not filename:
                filename = "export.json"
            if not filename.endswith('.json'):
                filename += '.json'
            
            # Get port filter
            port = input("Enter port to filter (e.g., /dev/ttyUSB0) or press Enter for all: ").strip()
            if not port:
                port = None
            
            # Get days filter
            days = input("Enter number of days to look back (press Enter for all): ").strip()
            if days:
                try:
                    days = int(days)
                except ValueError:
                    days = None
            else:
                days = None
            
            # Get limit
            limit = input("Enter maximum records to export (press Enter for 1000): ").strip()
            if limit:
                try:
                    limit = int(limit)
                except ValueError:
                    limit = 1000
            else:
                limit = 1000
            
            print(f"\n🔄 Exporting data...")
            
            # Get data
            if port:
                data = self.db.get_measurements_by_port(port, limit)
            else:
                data = self.db.get_latest_measurements(limit)
            
            if not data:
                print("❌ No data found for export")
                input("\nPress Enter to continue...")
                return
            
            # Filter by days if specified
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                data = [row for row in data if datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S') >= cutoff_date]
            
            # Write to JSON
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"✅ Successfully exported {len(data)} records to {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting to JSON: {e}")
        
        input("\nPress Enter to continue...")
    
    def cleanup_data(self):
        """Cleanup old data"""
        self.clear_screen()
        self.show_header()
        print("🗑️  Cleanup Old Data")
        print("-" * 40)
        
        try:
            # Get days to keep
            while True:
                try:
                    days = input("Enter number of days to keep (default: 30): ").strip()
                    if not days:
                        days = 30
                    else:
                        days = int(days)
                    if days > 0:
                        break
                    else:
                        print("❌ Please enter a positive number")
                except ValueError:
                    print("❌ Please enter a valid number")
            
            # Confirm cleanup
            print(f"\n⚠️  This will delete all measurements older than {days} days")
            confirm = input("Are you sure? (y/N): ").strip().lower()
            
            if confirm in ['y', 'yes']:
                print(f"\n🔄 Cleaning up old data...")
                deleted_count = self.db.cleanup_old_data(days)
                print(f"✅ Cleaned up {deleted_count} old measurements")
                
                # Show updated stats
                print(f"\n📊 Updated Database Statistics:")
                stats = self.db.get_database_stats()
                print(f"   📊 Total Measurements: {stats['total_measurements']:,}")
                print(f"   📁 Database Size: {stats['database_size_mb']} MB")
            else:
                print("❌ Cleanup cancelled")
            
        except Exception as e:
            print(f"❌ Error cleaning up data: {e}")
        
        input("\nPress Enter to continue...")
    
    def advanced_queries(self):
        """Advanced queries menu"""
        while True:
            self.clear_screen()
            self.show_header()
            print("🔍 Advanced Queries")
            print("-" * 40)
            print("1. 📊 Query by Port")
            print("2. 📅 Query by Date Range")
            print("3. 📈 Query Statistics")
            print("4. 🔙 Back to Main Menu")
            print()
            
            choice = self.get_user_choice(1, 4)
            
            if choice == 1:
                self.query_by_port()
            elif choice == 2:
                self.query_by_date_range()
            elif choice == 3:
                self.query_statistics()
            elif choice == 4:
                break
    
    def query_by_port(self):
        """Query data by specific port"""
        self.clear_screen()
        self.show_header()
        print("📊 Query by Port")
        print("-" * 40)
        
        try:
            # Get port
            port = input("Enter port to query (e.g., /dev/ttyUSB0): ").strip()
            if not port:
                print("❌ Port is required")
                input("\nPress Enter to continue...")
                return
            
            # Get limit
            limit = input("Enter number of records to show (default: 20): ").strip()
            if not limit:
                limit = 20
            else:
                limit = int(limit)
            
            print(f"\n🔄 Querying data for port {port}...")
            
            data = self.db.get_measurements_by_port(port, limit)
            
            if not data:
                print(f"❌ No data found for port {port}")
            else:
                print(f"📊 Found {len(data)} measurements for {port}:")
                print("=" * 100)
                
                for i, record in enumerate(data, 1):
                    print(f"{i:2d}. {record['timestamp']} | "
                          f"V:{record['voltage']:6.1f}V | I:{record['current']:6.3f}A | "
                          f"P:{record['power']:7.1f}W | E:{record['energy']:8.0f}Wh | "
                          f"F:{record['frequency']:4.1f}Hz | PF:{record['power_factor']:4.2f} | "
                          f"Alarm:{'ON' if record['alarm_status'] else 'OFF'}")
            
        except Exception as e:
            print(f"❌ Error querying by port: {e}")
        
        input("\nPress Enter to continue...")
    
    def query_by_date_range(self):
        """Query data by date range"""
        self.clear_screen()
        self.show_header()
        print("📅 Query by Date Range")
        print("-" * 40)
        
        try:
            # Get date range
            print("Enter date range (YYYY-MM-DD format):")
            start_date = input("Start date: ").strip()
            end_date = input("End date: ").strip()
            
            if not start_date or not end_date:
                print("❌ Both start and end dates are required")
                input("\nPress Enter to continue...")
                return
            
            # Validate dates
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD")
                input("\nPress Enter to continue...")
                return
            
            print(f"\n🔄 Querying data from {start_date} to {end_date}...")
            
            # Get all data and filter by date
            data = self.db.get_latest_measurements(10000)  # Get large number
            
            filtered_data = []
            for record in data:
                record_dt = datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
                if start_dt <= record_dt <= end_dt:
                    filtered_data.append(record)
            
            if not filtered_data:
                print(f"❌ No data found for the specified date range")
            else:
                print(f"📊 Found {len(filtered_data)} measurements in date range:")
                print("=" * 100)
                
                for i, record in enumerate(filtered_data[:20], 1):  # Show first 20
                    print(f"{i:2d}. {record['timestamp']} | {record['port']} | "
                          f"V:{record['voltage']:6.1f}V | I:{record['current']:6.3f}A | "
                          f"P:{record['power']:7.1f}W | E:{record['energy']:8.0f}Wh | "
                          f"F:{record['frequency']:4.1f}Hz | PF:{record['power_factor']:4.2f} | "
                          f"Alarm:{'ON' if record['alarm_status'] else 'OFF'}")
                
                if len(filtered_data) > 20:
                    print(f"... and {len(filtered_data) - 20} more records")
            
        except Exception as e:
            print(f"❌ Error querying by date range: {e}")
        
        input("\nPress Enter to continue...")
    
    def query_statistics(self):
        """Query statistical information"""
        self.clear_screen()
        self.show_header()
        print("📈 Query Statistics")
        print("-" * 40)
        
        try:
            # Get all data for analysis
            data = self.db.get_latest_measurements(10000)
            
            if not data:
                print("❌ No data found for analysis")
                input("\nPress Enter to continue...")
                return
            
            # Group by port
            port_data = {}
            for record in data:
                port = record['port']
                if port not in port_data:
                    port_data[port] = []
                port_data[port].append(record)
            
            print("📊 Statistical Summary by Port:")
            print("=" * 80)
            
            for port, records in port_data.items():
                if not records:
                    continue
                
                voltages = [r['voltage'] for r in records]
                currents = [r['current'] for r in records]
                powers = [r['power'] for r in records]
                energies = [r['energy'] for r in records]
                
                print(f"🔌 Port: {port}")
                print(f"   📊 Records: {len(records)}")
                print(f"   ⚡ Voltage: Avg={sum(voltages)/len(voltages):.1f}V, Min={min(voltages):.1f}V, Max={max(voltages):.1f}V")
                print(f"   🔌 Current: Avg={sum(currents)/len(currents):.3f}A, Min={min(currents):.3f}A, Max={max(currents):.3f}A")
                print(f"   💡 Power: Avg={sum(powers)/len(powers):.1f}W, Min={min(powers):.1f}W, Max={max(powers):.1f}W")
                print(f"   🔋 Energy: Total={sum(energies):.0f}Wh")
                print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error querying statistics: {e}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main application loop"""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_main_menu()
            
            choice = self.get_user_choice()
            
            if choice == 0:
                print("👋 Goodbye!")
                break
            elif choice == 1:
                self.show_database_stats()
            elif choice == 2:
                self.show_sensor_summary()
            elif choice == 3:
                self.show_latest_measurements()
            elif choice == 4:
                self.export_data_menu()
            elif choice == 5:
                self.cleanup_data()
            elif choice == 6:
                self.advanced_queries()

def main():
    """Main function"""
    print("🔌 PZEM-004T Database GUI Tool")
    print("=" * 50)
    
    # Get database path
    db_path = input("Enter database path (default: data/pzem_data.db): ").strip()
    if not db_path:
        db_path = "data/pzem_data.db"
    
    # Create and run GUI
    gui = DatabaseGUI(db_path)
    gui.run()

if __name__ == "__main__":
    main() 