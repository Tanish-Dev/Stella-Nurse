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
        eye_spacing=30,
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

        self.move_speed = 0.18  # slower, smoother
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
        
        # Smooth eye shape morphing (slower for smoother transitions)
        self.eye_width_scale += (self.target_width_scale - self.eye_width_scale) * 0.08
        self.eye_height_scale += (self.target_height_scale - self.eye_height_scale) * 0.08
        
        # Smooth angle transitions
        self.eye_angle += (self.target_angle - self.eye_angle) * 0.12
        
        # Smooth color transitions
        for i in range(3):
            self.current_color[i] += (self.target_color[i] - self.current_color[i]) * 0.08

    def _update_blink(self):
        now = time.time()

        # Blink every 4–7 seconds (natural)
        if now - self.last_blink > random.uniform(4.0, 7.0):
            self.blink_target = 0.05
            self.last_blink = now
            self.blink_speed = 0.6  # Fast blink down

        # Animate blink
        self.blink_value += (self.blink_target - self.blink_value) * self.blink_speed

        if self.blink_value < 0.1:
            self.blink_target = 1.0
            self.blink_speed = 0.35  # Slower blink up

    def _draw_eye(self, draw, x, y, scale_x=1.0, scale_y=1.0, angle=0.0, color=(0, 220, 255), is_left=True):
        """Draw a single eye - no pupils, just solid shapes"""
        size_x = int(self.eye_size * scale_x * self.eye_width_scale)
        size_y = int(self.eye_size * scale_y * self.eye_height_scale * self.blink_value)

        half_w = size_x // 2
        half_h = size_y // 2

        # Main eye shape
        if abs(angle) > 0.05:  # Only use polygon for significant angles
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
            # Ensure minimum radius for smooth corners
            radius = max(6, int(self.corner_radius * scale_x * min(self.eye_width_scale, 1.0)))
            radius = min(radius, half_w, half_h)  # Don't exceed eye size
            draw.rounded_rectangle(bbox, radius=radius, fill=color)

    def _render(self):
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)

        with self._lock:
            state = self.state
            if state != self.previous_state:
                self.state_transition_time = time.time()
                self.previous_state = state

        now = time.time()
        self.animation_time = now
        self.animation_phase += 0.08

        # ================= STATE LOGIC - Cozmo/EMO Style ================= #

        if state == "idle":
            # Gentle wandering with occasional micro-movements
            if now - self.last_idle_move > 2.5:
                self.target_x = random.uniform(-10, 10)
                self.target_y = random.uniform(-4, 4)
                self.last_idle_move = now
            
            self.target_width_scale = 1.0
            self.target_height_scale = 1.0
            self.target_angle = 0.0
            self.target_color = (0, 200, 255)  # Blue

        elif state == "happy":
            # Arc-shaped happy eyes like crescent smiles
            self.target_x = 0
            self.target_y = 2
            self.target_width_scale = 1.4  # Wider arcs
            self.target_height_scale = 0.25  # Very thin arcs
            self.target_angle = 0.0
            self.target_color = (50, 255, 150)  # Bright happy blue-green

        elif state == "sad":
            # Droopy eyes, looking down, very narrow
            self.target_x = 0
            self.target_y = 18
            self.target_width_scale = 0.85
            self.target_height_scale = 0.45  # Very droopy
            self.target_angle = 0.0
            self.target_color = (0, 180, 240)  # Dimmer blue

        elif state == "angry":
            # Very narrowed eyes, intense
            self.target_x = 0
            self.target_y = -6
            self.target_width_scale = 1.3
            self.target_height_scale = 0.3  # Very narrow, no pulsing
            self.target_angle = -0.2  # Angry tilt
            self.target_color = (255, 50, 50)  # Red - one of few colored

        elif state == "surprised":
            # Very wide open eyes
            self.target_x = 0
            self.target_y = -8
            self.target_width_scale = 1.4  # Much wider
            self.target_height_scale = 1.5  # Much taller
            self.target_angle = 0.0
            self.target_color = (200, 240, 255)  # Bright blue-white

        elif state == "curious":
            # Tilted, slightly wider
            self.target_x = 0
            self.target_y = -3
            self.target_width_scale = 1.15
            self.target_height_scale = 1.2
            self.target_angle = 0.0
            self.target_color = (0, 200, 255)  # Keep blue

        elif state == "thinking":
            # Eyes look up and to the side
            self.target_x = 12
            self.target_y = -8
            self.target_width_scale = 0.9
            self.target_height_scale = 0.95
            self.target_angle = 0.0
            self.target_color = (0, 180, 240)  # Dimmer blue

        elif state == "listening":
            # Focused upward, slightly wider and taller
            self.target_x = 0
            self.target_y = -18
            self.target_width_scale = 1.1
            self.target_height_scale = 1.2
            self.target_angle = 0.0
            self.target_color = (0, 220, 255)  # Bright blue

        elif state == "speaking":
            # Normal size, no movement
            self.target_x = 0
            self.target_y = 0
            self.target_width_scale = 1.0
            self.target_height_scale = 1.0
            self.target_angle = 0.0
            self.target_color = (0, 200, 255)  # Blue

        elif state == "alert":
            # Wide open, looking straight, focused
            self.target_x = 0
            self.target_y = -12
            self.target_width_scale = 1.2
            self.target_height_scale = 1.35
            self.target_angle = 0.0
            self.target_color = (255, 160, 0)  # Orange - important alert color

        elif state == "concerned":
            # Worried, drooped, narrow
            self.target_x = 0
            self.target_y = 8
            self.target_width_scale = 0.9
            self.target_height_scale = 0.7
            self.target_angle = 0.0
            self.target_color = (0, 180, 240)  # Dimmer blue

        elif state == "sleepy":
            # Very droopy and narrow
            self.target_x = 0
            self.target_y = 20
            self.target_width_scale = 0.8
            self.target_height_scale = 0.35  # Very droopy
            self.target_angle = 0.0
            self.target_color = (0, 150, 200)  # Dim blue
            # Override blink timing for sleepy
            if now - self.last_blink > 1.5:
                self.blink_target = 0.05
                self.last_blink = now

        elif state == "excited":
            # Wide eyes, very energetic
            self.target_x = 0
            self.target_y = -5
            self.target_width_scale = 1.3
            self.target_height_scale = 1.25
            self.target_angle = 0.0
            self.target_color = (100, 220, 255)  # Bright blue

        elif state == "love":
            # Soft, squinted, warm feeling
            self.target_x = 0
            self.target_y = 0
            self.target_width_scale = 1.15
            self.target_height_scale = 0.75  # Squinted with love
            self.target_angle = 0.0
            self.target_color = (255, 120, 180)  # Pink - warm emotion

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
        self._draw_eye(draw, right_x, eye_y, right_scale_x, scale_y, self.eye_angle, color, is_left=False)

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
