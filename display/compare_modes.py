"""
Side-by-Side Comparison: Basic vs Ultra-Fluid Animation
Shows the dramatic difference the advanced features make
"""
import time
from eye_controller import EyeController

def test_basic_mode():
    """Test with all advanced features disabled"""
    print("\n" + "="*60)
    print("🔴 BASIC MODE (Like old system)")
    print("="*60)
    print("Features: Linear movement only")
    print("Watch: Robotic, predictable motion")
    print()
    
    eyes = EyeController(fps=60)
    eyes.enable_micro_movements(False)
    eyes.enable_breathing(False)
    
    print("→ Moving through emotions...")
    emotions = ["idle", "happy", "curious", "thinking", "surprised"]
    for emotion in emotions:
        print(f"  {emotion}")
        eyes.set_state(emotion)
        time.sleep(2)
    
    print("\n💭 Notice: Movement feels direct but robotic")
    time.sleep(1)
    eyes.stop()

def test_ultra_fluid_mode():
    """Test with all advanced features enabled"""
    print("\n" + "="*60)
    print("🟢 ULTRA-FLUID MODE (New system)")
    print("="*60)
    print("Features: Overshoot + Follow-through + Micro + Breathing")
    print("Watch: Organic, lifelike motion")
    print()
    
    eyes = EyeController(fps=60)
    eyes.enable_micro_movements(True)
    eyes.enable_breathing(True)
    
    print("→ Moving through same emotions...")
    emotions = ["idle", "happy", "curious", "thinking", "surprised"]
    for emotion in emotions:
        print(f"  {emotion} ✨")
        eyes.set_state(emotion)
        time.sleep(2)
    
    print("\n✨ Notice: Movement has life, bounce, subtle wobble")
    time.sleep(1)
    eyes.stop()

def test_overshoot():
    """Demonstrate overshoot effect specifically"""
    print("\n" + "="*60)
    print("🎯 OVERSHOOT DEMONSTRATION")
    print("="*60)
    
    eyes = EyeController(fps=60)
    eyes.enable_micro_movements(False)
    eyes.enable_breathing(False)
    
    print("\nWatch the eyes carefully as they move.")
    print("Notice how they bounce slightly past the target,")
    print("then settle back - just like real eye muscles!\n")
    
    # Fast movements to show overshoot clearly
    print("→ Quick eye darts (left-right-center)")
    eyes.thinking()   # Look left-up
    time.sleep(1.5)
    eyes.listening()  # Look up
    time.sleep(1.5)
    eyes.curious()    # Look right
    time.sleep(1.5)
    eyes.idle()       # Center
    time.sleep(1.5)
    
    print("\n💡 That subtle bounce is the overshoot effect!")
    eyes.stop()

def test_micro_movements():
    """Show micro-movements in isolation"""
    print("\n" + "="*60)
    print("✨ MICRO-MOVEMENTS DEMONSTRATION")
    print("="*60)
    
    eyes = EyeController(fps=60)
    eyes.enable_breathing(False)
    
    print("\n🔴 First: NO micro-movements (static)")
    eyes.enable_micro_movements(False)
    eyes.idle()
    print("Watch: Eyes are perfectly still (feels robotic)")
    time.sleep(5)
    
    print("\n🟢 Now: WITH micro-movements (dynamic)")
    eyes.enable_micro_movements(True)
    print("Watch: Subtle organic wobble (feels alive)")
    time.sleep(5)
    
    print("\n✨ Even small wobble makes huge difference!")
    eyes.stop()

def test_breathing():
    """Show breathing effect"""
    print("\n" + "="*60)
    print("🫁 BREATHING DEMONSTRATION")
    print("="*60)
    
    eyes = EyeController(fps=60)
    eyes.enable_micro_movements(True)
    
    print("\n🔴 First: NO breathing")
    eyes.enable_breathing(False)
    eyes.idle()
    print("Watch: Size stays constant")
    time.sleep(4)
    
    print("\n🟢 Now: WITH breathing")
    eyes.enable_breathing(True)
    print("Watch: Gentle size pulsing (like gentle breaths)")
    time.sleep(6)
    
    print("\n✨ Subtle but adds life during idle!")
    eyes.stop()

def test_sequence():
    """Show emotion sequence"""
    print("\n" + "="*60)
    print("🎭 EMOTION SEQUENCE DEMONSTRATION")
    print("="*60)
    
    eyes = EyeController(fps=60)
    eyes.enable_micro_movements(True)
    eyes.enable_breathing(False)
    
    print("\nPlaying complex emotional journey:")
    print("  Idle → Notice something → Curious → Process → Joy")
    print()
    
    eyes.express_sequence(
        ["idle", "surprised", "curious", "thinking", "happy"],
        [2.0, 0.8, 1.5, 2.5, 3.0]
    )
    
    emotions_text = [
        ("idle", "😌 Resting peacefully"),
        ("surprised", "😮 Wait, what's that?"),
        ("curious", "🤔 Interesting..."),
        ("thinking", "💭 Let me process this..."),
        ("happy", "😊 I understand now!")
    ]
    
    for i, (emotion, description) in enumerate(emotions_text):
        print(f"  {i+1}. {description}")
        if i == 0:
            time.sleep(2.0)
        elif i == 1:
            time.sleep(0.8)
        elif i == 2:
            time.sleep(1.5)
        elif i == 3:
            time.sleep(2.5)
        else:
            time.sleep(3.0)
    
    print("\n✨ Sequences tell stories!")
    eyes.stop()

def main():
    print("\n" + "🎬"*30)
    print("ULTRA-FLUID ANIMATION COMPARISON")
    print("🎬"*30)
    print("\nThis demo shows the difference between basic and")
    print("ultra-fluid animation using Cozmo/EMO techniques.")
    print()
    
    while True:
        print("\n" + "="*60)
        print("SELECT TEST:")
        print("="*60)
        print("1. Side-by-side: Basic vs Ultra-Fluid")
        print("2. Overshoot effect demonstration")
        print("3. Micro-movements comparison")
        print("4. Breathing effect demonstration")
        print("5. Emotion sequence example")
        print("6. Run ALL tests")
        print("0. Exit")
        print()
        
        choice = input("Enter choice (0-6): ").strip()
        
        if choice == "1":
            test_basic_mode()
            input("\nPress Enter to see Ultra-Fluid mode...")
            test_ultra_fluid_mode()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            test_overshoot()
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            test_micro_movements()
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            test_breathing()
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            test_sequence()
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            print("\n🎬 Running complete test suite...\n")
            test_basic_mode()
            input("\n→ Press Enter for Ultra-Fluid mode...")
            test_ultra_fluid_mode()
            input("\n→ Press Enter for Overshoot demo...")
            test_overshoot()
            input("\n→ Press Enter for Micro-movements demo...")
            test_micro_movements()
            input("\n→ Press Enter for Breathing demo...")
            test_breathing()
            input("\n→ Press Enter for Sequence demo...")
            test_sequence()
            
            print("\n" + "="*60)
            print("✅ ALL TESTS COMPLETE!")
            print("="*60)
            print("\nKey Differences:")
            print("  ✨ Micro-movements → Constant subtle life")
            print("  🎯 Overshoot → Organic bounce and settle")
            print("  🌊 Follow-through → Depth and weight")
            print("  🫁 Breathing → Gentle pulsing during idle")
            print("  🎭 Sequences → Complex emotional stories")
            print("\nResult: Next-level Cozmo/EMO fluidity! 🚀")
            input("\nPress Enter to continue...")
            
        elif choice == "0":
            print("\n👋 Thanks for testing the ultra-fluid system!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
