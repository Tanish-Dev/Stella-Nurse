"""
Quick Reference: Advanced Eye Animation Features
================================================

🎯 QUICK START
--------------
from eye_controller import EyeController

eyes = EyeController(fps=60)
eyes.enable_micro_movements(True)   # Subtle wobble (DEFAULT: ON)
eyes.enable_breathing(True)          # Gentle pulsing (DEFAULT: OFF)
eyes.happy()


✨ FEATURE TOGGLES
------------------

# Micro-Movements (Organic wobble)
eyes.enable_micro_movements(True)    # More lifelike
eyes.enable_micro_movements(False)   # More static

# Breathing Effect (Scale pulsing)
eyes.enable_breathing(True)          # Gentle breathing
eyes.enable_breathing(False)         # No breathing

# Movement Speed
eyes.set_movement_speed(0.4)         # Slow, smooth
eyes.set_movement_speed(0.75)        # Normal (default)
eyes.set_movement_speed(0.95)        # Fast, snappy


🎬 EMOTION SEQUENCES
--------------------

# Single emotion
eyes.happy()
time.sleep(2)

# Complex sequence with timing
eyes.express_sequence(
    ["curious", "thinking", "happy"],  # Emotions
    [1.0, 2.5, 2.0]                    # Durations (seconds)
)

# Reaction pattern
eyes.express_sequence(
    ["surprised", "curious", "excited"],
    [0.5, 1.5, 2.0]
)


⚡ MOVEMENT EXAMPLES
--------------------

# Slow contemplative
eyes.set_movement_speed(0.4)
eyes.thinking()

# Normal conversational
eyes.set_movement_speed(0.75)
eyes.listening()

# Fast reactive
eyes.set_movement_speed(0.95)
eyes.alert()


🌟 ALL FEATURES COMBINED
-------------------------

# Maximum fluidity setup
eyes = EyeController(fps=60)
eyes.enable_micro_movements(True)
eyes.enable_breathing(True)
eyes.set_movement_speed(0.75)

# Run complex sequence
eyes.express_sequence(
    ["idle", "curious", "thinking", "happy", "love"],
    [2.0, 1.5, 3.0, 2.0, 3.0]
)


🎨 EMOTION REFERENCE
--------------------

Basic:
  eyes.idle()        # Resting with gentle wander
  eyes.happy()       # Wide, thin, happy
  eyes.sad()         # Droopy, downward
  eyes.angry()       # Narrow, tilted

Reactive:
  eyes.surprised()   # Very wide open
  eyes.alert()       # Focused, intense (orange)
  eyes.excited()     # Bouncy, energetic

Cognitive:
  eyes.curious()     # Inquisitive tilt
  eyes.thinking()    # Looking up-side
  eyes.listening()   # Attentive, focused up
  eyes.focused()     # Alert, narrowed

Social:
  eyes.love()        # Heart-shaped (red-pink)
  eyes.concerned()   # Worried, wobbling
  eyes.speaking()    # Gentle, normal
  eyes.sleepy()      # Droopy, slow


🔧 ADVANCED PARAMETERS
----------------------

# These work automatically but can be tuned in eyes.py:

Overshoot:
  self.overshoot_amount = 0.15      # Bounce past target (0.0-0.3)

Secondary Motion:
  spring_stiffness = 0.15           # Follow-through responsiveness
  damping = 0.82                    # Drag amount

Micro-Movements:
  amplitude = 0.3 pixels            # Wobble intensity
  
Breathing:
  period = 1.5 seconds              # Breath cycle time
  amplitude = 3% scale              # Size variation


📊 TECHNICAL SPECS
------------------

Frame Rate: 60 FPS (smooth as butter)
Motion Layers: 4 (primary + secondary + micro + breathing)
Easing: Physics-based spring with overshoot
Blinking: Cozmo-style (2-6s random, 20% double-blink)
Colors: Mostly blue (except alert=orange, angry=red, love=pink)


🎯 WHEN TO USE WHAT
--------------------

Idle/Waiting:
  eyes.enable_micro_movements(True)
  eyes.enable_breathing(True)
  eyes.idle()

Active Conversation:
  eyes.enable_breathing(False)
  eyes.listening()  # When user speaks
  eyes.speaking()   # When robot speaks

Fast Reactions:
  eyes.set_movement_speed(0.95)
  eyes.surprised()

Emotional Journey:
  eyes.express_sequence(
      ["idle", "curious", "thinking", "happy"],
      [1.0, 1.5, 2.5, 2.0]
  )


💡 PRO TIPS
-----------

1. 60 FPS is crucial - don't lower it
2. Micro-movements make idle feel alive
3. Use breathing during long idle periods only
4. Fast speed (0.9+) for surprises and alerts
5. Slow speed (0.4-0.6) for sleepy/sad
6. Chain emotions to tell stories
7. Let emotions breathe - don't switch too fast


🐛 COMMON ISSUES
----------------

Too jerky?
  → eyes.set_movement_speed(0.5)

Too much wobble?
  → eyes.enable_micro_movements(False)

Breathing too obvious?
  → Keep it disabled for active emotions
  → Only use during idle/thinking

Want more bounce?
  → Edit eyes.py: self.overshoot_amount = 0.25


🚀 LIVE DEMO
------------

Run this to see all features:
  cd display/
  python3 test_fluid_features.py


📚 FULL DOCS
------------

See ADVANCED_ANIMATION.md for complete technical details
"""

if __name__ == "__main__":
    print(__doc__)
