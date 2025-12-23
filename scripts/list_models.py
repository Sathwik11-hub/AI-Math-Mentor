#!/usr/bin/env python3
"""List available Gemini models"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

import google.generativeai as genai

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("Error: GEMINI_API_KEY not found")
    exit(1)

genai.configure(api_key=api_key)  # type: ignore[attr-defined]

print("=" * 70)
print("  AVAILABLE GEMINI MODELS")
print("=" * 70)

try:
    models = genai.list_models()  # type: ignore[attr-defined]
    
    print(f"\nFound {len(list(models))} models:\n")
    
    # List again since generator was consumed
    for model in genai.list_models():  # type: ignore[attr-defined]
        # Check if it supports generateContent
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description[:100]}...")
            print(f"  Supported: {', '.join(model.supported_generation_methods)}")
            print()
    
    print("=" * 70)
    print("\n💡 To use a model, set in .env:")
    print("   GEMINI_MODEL=models/gemini-pro")
    print("   or")
    print("   GEMINI_MODEL=models/gemini-1.5-flash")
    print("\nNote: Include the 'models/' prefix!")
    
except Exception as e:
    print(f"Error listing models: {e}")
    import traceback
    traceback.print_exc()
