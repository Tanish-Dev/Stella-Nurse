#!/usr/bin/env python3
"""
QUICK REFERENCE - Stella Nurse Eye Emotions
Copy-paste these examples into your code!
"""

# ============================================
# BASIC USAGE
# ============================================

from display.eye_controller import EyeController

eyes = EyeController()  # Auto-starts at 60 FPS

# Set emotions directly
eyes.idle()
eyes.happy()
eyes.sad()
eyes.thinking()

# Or use string names
eyes.set_emotion("excited")

eyes.stop()


# ============================================
# ALL 14 EMOTIONS
# ============================================

emotions = {
    "idle":       "😊 Default resting state, gentle wandering",
    "happy":      "😄 Joyful, bouncing, warm yellow",
    "sad":        "😢 Droopy, downward, cool blue",
    "angry":      "😠 Narrow, intense, pulsing red",
    "surprised":  "😲 Wide eyes with pupils, bright white",
    "curious":    "🤔 Tilted gaze with pupils, green-cyan",
    "thinking":   "💭 Eyes drift sideways, light purple",
    "listening":  "👂 Focused upward, attentive, cyan-green",
    "speaking":   "💬 Gentle bobbing, standard cyan",
    "alert":      "⚠️ Wide, intense focus, orange",
    "concerned":  "😟 Worried wobble, drooped, warm orange",
    "sleepy":     "😴 Very droopy, slow blinks, dim purple",
    "excited":    "🎉 Energetic wiggling, magenta",
    "love":       "💕 Warm pulsing glow, pink"
}


# ============================================
# INTEGRATION EXAMPLES
# ============================================

# Example 1: Voice Assistant
def voice_interaction():
    eyes.listening()      # User is speaking
    # ... listen to user ...
    
    eyes.thinking()       # Processing
    # ... process with AI ...
    
    eyes.speaking()       # Responding
    # ... speak response ...
    
    eyes.idle()          # Done


# Example 2: Health Monitoring
def check_vitals(heart_rate, temperature):
    eyes.curious()        # Checking...
    
    if heart_rate > 100:
        eyes.concerned()
    elif temperature > 38:
        eyes.alert()
    else:
        eyes.happy()


# Example 3: Emotional Responses
def respond_to_user(sentiment):
    emotion_map = {
        "positive": "happy",
        "negative": "sad",
        "neutral": "thinking",
        "question": "curious",
        "urgent": "alert"
    }
    eyes.set_emotion(emotion_map.get(sentiment, "idle"))


# Example 4: Surprise Reaction
def surprise_sequence():
    eyes.surprised()
    time.sleep(1)
    eyes.curious()
    time.sleep(1.5)
    eyes.happy()


# ============================================
# ADVANCED: Custom Parameters
# ============================================

from display.eyes import RoboEyes
from display.display_driver import init_display

disp = init_display()
eyes = RoboEyes(
    device=disp,
    fps=60,              # Frame rate (30-60)
    eye_size=36,         # Eye diameter
    eye_spacing=60,      # Distance between eyes
    width=128,
    height=128,
    display_type="adafruit"
)

# Adjust behavior at runtime
eyes.move_speed = 0.35      # Faster movement (0.1-0.5)
eyes.corner_radius = 15     # Rounder eyes

eyes.start()


# ============================================
# TESTING
# ============================================

# Test all emotions
def test_all():
    for emotion in emotions.keys():
        print(f"Testing: {emotion}")
        eyes.set_emotion(emotion)
        time.sleep(3)


# ============================================
# COMMON PATTERNS
# ============================================

# Pattern 1: Processing Loop
def processing_loop():
    eyes.thinking()
    for i in range(10):
        # Do work
        pass
    eyes.happy()

# Pattern 2: Error Handling
try:
    eyes.thinking()
    risky_operation()
    eyes.happy()
except Exception:
    eyes.sad()
    
# Pattern 3: Attention Getter
eyes.surprised()
time.sleep(0.5)
eyes.alert()

# Pattern 4: Farewell
eyes.love()
time.sleep(2)
eyes.sleepy()
