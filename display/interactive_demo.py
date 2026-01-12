#!/usr/bin/env python3
"""
Stella Nurse - Interactive Emotion Selector
Control eye emotions in real-time from keyboard
"""

import sys
import time
import threading
from display_driver import init_display
from eyes import RoboEyes


class InteractiveDemo:
    def __init__(self):
        self.display = init_display()
        self.eyes = RoboEyes(
            device=self.display,
            fps=60,
            display_type="adafruit"
        )
        self.current_emotion = "idle"
        self.running = True
        
        self.emotions = {
            '1': ('idle', '😊 Idle'),
            '2': ('happy', '😄 Happy'),
            '3': ('sad', '😢 Sad'),
            '4': ('angry', '😠 Angry'),
            '5': ('surprised', '😲 Surprised'),
            '6': ('curious', '🤔 Curious'),
            '7': ('thinking', '💭 Thinking'),
            '8': ('listening', '👂 Listening'),
            '9': ('speaking', '💬 Speaking'),
            'a': ('alert', '⚠️ Alert'),
            'c': ('concerned', '😟 Concerned'),
            's': ('sleepy', '😴 Sleepy'),
            'e': ('excited', '🎉 Excited'),
            'l': ('love', '💕 Love'),
        }
    
    def print_menu(self):
        print("\n" + "=" * 70)
        print("🤖 STELLA NURSE - INTERACTIVE EMOTION CONTROL")
        print("=" * 70)
        print("\nPress a key to change emotion:")
        print()
        print("  Basic Emotions:")
        print("    [1] 😊 Idle       [2] 😄 Happy      [3] 😢 Sad")
        print("    [4] 😠 Angry      [5] 😲 Surprised  [6] 🤔 Curious")
        print()
        print("  Activity States:")
        print("    [7] 💭 Thinking   [8] 👂 Listening  [9] 💬 Speaking")
        print()
        print("  Special Emotions:")
        print("    [A] ⚠️ Alert      [C] 😟 Concerned  [S] 😴 Sleepy")
        print("    [E] 🎉 Excited    [L] 💕 Love")
        print()
        print("  Controls:")
        print("    [Q] Quit         [H] Help")
        print("=" * 70)
        print(f"\nCurrent emotion: {self.current_emotion.upper()}")
        print("Waiting for input... (press a key)")
    
    def run(self):
        self.eyes.start()
        self.print_menu()
        
        try:
            # Note: This uses input() for simplicity
            # For true real-time control, you'd use keyboard library
            while self.running:
                try:
                    choice = input("\n> ").lower().strip()
                    
                    if choice == 'q':
                        print("\n👋 Quitting...")
                        break
                    
                    elif choice == 'h':
                        self.print_menu()
                    
                    elif choice in self.emotions:
                        emotion, display_name = self.emotions[choice]
                        self.current_emotion = emotion
                        self.eyes.set_state(emotion)
                        print(f"✅ Switched to: {display_name}")
                    
                    else:
                        print("❌ Invalid choice. Press [H] for help.")
                
                except EOFError:
                    break
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
        
        finally:
            self.eyes.stop()
            print("✅ Eye system shut down")


def main():
    try:
        demo = InteractiveDemo()
        demo.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
