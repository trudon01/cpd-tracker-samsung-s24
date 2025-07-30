#!/usr/bin/env python3
"""
Test OCR functionality with explicit Tesseract path
"""

import pytesseract
from PIL import Image
import os

def test_ocr_with_path():
    """Test OCR functionality with explicit Tesseract path"""
    
    # Set Tesseract path explicitly
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    image_path = "cpd_tracker/assets/photos/test_ocr_image.png"
    
    if not os.path.exists(image_path):
        print(f"Test image not found: {image_path}")
        return
    
    try:
        # Load the image
        image = Image.open(image_path)
        print(f"Testing OCR on image: {image_path}")
        print(f"Image size: {image.size}")
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image, config='--psm 6')
        
        print("\n" + "="*50)
        print("EXTRACTED TEXT:")
        print("="*50)
        print(extracted_text)
        print("="*50)
        
        if extracted_text.strip():
            print(f"\n✅ OCR successful! Extracted {len(extracted_text.strip())} characters")
            print(f"📝 Lines detected: {len(extracted_text.strip().split(chr(10)))}")
            
            # Show what would happen in the app
            print("\n🎯 IN THE CPD TRACKER APP:")
            print("1. This text would appear in the OCR dialog")
            print("2. User could edit and select portions")
            print("3. Selected text would be added to description field")
            
        else:
            print("\n⚠️ No text extracted")
            
    except Exception as e:
        print(f"OCR Error: {e}")

if __name__ == "__main__":
    test_ocr_with_path()
