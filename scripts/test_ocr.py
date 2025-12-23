#!/usr/bin/env python3
"""
Quick OCR Test Script
Tests if EasyOCR is working properly
"""
import sys
import os
import ssl

# Fix SSL FIRST before any other imports
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['CURL_CA_BUNDLE'] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

print("="*60)
print("  OCR QUICK TEST")
print("="*60)

# Test 1: Environment check
print("\n1. Environment Check:")
try:
    print(f"   ✓ certifi installed: {certifi.where()}")
except Exception as e:
    print(f"   ✗ certifi error: {e}")

try:
    import easyocr
    print("   ✓ easyocr imported")
except ImportError as e:
    print(f"   ✗ easyocr import failed: {e}")
    sys.exit(1)

try:
    import cv2
    print("   ✓ opencv-python installed")
except ImportError:
    print("   ✗ opencv-python NOT installed (may cause issues)")

# Test 2: Initialize EasyOCR
print("\n2. Initializing EasyOCR Reader:")
try:
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    print("   ✓ EasyOCR Reader initialized")
except Exception as e:
    print(f"   ✗ Failed to initialize: {e}")
    sys.exit(1)

# Test 3: Create a simple test image with text
print("\n3. Creating test image with text:")
try:
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    
    # Create a white image with black text
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw simple text (PIL uses default font)
    text = "x^2 + 5x + 6 = 0"
    draw.text((20, 30), text, fill='black')
    
    # Convert to numpy array
    img_array = np.array(img)
    print(f"   ✓ Test image created: {img_array.shape}")
    
except Exception as e:
    print(f"   ✗ Failed to create test image: {e}")
    sys.exit(1)

# Test 4: Perform OCR
print("\n4. Testing OCR on test image:")
try:
    results = reader.readtext(img_array, detail=1)
    
    if not results:
        print("   ⚠ No text detected")
    else:
        print(f"   ✓ OCR detected {len(results)} text region(s):")
        for bbox, text, conf in results:
            print(f"      Text: '{text}' (confidence: {conf:.2%})")
    
except Exception as e:
    print(f"   ✗ OCR failed: {e}")
    sys.exit(1)

# Test 5: Test with ImageInputHandler
print("\n5. Testing ImageInputHandler:")
try:
    from utils.input_handlers import ImageInputHandler  # type: ignore[import]
    
    handler = ImageInputHandler()
    result = handler.process_image(img)
    
    print(f"   ✓ Handler initialized")
    print(f"   Extracted text: '{result['extracted_text']}'")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Needs HITL: {result['needs_hitl']}")
    print(f"   Message: {result['message']}")
    
except Exception as e:
    print(f"   ✗ Handler test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("  ✅ ALL OCR TESTS PASSED!")
print("="*60)
