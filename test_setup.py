#!/usr/bin/env python3
"""
Test script to verify the AQI vs Transport Dashboard setup
"""

import sys
import os
import pandas as pd
import numpy as np

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from data_fetcher import AQIDataFetcher, TransportDataGenerator
        print("✅ Data fetcher modules imported successfully")
    except ImportError as e:
        print(f"❌ Data fetcher import failed: {e}")
        return False
    
    try:
        from data_processor import DataProcessor
        print("✅ Data processor imported successfully")
    except ImportError as e:
        print(f"❌ Data processor import failed: {e}")
        return False
    
    return True

def test_data_generation():
    """Test data generation functionality"""
    print("\n📊 Testing data generation...")
    
    try:
        from data_fetcher import TransportDataGenerator, save_sample_data
        
        # Test transport data generation
        generator = TransportDataGenerator('2024-01-01', days=10)
        transport_df = generator.generate_transport_data()
        
        if len(transport_df) == 20:  # 10 days * 2 modes
            print("✅ Transport data generation working")
        else:
            print(f"❌ Transport data generation issue: expected 20 records, got {len(transport_df)}")
            return False
        
        # Test sample data creation
        save_sample_data()
        
        if os.path.exists('sample_transport_data.csv') and os.path.exists('sample_aqi_data.csv'):
            print("✅ Sample data files created successfully")
        else:
            print("❌ Sample data files not created")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Data generation test failed: {e}")
        return False

def test_data_processing():
    """Test data processing functionality"""
    print("\n🔄 Testing data processing...")
    
    try:
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        
        # Load sample data
        transport_df = processor.load_transport_data('sample_transport_data.csv')
        aqi_df = processor.load_aqi_data('sample_aqi_data.csv')
        
        print(f"✅ Loaded {len(transport_df)} transport records")
        print(f"✅ Loaded {len(aqi_df)} AQI records")
        
        # Test merging
        merged_df = processor.merge_datasets(aqi_df, transport_df)
        print(f"✅ Merged dataset has {len(merged_df)} records")
        
        # Test correlations
        correlations = processor.calculate_correlations(merged_df)
        print(f"✅ Calculated {len(correlations)} correlations")
        
        # Test summary statistics
        summary = processor.get_summary_statistics(merged_df)
        print(f"✅ Generated summary statistics for {summary['total_days']} days")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        return False

def test_dashboard_components():
    """Test dashboard component loading"""
    print("\n🎨 Testing dashboard components...")
    
    try:
        # Import dashboard functions (without running the app)
        import importlib.util
        spec = importlib.util.spec_from_file_location("dashboard", "dashboard.py")
        dashboard_module = importlib.util.module_from_spec(spec)
        
        # This will test if the dashboard file is syntactically correct
        spec.loader.exec_module(dashboard_module)
        print("✅ Dashboard module loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard component test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    test_files = ['sample_transport_data.csv', 'sample_aqi_data.csv']
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🧹 Cleaned up {file}")
            except Exception as e:
                print(f"⚠️ Could not remove {file}: {e}")

def main():
    """Run all tests"""
    print("🧪 AQI vs Transport Dashboard - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Generation Test", test_data_generation),
        ("Data Processing Test", test_data_processing),
        ("Dashboard Components Test", test_dashboard_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the dashboard, run:")
        print("   streamlit run dashboard.py")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
        print("💡 Try running: pip install -r requirements.txt")
    
    # Ask about cleanup
    try:
        cleanup = input("\n🧹 Clean up test files? (y/n): ").lower().strip()
        if cleanup in ['y', 'yes']:
            cleanup_test_files()
    except KeyboardInterrupt:
        print("\n👋 Test completed!")

if __name__ == "__main__":
    main()