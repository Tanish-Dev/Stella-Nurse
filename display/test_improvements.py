#!/usr/bin/env python3
"""Test the new improvements: natural blinking, heart eyes, crescent happy"""
import time
from display_driver import init_display
from eyes import RoboEyes

print("🤖 Testing NEW Eye Improvements")
print("=" * 60)

disp = init_display()
eyes = RoboEyes(device=disp, fps=60, display_type="adafruit")
eyes.start()

print("\n1️⃣  IDLE - Watch for NATURAL BLINKING")
print("   - Look for occasional DOUBLE BLINKS (Cozmo style!)")
print("   - Blinks at random intervals (2-6 seconds)")
eyes.set_state("idle")
time.sleep(12)  # Longer to see multiple blinks

print("\n2️⃣  HAPPY - CRESCENT EYES")
print("   - Should be curved crescents, not straight lines")
print("   - Slightly taller, recognizable shape")
eyes.set_state("happy")
time.sleep(5)

print("\n3️⃣  LOVE - ❤️ HEART SHAPED EYES ❤️")
print("   - Eyes turn into RED-PINK HEARTS!")
print("   - Watch for the heart shape")
eyes.set_state("love")
time.sleep(6)

print("\n4️⃣  EXCITED - Notice taller eyes overall")
eyes.set_state("excited")
time.sleep(4)

print("\n5️⃣  Back to IDLE - More natural blinking")
eyes.set_state("idle")
time.sleep(10)

print("\n✅ Test Complete!")
print("\nKey improvements:")
print("  ✓ Cozmo-style natural blinking (random timing)")
print("  ✓ Occasional double blinks (20% chance)")
print("  ✓ Happy eyes = crescents (not straight lines)")
print("  ✓ Love eyes = ❤️ HEARTS ❤️ (red-pink)")
print("  ✓ All eyes 15% taller overall")

eyes.stop()
