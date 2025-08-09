#!/usr/bin/env python3
"""
Startup script for PZEM-004T Web Monitoring Dashboard
Easy-to-use script to launch the web server
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'jinja2',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Please install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_database():
    """Check if database exists and has data"""
    db_path = Path("data/pzem_data.db")
    
    if not db_path.exists():
        print("⚠️  Database not found. Please run sensor monitoring first:")
        print("   python tools/read_ac_sensor_db.py")
        print("   or")
        print("   make run-monitor-db")
        return False
    
    print(f"✅ Database found: {db_path}")
    print(f"   Size: {db_path.stat().st_size / 1024:.1f} KB")
    return True

def main():
    parser = argparse.ArgumentParser(description='PZEM-004T Web Dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    parser.add_argument('--skip-checks', action='store_true', help='Skip requirement and database checks')
    
    args = parser.parse_args()
    
    print("🔌 PZEM-004T Web Monitoring Dashboard")
    print("=" * 50)
    
    # Check requirements
    if not args.skip_checks:
        print("🔍 Checking requirements...")
        if not check_requirements():
            sys.exit(1)
        
        print("🔍 Checking database...")
        if not check_database():
            print("⚠️  Warning: No database found. Dashboard will have limited functionality.")
            response = input("Continue anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                sys.exit(1)
    
    # Change to web directory
    web_dir = Path(__file__).parent / "web"
    os.chdir(web_dir)
    
    print(f"\n🚀 Starting web server...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Dashboard: http://{args.host}:{args.port}")
    print(f"   API Docs: http://{args.host}:{args.port}/docs")
    print(f"   Reload: {'Enabled' if args.reload else 'Disabled'}")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Build uvicorn command
    cmd = [
        sys.executable, "-m", "uvicorn",
        "api:app",
        "--host", args.host,
        "--port", str(args.port),
        "--log-level", "info"
    ]
    
    if args.reload:
        cmd.append("--reload")
    
    try:
        # Run uvicorn
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
