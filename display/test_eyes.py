import time
from display_driver import init_display
from eyes import RoboEyes

print("🤖 Stella Nurse - Fluid Eye Animation Demo (Cozmo/EMO Style)")
print("=" * 60)

disp = init_display()

# Higher FPS for ultra-smooth animations
eyes = RoboEyes(
    device=disp,
    fps=60,  # Smooth 60fps like Cozmo
    display_type="adafruit"
)

eyes.start()

# Demo all emotions with appropriate timing
emotions = [
    ("idle", 4, "😊 Idle - gentle wandering"),
    ("happy", 4, "😄 Happy - joyful bounce"),
    ("sad", 4, "😢 Sad - droopy eyes"),
    ("angry", 4, "😠 Angry - intense stare"),
    ("surprised", 4, "😲 Surprised - wide eyes"),
    ("curious", 4, "🤔 Curious - head tilt"),
    ("thinking", 5, "💭 Thinking - contemplative"),
    ("listening", 4, "👂 Listening - attentive"),
    ("speaking", 4, "💬 Speaking - animated"),
    ("alert", 4, "⚠️ Alert - focused"),
    ("concerned", 4, "😟 Concerned - worried"),
    ("sleepy", 5, "😴 Sleepy - drowsy"),
    ("excited", 4, "🎉 Excited - energetic"),
    ("love", 5, "💕 Love - affectionate"),
]

try:
    for emotion, duration, description in emotions:
        print(f"\n{description}")
        eyes.set_state(emotion)
        time.sleep(duration)
    
    print("\n\n✅ Demo complete! Returning to idle...")
    eyes.set_state("idle")
    time.sleep(2)
    
except KeyboardInterrupt:
    print("\n\n⚠️ Demo interrupted by user")

finally:
    eyes.stop()
    print("👋 Shutting down eye system...")