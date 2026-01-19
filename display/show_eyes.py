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
    
    # Initialize Sounds
    robot_sounds = []
    last_sound_time = 0
    min_cooldown = 1.0  # Minimum time between sounds
    
    try:
        import pygame
        pygame.mixer.init()
        
        # Load all mp3s from assets/sounds
        sounds_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        if os.path.exists(sounds_dir):
            for filename in os.listdir(sounds_dir):
                if filename.endswith(".mp3"):
                    path = os.path.join(sounds_dir, filename)
                    try:
                        snd = pygame.mixer.Sound(path)
                        robot_sounds.append(snd)
                        print(f"🔊 Loaded: {filename}")
                    except Exception as e:
                        print(f"⚠️ Failed to load {filename}: {e}")
            
            if not robot_sounds:
                print("⚠️ No .mp3 sounds found in assets/sounds")
        else:
            print(f"⚠️ Sounds directory not found: {sounds_dir}")

    except ImportError:
        print("⚠️ Pygame not installed. Sound will be disabled. (pip install pygame)")
    except Exception as e:
        print(f"⚠️ Error initializing sounds: {e}")

    def play_noise(prob=1.0, force=False):
        """
        Play a random robot noise.
        - prob: probability to try playing
        - force: if True, ignores probability (but still respects cooldown)
        """
        nonlocal last_sound_time
        
        if not robot_sounds:
            return

        # Check random probability first
        if not force and random.random() > prob:
            return

        # Check cooldown (ensure sounds don't overlap too closely)
        # We add a slight random element to the cooldown requirements too
        current_time = time.time()
        time_since_last = current_time - last_sound_time
        
        # Required gap: 1.5 to 3.0 seconds
        required_gap = random.uniform(1.5, 3.0)
        
        if time_since_last < required_gap:
            return

        try:
            # Pick random sound
            snd = random.choice(robot_sounds)
            
            # Random volume for variation
            vol = random.uniform(0.1, 0.4)
            snd.set_volume(vol)
            snd.play()
            
            last_sound_time = current_time
        except Exception as e:
            print(f"Error playing sound: {e}")

    def sleep_with_noise(duration, noise_prob_per_sec=0.2):
        """Sleeps for duration, checking for random noise triggers."""
        start = time.time()
        while time.time() - start < duration:
            # Calculate sleep step
            remaining = duration - (time.time() - start)
            step = min(0.5, remaining) # Check more frequently (every 0.5s)
            if step <= 0: break
            
            time.sleep(step)
            
            # Chance to play sound
            # adjusted prob since we check every 0.5s instead of 1.0s
            play_noise(prob=noise_prob_per_sec * 0.5)

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
            # force=True to encourage sound on change, but play_noise handles cooldown
            play_noise(force=True) 
            eyes.set_state("idle")
            
            # Sleep with random background noises
            sleep_with_noise(idle_duration, noise_prob_per_sec=0.25)
            
            # 2. Pick a random emotion
            emotion = random.choice(emotions)
            
            # Play sound for movement
            play_noise(force=True) 
            eyes.set_state(emotion)
            
            # 3. Hold the emotion for a bit
            # Shorter duration for emotions, e.g., 2-5 seconds
            emotion_duration = random.uniform(2.0, 5.0)
            
            # Also use smart sleep here
            sleep_with_noise(emotion_duration, noise_prob_per_sec=0.15)
            
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
