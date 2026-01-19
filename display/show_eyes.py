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
    
    # Initialize Sound
    robot_sound = None
    try:
        import pygame
        pygame.mixer.init()
        # Path to new robot noise sound
        sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "robot-noises-70217.mp3")
        if os.path.exists(sound_path):
            robot_sound = pygame.mixer.Sound(sound_path)
            print(f"🔊 Sound initialized: {sound_path}")
        else:
            print(f"⚠️ Sound file not found at: {sound_path}")
    except ImportError:
        print("⚠️ Pygame not installed. Sound will be disabled. (pip install pygame)")
    except Exception as e:
        print(f"⚠️ Error initializing sound: {e}")

    def play_noise(prob=1.0):
        """Play robot noise with random volume and probability."""
        if robot_sound and random.random() < prob:
            # Random volume for natural variation
            vol = random.uniform(0.1, 0.4)
            robot_sound.set_volume(vol)
            robot_sound.play()

    def sleep_with_noise(duration, noise_prob_per_sec=0.1):
        """Sleeps for duration, checking for random noise triggers every second."""
        start = time.time()
        while time.time() - start < duration:
            # Calculate sleep step (max 1.0s or remaining time)
            remaining = duration - (time.time() - start)
            step = min(1.0, remaining)
            if step <= 0: break
            
            time.sleep(step)
            
            # Chance to play sound while idle
            play_noise(prob=noise_prob_per_sec)

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
            
            # Transition to idle
            play_noise(prob=0.8) # Sound on state change
            eyes.set_state("idle")
            
            # Sleep with random background noises
            sleep_with_noise(idle_duration, noise_prob_per_sec=0.15)
            
            # 2. Pick a random emotion
            emotion = random.choice(emotions)
            
            # Play sound for movement
            play_noise(prob=0.8) # Sound on state change
            eyes.set_state(emotion)
            
            # 3. Hold the emotion for a bit
            # Shorter duration for emotions, e.g., 2-5 seconds
            emotion_duration = random.uniform(2.0, 5.0)
            
            # Also use smart sleep here
            sleep_with_noise(emotion_duration, noise_prob_per_sec=0.1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping Eye Show...")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'eyes' in locals():
            eyes.stop()
        if 'pygame' in locals() and pygame.mixer.get_init():
            pygame.mixer.quit()
        print("Goodbye!")

if __name__ == "__main__":
    main()
