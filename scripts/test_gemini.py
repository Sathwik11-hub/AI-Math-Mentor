#!/usr/bin/env python3
"""Quick Gemini API test"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

print("=" * 60)
print("  GEMINI API QUICK TEST")
print("=" * 60)

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"\n1. API Key: {'Found' if api_key else 'NOT FOUND'}")
if api_key:
    print(f"   First 8 chars: {api_key[:8]}...")

# Check model name
model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')
print(f"\n2. Model: {model_name}")

# Try to import and configure
print(f"\n3. Testing Gemini connection...")
try:
    import google.generativeai as genai  # type: ignore
    print("   ✓ google.generativeai imported")
    
    genai.configure(api_key=api_key)  # type: ignore
    print("   ✓ API key configured")
    
    model = genai.GenerativeModel(model_name)  # type: ignore
    print(f"   ✓ Model '{model_name}' loaded")
    
    # Try a simple generation
    print("\n4. Testing generate_content...")
    response = model.generate_content("Say 'Hello from Gemini!'")
    print(f"   ✓ Response received:")
    print(f"   {response.text}")
    
    print("\n" + "=" * 60)
    print("  ✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYour Gemini API is working correctly!")
    print("You can now run: cd backend && streamlit run app_minimal.py")
    
except Exception as e:
    print(f"\n   ✗ Error: {e}")
    print("\n" + "=" * 60)
    print("  ❌ TEST FAILED")
    print("=" * 60)
    
    print("\n💡 Possible fixes:")
    print("1. Check your API key at: https://makersuite.google.com/app/apikey")
    print("2. Verify the key has Gemini API access enabled")
    print("3. Check if you have API quota remaining")
    print("4. Try model 'gemini-pro' instead of 'gemini-1.5-flash'")
    
    import traceback
    print("\nFull error traceback:")
    traceback.print_exc()
