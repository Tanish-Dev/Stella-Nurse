#!/usr/bin/env python3
"""Quick test to see the improvements - just a few key emotions"""
import time
import sys

try:
    from display_driver import init_display
    from eyes import RoboEyes
    
    print("🤖 Testing Improved Eye Animations")
    print("=" * 50)
    
    disp = init_display()
    eyes = RoboEyes(device=disp, fps=60, display_type="adafruit")
    eyes.start()
    
    # Test key different emotions
    tests = [
        ("idle", "Normal eyes, gentle wander"),
        ("happy", "SQUINTED wide - notice the shape!"),
        ("sad", "VERY droopy and narrow"),
        ("surprised", "VERY WIDE with pupils"),
        ("thinking", "Looking away up-right"),
        ("sleepy", "Almost closed, very droopy"),
    ]
    
    for emotion, desc in tests:
        print(f"\n{emotion.upper()}: {desc}")
        eyes.set_state(emotion)
        time.sleep(4)
    
    print("\n✅ Done! Notice:")
    print("   - Smoother movement (less jittery)")
    print("   - More distinct shapes between emotions")
    print("   - Mostly blue (except alert/angry/love)")
    print("   - Better corner rounding")
    
    eyes.stop()
    
except KeyboardInterrupt:
    print("\n\nInterrupted!")
    eyes.stop()
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
