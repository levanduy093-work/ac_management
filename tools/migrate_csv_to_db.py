#!/usr/bin/env python3
"""
Migration script to convert CSV data to SQLite database
Converts existing CSV files to the new database format
"""

import sys
import os
import glob
import pandas as pd
from datetime import datetime
import argparse

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database import PZEMDatabase

def migrate_csv_to_db(csv_file, db, dry_run=False):
    """
    Migrate CSV data to database
    
    Args:
        csv_file: Path to CSV file
        db: Database instance
        dry_run: If True, only show what would be migrated without actually doing it
        
    Returns:
        Number of records migrated
    """
    try:
        print(f"📁 Processing: {csv_file}")
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        if df.empty:
            print(f"   ⚠️  File is empty, skipping")
            return 0
        
        print(f"   📊 Found {len(df)} records")
        
        if dry_run:
            print(f"   🔍 DRY RUN: Would migrate {len(df)} records")
            return len(df)
        
        # Migrate each record
        migrated_count = 0
        for _, row in df.iterrows():
            try:
                # Convert data types and handle missing values
                sensor_data = {
                    'port': str(row['port']),
                    'voltage': float(row['voltage_v']) if pd.notna(row['voltage_v']) else 0.0,
                    'current': float(row['current_a']) if pd.notna(row['current_a']) else 0.0,
                    'power': float(row['power_w']) if pd.notna(row['power_w']) else 0.0,
                    'energy': float(row['energy_wh']) if pd.notna(row['energy_wh']) else 0.0,
                    'frequency': float(row['frequency_hz']) if pd.notna(row['frequency_hz']) else 0.0,
                    'power_factor': float(row['power_factor']) if pd.notna(row['power_factor']) else 0.0,
                    'alarm': str(row['alarm_status']).upper() == 'ON' if pd.notna(row['alarm_status']) else False,
                    'timestamp': datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
                }
                
                # Save to database
                if db.save_measurement(sensor_data):
                    migrated_count += 1
                else:
                    print(f"   ❌ Failed to save record at {row['datetime']}")
                    
            except Exception as e:
                print(f"   ❌ Error processing record at {row.get('datetime', 'unknown')}: {e}")
                continue
        
        print(f"   ✅ Successfully migrated {migrated_count}/{len(df)} records")
        return migrated_count
        
    except Exception as e:
        print(f"   ❌ Error reading CSV file: {e}")
        return 0

def find_csv_files(csv_dir="data/csv_logs"):
    """
    Find all CSV files in the specified directory
    
    Args:
        csv_dir: Directory containing CSV files
        
    Returns:
        List of CSV file paths
    """
    if not os.path.exists(csv_dir):
        print(f"❌ Directory not found: {csv_dir}")
        return []
    
    # Find all CSV files
    csv_pattern = os.path.join(csv_dir, "*.csv")
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"❌ No CSV files found in {csv_dir}")
        return []
    
    return sorted(csv_files)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Migrate CSV data to SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run - show what would be migrated
  python migrate_csv_to_db.py --dry-run
  
  # Migrate all CSV files
  python migrate_csv_to_db.py
  
  # Migrate specific CSV file
  python migrate_csv_to_db.py --csv-file data/csv_logs/pzem__dev_ttyUSB0.csv
  
  # Migrate with custom database path
  python migrate_csv_to_db.py --db-path custom_database.db
        """
    )
    
    parser.add_argument('--csv-dir', default='data/csv_logs',
                       help='Directory containing CSV files (default: data/csv_logs)')
    parser.add_argument('--csv-file', 
                       help='Specific CSV file to migrate (overrides --csv-dir)')
    parser.add_argument('--db-path', default='data/pzem_data.db',
                       help='Database file path (default: data/pzem_data.db)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be migrated without actually doing it')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup of CSV files after successful migration')
    
    args = parser.parse_args()
    
    print("🔄 CSV to Database Migration Tool")
    print("=" * 50)
    
    # Initialize database
    try:
        db = PZEMDatabase(args.db_path)
        print(f"💾 Connected to database: {db.db_path}")
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return 1
    
    # Show database stats before migration
    print("\n📊 Database before migration:")
    try:
        stats = db.get_database_stats()
        print(f"   📊 Total Measurements: {stats['total_measurements']:,}")
        print(f"   🔌 Total Sensors: {stats['total_sensors']}")
    except Exception as e:
        print(f"   ⚠️  Could not get database stats: {e}")
    
    # Find CSV files to migrate
    if args.csv_file:
        csv_files = [args.csv_file] if os.path.exists(args.csv_file) else []
    else:
        csv_files = find_csv_files(args.csv_dir)
    
    if not csv_files:
        print("❌ No CSV files found to migrate")
        return 1
    
    print(f"\n📁 Found {len(csv_files)} CSV file(s) to migrate:")
    for csv_file in csv_files:
        print(f"   📄 {csv_file}")
    
    if args.dry_run:
        print(f"\n🔍 DRY RUN MODE - No data will be actually migrated")
    
    # Confirm migration
    if not args.dry_run:
        response = input(f"\n❓ Proceed with migration? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ Migration cancelled")
            return 0
    
    # Perform migration
    print(f"\n🚀 Starting migration...")
    total_migrated = 0
    successful_files = 0
    
    for csv_file in csv_files:
        try:
            migrated_count = migrate_csv_to_db(csv_file, db, args.dry_run)
            if migrated_count > 0:
                total_migrated += migrated_count
                successful_files += 1
        except Exception as e:
            print(f"❌ Error migrating {csv_file}: {e}")
    
    # Show results
    print(f"\n📊 Migration Results:")
    print(f"   📁 Files processed: {len(csv_files)}")
    print(f"   ✅ Successful files: {successful_files}")
    print(f"   📊 Total records migrated: {total_migrated:,}")
    
    # Show database stats after migration
    if not args.dry_run and total_migrated > 0:
        print(f"\n📊 Database after migration:")
        try:
            stats = db.get_database_stats()
            print(f"   📊 Total Measurements: {stats['total_measurements']:,}")
            print(f"   🔌 Total Sensors: {stats['total_sensors']}")
            print(f"   📁 Database Size: {stats['database_size_mb']} MB")
        except Exception as e:
            print(f"   ⚠️  Could not get database stats: {e}")
    
    # Backup CSV files if requested
    if args.backup and not args.dry_run and total_migrated > 0:
        print(f"\n💾 Creating backups of CSV files...")
        backup_dir = f"{args.csv_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        for csv_file in csv_files:
            try:
                backup_file = os.path.join(backup_dir, os.path.basename(csv_file))
                import shutil
                shutil.copy2(csv_file, backup_file)
                print(f"   ✅ Backed up: {os.path.basename(csv_file)}")
            except Exception as e:
                print(f"   ❌ Failed to backup {csv_file}: {e}")
        
        print(f"   📁 Backup directory: {backup_dir}")
    
    print(f"\n✅ Migration completed!")
    
    if not args.dry_run and total_migrated > 0:
        print(f"\n💡 Next steps:")
        print(f"   1. Test the database: make db-stats")
        print(f"   2. View sensor summary: make db-sensors")
        print(f"   3. View latest data: make db-latest")
        print(f"   4. Start monitoring with database: make run-monitor-db")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 