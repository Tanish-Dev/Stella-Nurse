import time
import threading
import random
import math
from PIL import Image, ImageDraw


class RoboEyes:
    def __init__(
        self,
        device,
        width=128,
        height=128,
        fps=60,
        eye_size=36,
        eye_spacing=60,
        display_type="adafruit",
    ):
        self.device = device
        self.display_type = display_type

        self.width = width
        self.height = height
        self.fps = fps

        # Eye geometry
        self.eye_size = eye_size
        self.eye_spacing = eye_spacing
        self.corner_radius = 12

        self.center_y = height // 2
        self.left_eye_x = (width // 2) - eye_spacing // 2
        self.right_eye_x = (width // 2) + eye_spacing // 2

        # Motion (current vs target)
        self.current_x = 0.0
        self.current_y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0

        self.move_speed = 0.28  # snappy but smooth
        self.last_idle_move = time.time()

        # Blink system
        self.blink_value = 1.0
        self.blink_target = 1.0
        self.last_blink = time.time()
        self.blink_speed = 0.45

        # Emotion-specific parameters
        self.eye_width_scale = 1.0
        self.eye_height_scale = 1.0
        self.target_width_scale = 1.0
        self.target_height_scale = 1.0
        
        self.eye_angle = 0.0  # For tilt
        self.target_angle = 0.0
        
        self.pupil_size = 0.5  # For emotions like surprise
        self.target_pupil_size = 0.5
        
        self.eye_color = (0, 220, 255)  # Cyan
        self.target_color = (0, 220, 255)
        self.current_color = [0, 220, 255]

        # Animation state
        self.animation_time = 0.0
        self.animation_phase = 0.0

        # State
        self.state = "idle"
        self.previous_state = "idle"
        self.state_transition_time = 0.0
        self.running = False

        self._lock = threading.Lock()

    # ================= PUBLIC API ================= #

    def set_state(self, state):
        with self._lock:
            self.state = state

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    # ================= INTERNAL ================= #

    def _update_motion(self):
        # Smooth easing with spring-like behavior
        self.current_x += (self.target_x - self.current_x) * self.move_speed
        self.current_y += (self.target_y - self.current_y) * self.move_speed
        
        # Smooth eye shape morphing
        self.eye_width_scale += (self.target_width_scale - self.eye_width_scale) * 0.15
        self.eye_height_scale += (self.target_height_scale - self.eye_height_scale) * 0.15
        
        # Smooth angle transitions
        self.eye_angle += (self.target_angle - self.eye_angle) * 0.2
        
        # Smooth pupil size changes
        self.pupil_size += (self.target_pupil_size - self.pupil_size) * 0.18
        
        # Smooth color transitions
        for i in range(3):
            self.current_color[i] += (self.target_color[i] - self.current_color[i]) * 0.12

    def _update_blink(self):angle=0.0, color=(0, 220, 255), is_left=True):
        """Draw a single eye with rotation and pupil support"""
        size_x = int(self.eye_size * scale_x * self.eye_width_scale)
        size_y = int(self.eye_size * scale_y * self.eye_height_scale * self.blink_value)

        half_w = size_x // 2
        half_h = size_y // 2

        # Main eye shape
        if angle != 0:
            # For angled eyes (emotions like angry), create polygon
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            # Create rotated rectangle corners
            corners = []
            for dx, dy in [(-half_w, -half_h), (half_w, -half_h), 
                          (half_w, half_h), (-half_w, half_h)]:
                rx = x + dx * cos_a - dy * sin_a
                ry = y + dx * sin_a + dy * cos_a
                corners.append((rx, ry))
            
            # Draw as polygon for rotation
            draw.polygon(corners, fill=color)
        else:
            # Standard rounded rectangle for most emotions
            bbox = [x - half_w, y - half_h, x + half_w, y + half_h]
            radius = int(self.corner_radius * scale_x)
            draw.rounded_rectangle(bbox, radius=radius, fill=color)
        
        # Draw pupil for certain emotions (like surprised, curious)
        if self.pupil_size > 0.1 and size_y > 10:
            pupil_radius = int(min(size_x, size_y) * self.pupil_size * 0.3)
            if pupil_radius > 2:
                pupil_bbox = [
                    x - pupil_radius,
                    y - pupil_radius,
                    x + pupil_radius,
                    y + pupil_radius
                ]
                draw.ellipse(pupil_bbox, fill=(0, 0, 0)size_y = int(self.eye_size * scale_y * self.blink_value)

            if state != self.previous_state:
                self.state_transition_time = time.time()
                self.previous_state = state

        now = time.time()
        self.animation_time = now
        self.animation_phase += 0.08

        # ================= STATE LOGIC - Cozmo/EMO Style ================= #

        if state == "idle":
            # Gentle wandering with occasional micro-movements
            if now - self.last_idle_move > 1.6:
                self.target_x = random.uniform(-14, 14)
                self.target_y = random.uniform(-6, 6)
                self.last_idle_move = now
            
            self.target_width_scale = 1.0
            self.target_height_scale = 1.0
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (0, 220, 255)

        elif state == "happy":
            # Wide eyes, slight bounce, bright color
            bounce = math.sin(self.animation_phase * 2) * 2
            self.target_x = 0
            self.target_y = bounce
            self.target_width_scale = 1.15
            self.target_height_scale = 0.85  # Squinted happy eyes
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (255, 200, 0)  # Warm yellow/orange

        elif state == "sad":
            # Droopy eyes, looking down
            self.target_x = 0
            self.target_y = 12
            self.target_width_scale = 0.9
            self.target_height_scale = 0.7
            self.target_angle = 0.15  # Slight droop angle
            self.target_pupil_size = 0.0
            self.target_color = (100, 150, 255)  # Cool blue

        elif state == "angry":
            # Narrowed eyes with sharp angle
            pulse = abs(math.sin(self.animation_phase * 3)) * 0.1
            self.target_x = 0
            self.target_y = -8
            self.target_width_scale = 1.2
            self.target_height_scale = 0.4 + pulse  # Narrow, pulsing
            self.target_angle = -0.25  # Angry tilt
            self.target_pupil_size = 0.0
            self.target_color = (255, 50, 50)  # Red

        elif state == "surprised":
            # Wide open eyes with visible pupils
            self.target_x = 0
            self.target_y = -5
            self.target_width_scale = 1.3
            self.target_height_scale = 1.4
            self.target_angle = 0.0
            self.target_pupil_size = 0.8  # Show pupils when surprised
            self.target_color = (255, 255, 255)  # Bright white

        elif state == "curious":
            # One eye slightly higher, pupils visible, head-tilt simulation
            tilt = math.sin(self.animation_phase) * 3
            self.target_x = tilt
            self.target_y = -5
            self.target_width_scale = 1.1
            self.target_height_scale = 1.15
            self.target_angle = 0.0
            self.target_pupil_size = 0.6
            self.target_color = (150, 255, 200)  # Curious green-cyan

        elif state == "thinking":
            # Eyes drift to side, slightly narrowed
            drift = math.sin(self.animation_phase * 0.5) * 18
            self.target_x = drift
            self.target_y = -3
            self.target_width_scale = 0.95
            self.target_height_scale = 0.9
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (200, 200, 255)  # Light purple

        elif state == "listening":
            # Focused upward, attentive
            self.target_x = 0
            self.target_y = -16
            self.target_width_scale = 1.05
            self.target_height_scale = 1.1
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (0, 255, 200)  # Bright cyan-green

        elif state == "speaking":
            # Slight bob while speaking
            bob = math.sin(self.animation_phase * 4) * 1.5
            self.target_x = 0
            self.target_y = bob
            self.target_width_scale = 1.0
            self.target_height_scale = 1.0
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (0, 220, 255)  # Standard cyan

        elif state == "alert":
            # Wide, focused, intense
            self.target_x = 0
            self.target_y = -20
            self.target_width_scale = 1.1
            self.target_height_scale = 1.25
            self.target_angle = 0.0
            self.target_pupil_size = 0.4
            self.target_color = (255, 180, 0)  # Alert orange

        elif state == "concerned":
            # Worried, slightly drooped
            wobble = math.sin(self.animation_phase * 1.5) * 2
            self.target_x = wobble
            self.target_y = 10
            self.target_width_scale = 1.0
            self.target_height_scale = 0.75
            self.target_angle = 0.08
            self.target_pupil_size = 0.0
            self.target_color = (255, 150, 100)  # Warm orange

        elif state == "sleepy":
            # Very droopy, slow blink
            self.target_x = 0
            self.target_y = 15
            self.target_width_scale = 0.85
            self.target_height_scale = 0.5
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (100, 100, 150)  # Dim purple
            # Override blink timing for sleepy
            if now - self.last_blink > 2.0:
                self.blink_target = 0.05
                self.last_blink = now

        elif state == "excited":
            # Fast movement, wide eyes, bouncy
            bounce = math.sin(self.animation_phase * 5) * 4
            wiggle = math.cos(self.animation_phase * 3) * 6
            self.target_x = wiggle
            self.target_y = bounce
            self.target_width_scale = 1.2
            self.target_height_scale = 1.15
            self.target_angle = 0.0
            self.target_pupil_size = 0.5
            self.target_color = (255, 100, 255)  # Excited magenta

        elif state == "love":
            # Heart-eyes effect (simplified as wider, warm glow)
            pulse = math.sin(self.animation_phase * 2) * 0.1 + 0.1
            self.target_x = 0
            self.target_y = 0
            self.target_width_scale = 1.1 + pulse
            self.target_height_scale = 1.1 + pulse
            self.target_angle = 0.0
            self.target_pupil_size = 0.0
            self.target_color = (255, 100, 150)  # Pink

        # ================= ANIMATION ================= #

        self._update_motion()
        self._update_blink()

        eye_y = int(self.center_y + self.current_y)
        left_x = int(self.left_eye_x + self.current_x)
        right_x = int(self.right_eye_x + self.current_x)

        # Perspective scaling (depth illusion) - Cozmo style
        direction = self.current_x / 18.0
        direction = max(-1.0, min(1.0, direction))

        left_scale_x = 1.0 - (direction * 0.25)
        right_scale_x = 1.0 + (direction * 0.25)

        left_scale_x = max(0.75, min(1.4, left_scale_x))
        right_scale_x = max(0.75, min(1.4, right_scale_x))

        scale_y = 1.0

        # ================= DRAW ================= #

        color = tuple(int(c) for c in self.current_color)
        
        self._draw_eye(draw, left_x, eye_y, left_scale_x, scale_y, self.eye_angle, color, is_left=True)
        self._draw_eye(draw, right_x, eye_y, right_scale_x, scale_y, self.eye_angle, color, is_left=False
        # Perspective scaling (depth illusion)
        direction = self.current_x / 18.0
        direction = max(-1.0, min(1.0, direction))

        left_scale_x = 1.0 - (direction * 0.25)
        right_scale_x = 1.0 + (direction * 0.25)

        left_scale_x = max(0.8, min(1.35, left_scale_x))
        right_scale_x = max(0.8, min(1.35, right_scale_x))

        # Vertical emotion scaling
        if state == "alert":
            scale_y = 1.2
        elif state == "concerned":
            scale_y = 0.75
        else:
            scale_y = 1.0

        # ================= DRAW ================= #

        self._draw_eye(draw, left_x, eye_y, left_scale_x, scale_y)
        self._draw_eye(draw, right_x, eye_y, right_scale_x, scale_y)

        return img

    # ================= DISPLAY ================= #

    def _display_frame(self, frame):
        if self.display_type == "adafruit":
            self.device.image(frame)
        else:
            self.device.display(frame)

    def _loop(self):
        frame_time = 1 / self.fps

        while self.running:
            frame = self._render()
            self._display_frame(frame)
            time.sleep(frame_time)