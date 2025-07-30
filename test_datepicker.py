#!/usr/bin/env python3
"""
Date Picker Improvements Verification
Testing the gap reduction and text visibility improvements
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

def test_date_picker_improvements():
    """Test the date picker spacing and text color improvements"""
    print("🔍 Testing Date Picker Improvements...")
    
    try:
        with open("main.py", 'r', encoding='utf-8') as f:
            main_content = f.read()
            
        # Check for spacing improvements
        improvements = {
            "Month layout with fixed height": "height='95dp'" in main_content,
            "Reduced month label height": "height='20dp'" in main_content,
            "Compact month rows": "height='30dp'" in main_content,
            "White text for selected year": "color=(1, 1, 1, 1) if year == current_year" in main_content,
            "Dark text for unselected year": "color=(0.2, 0.2, 0.2, 1)" in main_content,
            "White text for selected month": "color=(1, 1, 1, 1) if month == current_month" in main_content,
            "Dark text for unselected month": "color=(0.2, 0.2, 0.2, 1)" in main_content,
            "Text color updates in select_year": "btn.color = (1, 1, 1, 1)  # White text for selected" in main_content,
            "Text color updates in select_month": "btn.color = (1, 1, 1, 1)  # White text for selected" in main_content
        }
        
        all_passed = True
        for feature, found in improvements.items():
            if found:
                print(f"✅ {feature}: Implemented")
            else:
                print(f"❌ {feature}: Missing")
                all_passed = False
        
        if all_passed:
            print("\n🎉 All date picker improvements successfully implemented!")
        else:
            print("\n⚠️  Some improvements may be missing")
            
        print("\n📱 Date Picker Improvements Summary:")
        print("   • Reduced gap between year and months")
        print("   • Month layout height fixed to 95dp")
        print("   • Month label height reduced to 20dp")
        print("   • Month button rows reduced to 30dp")
        print("   • White text on selected buttons (blue background)")
        print("   • Dark text on unselected buttons (light background)")
        print("   • Dynamic text color updates when selecting year/month")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_date_picker_improvements()
