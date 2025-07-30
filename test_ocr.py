#!/usr/bin/env python3
"""
Test script to create a sample image with text for OCR testing
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """Create a test image with text for OCR testing"""
    
    # Create a white background image
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        # Try to use a larger font
        font_size = 40
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Sample text that might appear in a CPD certificate or document
    test_text = [
        "Professional Development Certificate",
        "Course: Advanced Data Analytics",
        "Date: January 15, 2025",
        "Duration: 8 hours",
        "Points: 10 CPD Points",
        "Completed by: John Smith"
    ]
    
    # Draw the text on the image
    y_position = 30
    for line in test_text:
        if font:
            draw.text((50, y_position), line, fill='black', font=font)
        else:
            draw.text((50, y_position), line, fill='black')
        y_position += 50
    
    # Save the test image
    test_dir = "cpd_tracker/assets/photos"
    os.makedirs(test_dir, exist_ok=True)
    
    image_path = os.path.join(test_dir, "test_ocr_image.png")
    img.save(image_path)
    
    print(f"Test image created: {image_path}")
    return image_path

if __name__ == "__main__":
    create_test_image()
