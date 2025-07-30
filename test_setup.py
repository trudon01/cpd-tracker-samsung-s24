#!/usr/bin/env python3
"""
CPD Tracker - Setup Test Script
This script tests various components of the CPD Tracker app to ensure everything is working correctly.
"""

import os
import sys
import traceback
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import kivy
        print(f"✓ Kivy {kivy.__version__}")
    except ImportError as e:
        print(f"✗ Kivy import failed: {e}")
        return False
    
    try:
        import kivymd
        print(f"✓ KivyMD {kivymd.__version__}")
    except ImportError as e:
        print(f"✗ KivyMD import failed: {e}")
        return False
    
    try:
        from google.oauth2.service_account import Credentials
        print("✓ Google Auth")
    except ImportError as e:
        print(f"✗ Google Auth import failed: {e}")
        return False
    
    try:
        from googleapiclient.discovery import build
        print("✓ Google API Client")
    except ImportError as e:
        print(f"✗ Google API Client import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database initialization and operations"""
    print("\nTesting database...")
    
    try:
        from database import init_db, insert_entry, get_entries_count
        
        # Test database initialization
        init_db()
        print("✓ Database initialized")
        
        # Test entry insertion
        test_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date_start": "2025-07-01",
            "date_end": "2025-07-02",
            "name": "Test Entry",
            "type": "Other",
            "description": "This is a test entry",
            "photo": ""
        }
        
        entry_id = insert_entry(test_data)
        print(f"✓ Test entry inserted with ID: {entry_id}")
        
        # Test entry count
        count = get_entries_count()
        print(f"✓ Database contains {count} entries")
        
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_directories():
    """Test if required directories can be created"""
    print("\nTesting directory structure...")
    
    try:
        # Create required directories
        directories = [
            "cpd_tracker",
            "cpd_tracker/assets",
            "cpd_tracker/assets/photos",
            "cpd_tracker/backups"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            if os.path.exists(directory):
                print(f"✓ Directory created: {directory}")
            else:
                print(f"✗ Failed to create directory: {directory}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Directory test failed: {e}")
        return False

def test_backup_system():
    """Test backup system functionality"""
    print("\nTesting backup system...")
    
    try:
        from backup import create_backup, is_backup_needed
        
        # Test backup check
        backup_needed = is_backup_needed()
        print(f"✓ Backup check completed: {'needed' if backup_needed else 'not needed'}")
        
        # Test backup creation (without upload)
        if os.path.exists("cpd_tracker/cpd.db"):
            zip_path, entries_count = create_backup()
            if os.path.exists(zip_path):
                print(f"✓ Backup created: {zip_path} ({entries_count} entries)")
                return True
            else:
                print("✗ Backup file not found")
                return False
        else:
            print("! Skipping backup test (no database file)")
            return True
        
    except Exception as e:
        print(f"✗ Backup test failed: {e}")
        traceback.print_exc()
        return False

def test_google_drive():
    """Test Google Drive connectivity (if credentials exist)"""
    print("\nTesting Google Drive...")
    
    if not os.path.exists("credentials.json"):
        print("! Skipping Google Drive test (credentials.json not found)")
        print("  Create credentials.json following the setup guide to enable Google Drive")
        return True
    
    try:
        from drive_upload import test_drive_connection
        
        success = test_drive_connection()
        if success:
            print("✓ Google Drive connection successful")
            return True
        else:
            print("✗ Google Drive connection failed")
            return False
        
    except Exception as e:
        print(f"✗ Google Drive test failed: {e}")
        return False

def test_app_components():
    """Test main app components without starting the GUI"""
    print("\nTesting app components...")
    
    try:
        # Test main imports
        from main import CPDScreen, CPDApp
        print("✓ Main app classes imported")
        
        # Test KV file exists
        if os.path.exists("cpd.kv"):
            print("✓ UI layout file found")
        else:
            print("✗ cpd.kv file not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ App component test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("CPD Tracker - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Directories", test_directories),
        ("Database", test_database),
        ("App Components", test_app_components),
        ("Backup System", test_backup_system),
        ("Google Drive", test_google_drive),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        print("-" * 20)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} test FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your CPD Tracker is ready to go.")
        print("Run 'python main.py' to start the application.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the errors above and refer to the setup guide.")
    
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
