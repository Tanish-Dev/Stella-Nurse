# 🤖 Stella Nurse - Expressive Eye Animation System

Ultra-smooth, expressive robot eyes inspired by **Anki Cozmo** and **EMO Robot**, optimized for SPI displays running at 60 FPS.

## ✨ Features

- **14 Distinct Emotions** with unique animations
- **60 FPS Smooth Animation** for fluid, lifelike movement
- **Cozmo-Style Eye Behaviors** including:
  - Natural blinking (every 4-7 seconds)
  - Smooth easing and spring physics
  - Perspective scaling for depth illusion
  - Pupil dilation for certain emotions
  - Dynamic color changes per emotion
  - Tilted/angled eye expressions
  - Bouncing, wobbling, and pulsing effects

## 🎭 Available Emotions

| Emotion | Visual Style | Use Case |
|---------|-------------|----------|
| **Idle** 😊 | Gentle wandering gaze | Default resting state |
| **Happy** 😄 | Bouncing, squinted eyes | Success, positive feedback |
| **Sad** 😢 | Droopy, downward look | Failure, disappointment |
| **Angry** 😠 | Narrow, intense stare | Error, frustration |
| **Surprised** 😲 | Wide eyes with pupils | Unexpected events |
| **Curious** 🤔 | Tilted gaze with pupils | Exploring, questioning |
| **Thinking** 💭 | Eyes drift sideways | Processing, computing |
| **Listening** 👂 | Focused upward | Receiving voice input |
| **Speaking** 💬 | Gentle bobbing | Giving responses |
| **Alert** ⚠️ | Wide, focused stare | Important notifications |
| **Concerned** 😟 | Worried wobble | Warnings, issues |
| **Sleepy** 😴 | Very droopy, slow blinks | Low power, standby |
| **Excited** 🎉 | Energetic wiggling | High engagement |
| **Love** 💕 | Warm, pulsing gaze | Affection, care |

## 🚀 Quick Start

### Basic Usage

```python
from display.eye_controller import EyeController

# Initialize (starts automatically)
eyes = EyeController()

# Change emotions
eyes.happy()
eyes.thinking()
eyes.speaking()

# Cleanup
eyes.stop()
```

### Advanced Usage

```python
from display.eyes import RoboEyes
from display.display_driver import init_display

disp = init_display()
eyes = RoboEyes(
    device=disp,
    fps=60,           # Frame rate (30-60 recommended)
    eye_size=36,      # Eye diameter in pixels
    eye_spacing=60,   # Distance between eyes
    display_type="adafruit"
)

eyes.start()
eyes.set_state("excited")
```

## 🎬 Running Demos

### Full Emotion Showcase
```bash
cd display
python3 demo_emotions.py
```

### Quick Test
```bash
python3 test_eyes.py
```

## 🔧 Integration Examples

### With Voice Assistant
```python
from display.eye_controller import EyeController
from voice.elevenlabs import speak

eyes = EyeController()

# Listening for wake word
eyes.listening()

# User is speaking
eyes.thinking()

# Robot responds
eyes.speaking()
speak("Hello! How can I help you?")

# Return to idle
eyes.idle()
```

### With Emotion Detection
```python
eyes = EyeController()

# Map detected emotions
emotion_map = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "concerned",
    "surprise": "surprised"
}

detected = detect_emotion(user_face)
eyes.set_emotion(emotion_map[detected])
```

### With Health Monitoring
```python
eyes = EyeController()

heart_rate = get_heart_rate()

if heart_rate > 100:
    eyes.concerned()
elif heart_rate < 60:
    eyes.sleepy()
else:
    eyes.happy()
```

## ⚙️ Technical Details

### Animation System
- **Easing Functions**: Smooth exponential easing for all movements
- **Blink System**: Natural timing with fast-down, slow-up animation
- **Color Transitions**: Smooth RGB interpolation between states
- **Perspective Scaling**: Eyes scale based on gaze direction for 3D effect
- **Shape Morphing**: Width, height, and angle smoothly transition

### Performance
- Optimized for **ST7735 SPI displays** (128x128)
- Runs at **60 FPS** on Raspberry Pi
- Low CPU usage with threaded rendering
- Thread-safe state management

### Customization

```python
eyes = RoboEyes(
    device=disp,
    width=128,           # Display width
    height=128,          # Display height
    fps=60,              # Target frame rate
    eye_size=36,         # Base eye diameter
    eye_spacing=60,      # Distance between eyes
    display_type="adafruit"
)

# Adjust after creation
eyes.move_speed = 0.35      # How fast eyes move (0.1-0.5)
eyes.corner_radius = 15     # Eye corner roundness
```

## 🎨 Animation Characteristics

### Cozmo/EMO-Inspired Features
1. **Micro-movements**: Subtle idle animations prevent static appearance
2. **Overshoot**: Slight spring-like bounce on direction changes
3. **Anticipation**: Eyes "prepare" for movement with subtle pre-animation
4. **Squash & Stretch**: Eyes deform during rapid movements
5. **Secondary Motion**: Pupils and angles add extra expressiveness
6. **Timing Variation**: Each emotion has unique animation speed

## 📁 File Structure

```
display/
├── eyes.py              # Core animation engine
├── eye_controller.py    # High-level API
├── display_driver.py    # SPI display initialization
├── test_eyes.py         # Basic test script
└── demo_emotions.py     # Full emotion showcase
```

## 🐛 Troubleshooting

**Eyes not animating smoothly?**
- Reduce FPS from 60 to 30
- Check SPI bus speed settings
- Ensure no other processes are using CPU

**Colors look wrong?**
- Check `bgr=False` in display_driver.py
- Verify x_offset and y_offset settings

**Eyes feel laggy?**
- Increase `move_speed` parameter (default 0.28)
- Check thread priority

## 📝 License

Part of the Stella Nurse project.

## 🙏 Acknowledgments

Inspired by:
- **Anki Cozmo** - Expressive eye animation pioneer
- **Living.ai EMO** - Modern emotional robotics
- **Pixar Animation Principles** - 12 principles of animation
