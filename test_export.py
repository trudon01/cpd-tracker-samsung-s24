#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from main import CPDScreen
import sqlite3
import csv
from datetime import datetime

def test_export():
    """Test the export functionality"""
    try:
        # Create a CPDScreen instance to test export
        screen = CPDScreen()
        
        # Call export method
        screen.export_to_csv()
        
        # Check if export file was created
        export_dir = os.path.join("cpd_tracker", "exports")
        if os.path.exists(export_dir):
            files = [f for f in os.listdir(export_dir) if f.endswith('.csv')]
            if files:
                latest_file = os.path.join(export_dir, files[-1])
                print(f"✓ Export file created: {files[-1]}")
                
                # Read and display first few lines
                with open(latest_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"✓ File contains {len(lines)} lines")
                    if lines:
                        print("Header:", lines[0].strip())
                        if len(lines) > 1:
                            print("Sample data:", lines[1].strip())
            else:
                print("❌ No CSV files found in exports directory")
        else:
            print("❌ Exports directory not found")
            
    except Exception as e:
        print(f"❌ Export test failed: {e}")

if __name__ == "__main__":
    test_export()
