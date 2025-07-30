#!/usr/bin/env python3
"""
Test OCR functionality with the created test image
"""

import pytesseract
from PIL import Image
import os

def test_ocr():
    """Test OCR functionality with the test image"""
    
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
            print(f"\n✓ OCR successful! Extracted {len(extracted_text.strip())} characters")
        else:
            print("\n✗ No text extracted")
            
    except Exception as e:
        print(f"OCR Error: {e}")

if __name__ == "__main__":
    test_ocr()
