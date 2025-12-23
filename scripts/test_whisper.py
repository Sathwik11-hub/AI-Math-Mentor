#!/usr/bin/env python3
"""
Quick test to verify Whisper is working
"""

print("=" * 60)
print("  WHISPER TEST")
print("=" * 60)

try:
    import whisper
    print("\n✓ Whisper imported successfully")
    print(f"  Version: {whisper.__version__}")
    
    print("\n✓ Loading Whisper base model...")
    model = whisper.load_model("base")
    print("✓ Model loaded successfully")
    
    print("\n" + "=" * 60)
    print("  ✅ WHISPER IS READY!")
    print("=" * 60)
    print("\nYou can now use audio transcription in the app.")
    print("Note: First transcription will be slower as it downloads the model.")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\n" + "=" * 60)
    print("  ❌ WHISPER TEST FAILED")
    print("=" * 60)
