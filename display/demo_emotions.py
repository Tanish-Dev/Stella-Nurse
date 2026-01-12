#!/usr/bin/env python3
"""
Stella Nurse - Full Emotion Demo
Showcases all eye animations with Cozmo/EMO-style fluidity
"""

import time
import sys
from display_driver import init_display
from eyes import RoboEyes


def main():
    print("=" * 70)
    print("🤖 STELLA NURSE - EMOTIONAL EYE ANIMATION SYSTEM")
    print("=" * 70)
    print("Inspired by Anki Cozmo & EMO Robot eye animations")
    print("Running at 60 FPS for ultra-smooth, expressive movements")
    print("-" * 70)
    
    try:
        disp = init_display()
        print("✅ Display initialized")
    except Exception as e:
        print(f"❌ Failed to initialize display: {e}")
        return 1
    
    # Create eye system with maximum smoothness
    eyes = RoboEyes(
        device=disp,
        fps=60,  # Cozmo-style 60fps
        eye_size=36,
        eye_spacing=60,
        display_type="adafruit"
    )
    
    print("✅ Eye system created")
    eyes.start()
    print("✅ Animation loop started\n")
    
    # Emotion showcase
    demos = [
        ("idle", 5, "😊 IDLE", "Gentle wandering gaze, natural micro-movements"),
        ("happy", 5, "😄 HAPPY", "Joyful bouncing with squinted eyes"),
        ("excited", 5, "🎉 EXCITED", "Energetic wiggling and bouncing"),
        ("love", 5, "💕 LOVE", "Warm, pulsing affectionate gaze"),
        ("surprised", 5, "😲 SURPRISED", "Wide eyes with visible pupils"),
        ("curious", 6, "🤔 CURIOUS", "Tilted gaze with pupils showing"),
        ("thinking", 6, "💭 THINKING", "Eyes drift to the side, contemplative"),
        ("listening", 5, "👂 LISTENING", "Focused upward, attentive posture"),
        ("speaking", 5, "💬 SPEAKING", "Gentle bobbing while communicating"),
        ("alert", 5, "⚠️ ALERT", "Wide, intense, focused stare"),
        ("concerned", 5, "😟 CONCERNED", "Worried wobble with slight droop"),
        ("sad", 5, "😢 SAD", "Droopy, downward gaze"),
        ("angry", 5, "😠 ANGRY", "Narrowed, pulsing intense stare"),
        ("sleepy", 6, "😴 SLEEPY", "Very droopy with slow blinking"),
    ]
    
    try:
        for emotion, duration, emoji_title, description in demos:
            print(f"\n{'=' * 70}")
            print(f"{emoji_title}")
            print(f"Description: {description}")
            print(f"Duration: {duration}s")
            print(f"{'=' * 70}")
            
            eyes.set_state(emotion)
            
            # Show countdown
            for i in range(duration, 0, -1):
                print(f"⏱️  {i}s remaining...", end='\r')
                time.sleep(1)
            print(" " * 40, end='\r')  # Clear countdown
        
        print("\n\n" + "=" * 70)
        print("✅ DEMO COMPLETE!")
        print("=" * 70)
        print("\nReturning to idle state...")
        eyes.set_state("idle")
        time.sleep(3)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user (Ctrl+C)")
    
    finally:
        print("\n👋 Shutting down eye animation system...")
        eyes.stop()
        time.sleep(0.5)
        print("✅ Shutdown complete\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
