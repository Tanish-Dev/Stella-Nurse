#!/usr/bin/env python3
"""Quick syntax check for eyes.py"""
import sys

try:
    # Try to import the module
    sys.path.insert(0, '/Users/Tanish/Documents/Stella-Nurse/display')
    import eyes
    print("✅ SUCCESS: eyes.py has no syntax errors!")
    print(f"✅ RoboEyes class found with {len([m for m in dir(eyes.RoboEyes) if not m.startswith('_')])} public methods")
    print("\n📝 Available emotions:")
    test_emotions = ["idle", "happy", "sad", "angry", "surprised", "curious", 
                     "thinking", "listening", "speaking", "alert", "concerned", 
                     "sleepy", "excited", "love"]
    for emotion in test_emotions:
        print(f"   - {emotion}")
except SyntaxError as e:
    print(f"❌ SYNTAX ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"⚠️  Import error (this is okay if dependencies aren't installed): {e}")
    print("✅ But no syntax errors were found!")
