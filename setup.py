#!/usr/bin/env python3
"""
Setup script for AQI vs Transport Usage Dashboard
This script helps users set up and run the dashboard quickly
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def generate_sample_data():
    """Generate sample data if it doesn't exist"""
    if not os.path.exists('sample_transport_data.csv') or not os.path.exists('sample_aqi_data.csv'):
        print("📊 Generating sample data...")
        try:
            from data_fetcher import save_sample_data
            save_sample_data()
            print("✅ Sample data generated successfully!")
            return True
        except Exception as e:
            print(f"❌ Error generating sample data: {e}")
            return False
    else:
        print("✅ Sample data already exists!")
        return True

def run_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching dashboard...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

def main():
    """Main setup function"""
    print("🚌 AQI vs Transport Usage Dashboard Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    required_files = ['dashboard.py', 'data_fetcher.py', 'data_processor.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure you're in the correct directory with all project files.")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return
    
    # Generate sample data
    if not generate_sample_data():
        print("❌ Setup failed during data generation")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 You can now:")
    print("   1. Run 'streamlit run dashboard.py' to start the dashboard")
    print("   2. Or run this script again to launch automatically")
    
    # Ask user if they want to launch now
    try:
        launch = input("\n🚀 Launch dashboard now? (y/n): ").lower().strip()
        if launch in ['y', 'yes']:
            run_dashboard()
    except KeyboardInterrupt:
        print("\n👋 Setup completed. Run 'streamlit run dashboard.py' when ready!")

if __name__ == "__main__":
    main()