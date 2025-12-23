#!/usr/bin/env python3
"""
Check API Quota Status
Provides information about current quota usage and availability
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()

print("="*70)
print("  GEMINI API QUOTA STATUS CHECK")
print("="*70)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Check API Key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    sys.exit(1)

print(f"1. API Key: {api_key[:20]}...{api_key[-4:]}")
print(f"   Length: {len(api_key)} characters\n")

# Check Model
model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.5-flash')
print(f"2. Model: {model_name}\n")

# Test API
print("3. Testing API Connection:")
try:
    genai.configure(api_key=api_key)  # type: ignore[attr-defined]
    model = genai.GenerativeModel(model_name)  # type: ignore[attr-defined]
    
    print("   Attempting to generate content...")
    response = model.generate_content("Say 'OK' if you can read this")
    
    print("   ✅ SUCCESS! API is working!")
    print(f"   Response: {response.text}")
    print(f"\n{'='*70}")
    print("  STATUS: API KEY IS WORKING ✅")
    print(f"{'='*70}")
    print("\n💡 Your API key has available quota!")
    print("   You can now use the application normally.\n")
    
except Exception as e:
    error = str(e)
    
    if '429' in error or 'quota' in error.lower():
        print("   ❌ QUOTA EXCEEDED\n")
        print(f"{'='*70}")
        print("  STATUS: QUOTA EXHAUSTED ⚠️")
        print(f"{'='*70}")
        
        # Try to extract retry delay
        import re
        match = re.search(r'retry in ([\d.]+)s', error)
        if match:
            retry_delay = float(match.group(1))
            minutes = int(retry_delay // 60)
            seconds = int(retry_delay % 60)
            print(f"\n⏰ Quota will reset in: {minutes}m {seconds}s")
        
        # Check if daily limit
        if "GenerateRequestsPerDayPerProjectPerModel" in error:
            print("\n📊 Daily Quota Limit Reached:")
            print("   • Free tier: 20 requests/day")
            print("   • Resets: Every 24 hours")
            print("   • All models share the same daily quota")
        
        print("\n🔧 Solutions:")
        print("   1. ⏰ Wait for automatic reset")
        print("   2. 🔑 Create new Google Cloud project + new API key")
        print("   3. 💳 Upgrade to paid plan ($0.075/1M tokens)")
        
        print("\n📝 Useful Links:")
        print("   • Check usage: https://ai.dev/usage?tab=rate-limit")
        print("   • Rate limits: https://ai.google.dev/gemini-api/docs/rate-limits")
        print("   • Pricing: https://ai.google.dev/pricing")
        print("   • New API key: https://aistudio.google.com/apikey")
        
    elif '404' in error:
        print(f"   ❌ MODEL NOT FOUND: {model_name}")
        print(f"\n   Try running: python3 scripts/list_models.py")
        
    else:
        print(f"   ❌ ERROR: {error}")

print(f"\n{'='*70}\n")
