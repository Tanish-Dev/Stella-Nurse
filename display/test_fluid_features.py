"""
Test the advanced fluid animation features
Shows off: micro-movements, breathing, overshoot, follow-through
"""
import time
from eye_controller import EyeController

def main():
    print("🎬 Testing Advanced Fluid Animation Features")
    print("=" * 50)
    
    # Initialize with default settings
    eyes = EyeController(fps=60)
    
    # Test 1: Basic emotions with micro-movements (default on)
    print("\n✨ Test 1: Idle with micro-movements")
    print("Watch for subtle organic wobble...")
    eyes.idle()
    time.sleep(5)
    
    # Test 2: Disable micro-movements for comparison
    print("\n❌ Test 2: Idle WITHOUT micro-movements")
    print("Notice it's more static...")
    eyes.enable_micro_movements(False)
    time.sleep(3)
    
    # Re-enable
    print("\n✅ Re-enabling micro-movements")
    eyes.enable_micro_movements(True)
    time.sleep(2)
    
    # Test 3: Fast movements showing overshoot
    print("\n🎯 Test 3: Quick eye darts (overshoot effect)")
    print("Watch eyes bounce slightly past target...")
    eyes.curious()
    time.sleep(1)
    eyes.thinking()
    time.sleep(1)
    eyes.surprised()
    time.sleep(1)
    eyes.idle()
    time.sleep(2)
    
    # Test 4: Breathing effect
    print("\n🫁 Test 4: Breathing animation")
    print("Watch for gentle scale pulsing...")
    eyes.enable_breathing(True)
    eyes.idle()
    time.sleep(6)
    
    # Test 5: Emotion sequence
    print("\n🎭 Test 5: Complex emotion sequence")
    print("Playing: curious → surprised → excited → happy")
    eyes.express_sequence(
        ["curious", "surprised", "excited", "happy"],
        [1.5, 1.0, 1.5, 2.0]
    )
    time.sleep(6.5)
    
    # Test 6: Speed adjustments
    print("\n⚡ Test 6: Different movement speeds")
    
    print("  → Slow smooth (0.4)")
    eyes.set_movement_speed(0.4)
    eyes.sad()
    time.sleep(2)
    
    print("  → Normal (0.75)")
    eyes.set_movement_speed(0.75)
    eyes.curious()
    time.sleep(2)
    
    print("  → Very fast (0.95)")
    eyes.set_movement_speed(0.95)
    eyes.alert()
    time.sleep(1)
    eyes.excited()
    time.sleep(1)
    
    # Reset to default
    eyes.set_movement_speed(0.75)
    
    # Test 7: All features combined
    print("\n🌟 Test 7: ALL FEATURES COMBINED")
    print("Micro-movements + Breathing + Overshoot + Follow-through")
    eyes.enable_micro_movements(True)
    eyes.enable_breathing(True)
    eyes.express_sequence(
        ["idle", "happy", "love", "excited", "idle"],
        [2.0, 2.5, 2.5, 2.0, 2.0]
    )
    time.sleep(11.5)
    
    print("\n✅ Test complete!")
    print("=" * 50)
    print("\nKey Features Demonstrated:")
    print("  ✨ Micro-movements: Constant subtle organic motion")
    print("  🎯 Overshoot: Eyes bounce past target")
    print("  🌊 Follow-through: Secondary drag motion")
    print("  🫁 Breathing: Gentle scale pulsing")
    print("  🎬 Sequences: Complex multi-emotion animations")
    
    eyes.stop()

if __name__ == "__main__":
    main()
