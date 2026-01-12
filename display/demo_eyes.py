from eye_controller import EyeController
import time
import random

def main():
    print("Initializing Fluid Eye Controller...")
    eyes = EyeController(fps=60)
    
    # Wait for init
    time.sleep(1)
    
    print("\n--- DEMO START ---\n")
    
    emotions = [
        ("idle", 3),
        ("happy", 2),
        ("excited", 2),
        ("surprised", 1.5),
        ("idle", 2),
        ("suspicious", 2),
        ("angry", 2),
        ("concerned", 2),
        ("sad", 2),
        ("sleepy", 3), # Wait for blink pattern
        ("alert", 2),
        ("curious", 2),
        ("thinking", 2),
        ("love", 3),
    ]
    
    try:
        for name, duration in emotions:
            print(f"Emotion: {name.upper()}")
            # Call the method by name if it exists, else set_state
            if hasattr(eyes, name):
                getattr(eyes, name)()
            else:
                eyes.set_emotion(name)
            
            time.sleep(duration)
            
        print("\n--- RANDOM MODE (Press Ctrl+C to stop) ---\n")
        
        while True:
            name, _ = random.choice(emotions)
            print(f"Random: {name}")
            getattr(eyes, name)()
            time.sleep(random.uniform(1.0, 4.0))
            
    except KeyboardInterrupt:
        print("\nStopping...")
        eyes.stop()

if __name__ == "__main__":
    main()
