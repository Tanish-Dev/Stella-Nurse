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
    
    # Emotion showcase - Key emotions only with clear differences
    demos = [
        ("idle", 6, "😊 IDLE", "Gentle wandering, normal eyes"),
        ("happy", 6, "😄 HAPPY", "Arc-shaped crescent eyes (like smiling)"),
        ("sad", 6, "😢 SAD", "Very droopy and narrow"),
        ("surprised", 6, "😲 SURPRISED", "Very wide open"),
        ("thinking", 6, "💭 THINKING", "Looking up and away"),
        ("listening", 6, "👂 LISTENING", "Focused upward, attentive"),
        ("alert", 6, "⚠️ ALERT", "Wide, intense, orange glow"),
        ("sleepy", 6, "😴 SLEEPY", "Very droopy, slow blinks"),
        ("love", 6, "💕 LOVE", "Squinted warmth, pink glow"),
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
