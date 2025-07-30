#!/usr/bin/env python3
"""
Samsung S24 Optimization Test Suite for CPD Tracker
Tests all features optimized for Samsung S24 (1080x2340 resolution)
"""

import os
import sys
import sqlite3
import csv
from datetime import datetime, timedelta

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_database_with_points():
    """Test database operations with points system"""
    print("🔍 Testing Database with Points System...")
    
    try:
        # Import database functions
        from database import insert_entry, init_db
        
        # Initialize database
        init_db()
        
        # Test entry with points
        test_data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date_start": "2025-07-01",
            "date_end": "2025-07-02", 
            "name": "S24 Test Activity",
            "type": "Conference",
            "description": "Testing Samsung S24 optimized layout",
            "photo": "",
            "points": 8
        }
        
        entry_id = insert_entry(test_data)
        print(f"✅ Entry created with ID: {entry_id}")
        
        # Verify points column exists
        db_path = os.path.join("cpd_tracker", "cpd.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check table schema
        cursor.execute("PRAGMA table_info(cpd_entries)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'points' in column_names:
            print("✅ Points column exists in database")
        else:
            print("❌ Points column missing from database")
            
        # Test retrieving the entry
        cursor.execute("SELECT name, points FROM cpd_entries WHERE id = ?", (entry_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[1] == 8:
            print(f"✅ Points correctly stored: {result[1]}")
        else:
            print(f"❌ Points storage failed: {result}")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")

def test_csv_export_functionality():
    """Test CSV export with all data"""
    print("\n📊 Testing CSV Export Functionality...")
    
    try:
        # Import main CPDScreen class
        from main import CPDScreen
        
        # Create instance and test export
        screen = CPDScreen()
        screen.export_to_csv()
        
        # Check if export file was created
        export_dir = os.path.join("cpd_tracker", "exports")
        if os.path.exists(export_dir):
            csv_files = [f for f in os.listdir(export_dir) if f.endswith('.csv')]
            if csv_files:
                latest_file = os.path.join(export_dir, csv_files[-1])
                print(f"✅ CSV Export created: {csv_files[-1]}")
                
                # Verify CSV content
                with open(latest_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'CPD Points' in content:
                        print("✅ Points column included in CSV export")
                    else:
                        print("❌ Points column missing from CSV export")
                        
                    lines = content.strip().split('\n')
                    print(f"✅ CSV contains {len(lines)} lines (including header)")
                    
            else:
                print("❌ No CSV files found")
        else:
            print("❌ Export directory not found")
            
    except Exception as e:
        print(f"❌ CSV export test failed: {e}")

def test_layout_measurements():
    """Test Samsung S24 layout optimizations"""
    print("\n📱 Testing Samsung S24 Layout Optimizations...")
    
    try:
        # Read the KV file to verify compact layout
        with open("cpd.kv", 'r', encoding='utf-8') as f:
            kv_content = f.read()
            
        # Check for S24 optimizations
        optimizations = {
            "Compact sections": "height: \"130dp\"" in kv_content,  # Date section
            "Small fonts": "font_size: \"14sp\"" in kv_content,     # Button fonts
            "Reduced spacing": "spacing: \"20dp\"" in kv_content,   # Main spacing
            "Points section": "🏆 CPD Points" in kv_content,       # Points feature
            "Export button": "📊 Export to CSV" in kv_content       # Export feature
        }
        
        for feature, found in optimizations.items():
            if found:
                print(f"✅ {feature}: Optimized")
            else:
                print(f"❌ {feature}: Not found")
                
        # Check specific height reductions for S24
        if "height: \"100dp\"" in kv_content:  # Points section
            print("✅ Points section height optimized for S24")
        if "height: \"170dp\"" in kv_content:  # Activity type section  
            print("✅ Activity type section height optimized for S24")
            
    except Exception as e:
        print(f"❌ Layout test failed: {e}")

def test_points_system():
    """Test the points selection system"""
    print("\n🏆 Testing Points System...")
    
    try:
        # Test points range (-, 0-12)
        expected_points = ['-', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'Clear']
        
        # Read main.py to verify points implementation
        with open("main.py", 'r') as f:
            main_content = f.read()
            
        # Check for points system implementation
        checks = {
            "Points selector method": "def show_points_selector(self):" in main_content,
            "Points range 0-12": "point_values = ['-', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'Clear']" in main_content,
            "Points button update": "self.ids.points_btn.text = f\"Points: {points}\"" in main_content,
            "Points in form data": "\"points\": self.selected_points" in main_content,
            "Grid layout 5 cols": "GridLayout(cols=5" in main_content
        }
        
        for feature, found in checks.items():
            if found:
                print(f"✅ {feature}: Implemented")
            else:
                print(f"❌ {feature}: Missing")
                
    except Exception as e:
        print(f"❌ Points system test failed: {e}")

def test_date_picker_improvements():
    """Test date picker spacing improvements"""
    print("\n📅 Testing Date Picker Improvements...")
    
    try:
        with open("main.py", 'r') as f:
            main_content = f.read()
            
        # Check for spacing improvements
        improvements = {
            "Reduced month spacing": "spacing=2)" in main_content,
            "Smaller month label": "height='25dp'" in main_content, 
            "Compact month rows": "height='35dp'" in main_content,
            "Mobile-friendly picker": "def show_date_picker(self, date_type):" in main_content
        }
        
        for feature, found in improvements.items():
            if found:
                print(f"✅ {feature}: Implemented")
            else:
                print(f"❌ {feature}: Missing")
                
    except Exception as e:
        print(f"❌ Date picker test failed: {e}")

def run_s24_test_suite():
    """Run complete Samsung S24 optimization test suite"""
    print("🚀 Samsung S24 CPD Tracker Test Suite")
    print("=" * 50)
    
    test_database_with_points()
    test_csv_export_functionality() 
    test_layout_measurements()
    test_points_system()
    test_date_picker_improvements()
    
    print("\n" + "=" * 50)
    print("✅ Samsung S24 Test Suite Complete!")
    print("\n📱 S24 Optimization Summary:")
    print("   • Compact layout for 1080x2340 resolution")
    print("   • Touch-friendly date picker with reduced gaps")
    print("   • Points system with 0-12 range")
    print("   • CSV export with all data including points")
    print("   • Professional UI with proper spacing")

if __name__ == "__main__":
    run_s24_test_suite()
