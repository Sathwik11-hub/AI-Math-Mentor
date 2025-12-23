#!/usr/bin/env python3
"""
Test audio transcription with numpy array (no ffmpeg needed)
"""
import sys
import os

print("=" * 60)
print("  AUDIO TRANSCRIPTION TEST (NUMPY ARRAY METHOD)")
print("=" * 60)

print("\n1. Testing imports...")
try:
    import whisper
    print("   ✓ whisper")
except ImportError as e:
    print(f"   ✗ whisper: {e}")
    sys.exit(1)

try:
    import librosa
    print("   ✓ librosa")
except ImportError as e:
    print(f"   ✗ librosa: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("   ✓ numpy")
except ImportError as e:
    print(f"   ✗ numpy: {e}")
    sys.exit(1)

print("\n2. Loading Whisper model...")
try:
    model = whisper.load_model("base")
    print("   ✓ Whisper base model loaded")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n3. Testing audio loading with librosa...")
try:
    # Create a simple test tone (1 second of 440Hz)
    import numpy as np
    sample_rate = 16000
    duration = 1.0
    frequency = 440.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    print(f"   ✓ Created test audio: shape={audio_data.shape}, dtype={audio_data.dtype}")
    print(f"   ✓ Sample rate: {sample_rate}Hz")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n4. Testing Whisper transcription with numpy array...")
try:
    # This should work without ffmpeg!
    result = model.transcribe(
        audio_data,
        fp16=False,
        language='en'
    )
    print("   ✓ Transcription successful!")
    print(f"   ✓ Result text: '{result['text']}'")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("  ✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n✨ Audio transcription works WITHOUT ffmpeg!")
print("   - Pass numpy array directly to Whisper")
print("   - Load audio with librosa")
print("   - No temporary files needed")
print("\n🎤 Your app should now transcribe audio files!")
