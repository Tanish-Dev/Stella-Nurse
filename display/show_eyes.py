#!/usr/bin/env python3
"""
Eye Show Script
Runs the robot eyes endlessly, switching between idle and various emotions.
Exits on KeyboardInterrupt (Ctrl+C).
"""
import time
import random
import sys
import os

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from display_driver import init_display
    from eyes import RoboEyes
except ImportError:
    print("Error: Could not import display_driver or eyes. Make sure you are in the correct directory.")
    sys.exit(1)

def main():
    print("🤖 Starting Eye Show... (Press Ctrl+C to exit)")
    
    try:
        disp = init_display()
        eyes = RoboEyes(device=disp, fps=60, display_type="adafruit")
        eyes.start()
        
        # List of emotions to cycle through
        # "idle" is the default state we return to.
        emotions = [
            "happy", 
            "curious", 
            "surprised", 
            "excited", 
            "love", 
            "sleepy", 
            "suspicious",
            "sad", 
            "angry"
        ]
        
        while True:
            # 1. Stay idle for a significant amount of time
            # User wants "most time" in idle.
            # Random duration between 8 and 20 seconds.
            idle_duration = random.uniform(8.0, 20.0)
            # print(f"State: IDLE ({idle_duration:.1f}s)")
            eyes.set_state("idle")
            time.sleep(idle_duration)
            
            # 2. Pick a random emotion
            emotion = random.choice(emotions)
            # print(f"State: {emotion.upper()}")
            eyes.set_state(emotion)
            
            # 3. Hold the emotion for a bit
            # Shorter duration for emotions, e.g., 2-5 seconds
            emotion_duration = random.uniform(2.0, 5.0)
            time.sleep(emotion_duration)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping Eye Show...")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'eyes' in locals():
            eyes.stop()
        print("Goodbye!")

if __name__ == "__main__":
    main()
