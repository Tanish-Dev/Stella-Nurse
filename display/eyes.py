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
        eye_spacing=45,
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
        self.base_height_scale = 1.15  # Slightly taller eyes overall

        self.center_y = height // 2
        self.left_eye_x = (width // 2) - eye_spacing // 2
        self.right_eye_x = (width // 2) + eye_spacing // 2

        # Motion (current vs target)
        self.current_x = 0.0
        self.current_y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0

        self.move_speed = 0.75  # Very quick, snappy movements (Cozmo-like)
        self.last_idle_move = time.time()
        
        # Advanced animation parameters for ultra-fluid motion
        self.overshoot_amount = 0.15  # Bounce past target slightly
        self.secondary_offset_x = 0.0  # Follow-through motion
        self.secondary_offset_y = 0.0
        self.secondary_velocity_x = 0.0
        self.secondary_velocity_y = 0.0
        self.micro_movement_enabled = True  # Subtle idle wobble
        self.breathing_enabled = False  # Breathing scale effect
        self.breathing_phase = 0.0

        # Blink system - Cozmo style
        self.blink_value = 1.0
        self.blink_target = 1.0
        self.last_blink = time.time()
        self.blink_speed = 0.45
        self.next_blink_time = time.time() + random.uniform(2.0, 5.0)
        self.double_blink = False  # For occasional double blinks

        # Emotion-specific parameters
        self.eye_width_scale = 1.0
        self.eye_height_scale = 1.0
        self.target_width_scale = 1.0
        self.target_height_scale = 1.0
        
        self.width_scale_speed = 0.18  # Faster, smoother scaling
        self.height_scale_speed = 0.18  # Faster, smoother scaling
        
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
        # Advanced smooth easing with overshoot for organic movement
        diff_x = self.target_x - self.current_x
        diff_y = self.target_y - self.current_y
        
        # Apply overshoot when close to target for bounce effect
        if abs(diff_x) < 3:
            self.current_x += diff_x * self.move_speed * (1 + self.overshoot_amount)
        else:
            self.current_x += diff_x * self.move_speed
            
        if abs(diff_y) < 3:
            self.current_y += diff_y * self.move_speed * (1 + self.overshoot_amount)
        else:
            self.current_y += diff_y * self.move_speed
        
        # Secondary motion (follow-through) - Disney principle
        target_secondary_x = self.current_x * 0.2
        target_secondary_y = self.current_y * 0.2
        
        spring_stiffness = 0.15
        damping = 0.82
        
        force_x = (target_secondary_x - self.secondary_offset_x) * spring_stiffness
        force_y = (target_secondary_y - self.secondary_offset_y) * spring_stiffness
        
        self.secondary_velocity_x = (self.secondary_velocity_x + force_x) * damping
        self.secondary_velocity_y = (self.secondary_velocity_y + force_y) * damping
        
        self.secondary_offset_x += self.secondary_velocity_x
        self.secondary_offset_y += self.secondary_velocity_y
        
        # Faster smooth eye shape morphing
        self.eye_width_scale += (self.target_width_scale - self.eye_width_scale) * self.width_scale_speed
        self.eye_height_scale += (self.target_height_scale - self.eye_height_scale) * self.height_scale_speed
        
        # Smooth angle transitions
        self.eye_angle += (self.target_angle - self.eye_angle) * 0.12
        
        # Smooth color transitions
        for i in range(3):
            self.current_color[i] += (self.target_color[i] - self.current_color[i]) * 0.08

    def _add_micro_movements(self):
        """Add subtle organic micro-movements for liveliness"""
        if not self.micro_movement_enabled:
            return 0.0, 0.0
            
        t = time.time() * 0.8
        
        # Multi-frequency sine waves for natural movement
        micro_x = (math.sin(t * 1.3) * 0.4 + math.sin(t * 2.7) * 0.2) * 0.3
        micro_y = (math.cos(t * 1.1) * 0.3 + math.cos(t * 2.3) * 0.15) * 0.3
        
        return micro_x, micro_y
    
    def _update_breathing(self):
        """Add subtle breathing scale effect"""
        if not self.breathing_enabled:
            return 1.0
            
        self.breathing_phase += 0.02
        # Gentle sine wave breathing (1.5 second period)
        breath_scale = 1.0 + math.sin(self.breathing_phase) * 0.03
        return breath_scale

    def _update_blink(self):
        now = time.time()

        # Cozmo-style natural blinking with variation
        if now >= self.next_blink_time and self.blink_value > 0.95:
            # Start a blink
            self.blink_target = 0.0
            self.blink_speed = 0.85  # Very fast blink down (Cozmo-like)
            self.last_blink = now
            
            # 20% chance of double blink (Cozmo does this!)
            if random.random() < 0.2:
                self.double_blink = True
        
        # Animate blink
        self.blink_value += (self.blink_target - self.blink_value) * self.blink_speed

        # Blink finished going down
        if self.blink_value < 0.05 and self.blink_target < 0.5:
            self.blink_target = 1.0
            self.blink_speed = 0.4  # Slower blink up
        
        # Blink finished going up
        if self.blink_value > 0.95 and self.blink_target > 0.5:
            if self.double_blink:
                # Quick second blink!
                self.blink_target = 0.0
                self.blink_speed = 0.85
                self.double_blink = False
            else:
                # Schedule next blink with natural variation (2-6 seconds)
                self.next_blink_time = now + random.uniform(2.0, 6.0)

    def _draw_heart(self, draw, x, y, size, color):
        """Draw a heart shape for love emotion"""
        # Heart is made of two circles on top and a triangle on bottom
        w = size
        h = size
        
        # Draw filled heart using polygon approximation
        points = []
        # Top left curve
        for angle in range(180, 360, 10):
            px = x - w//4 + int(w//4 * math.cos(math.radians(angle)))
            py = y - h//4 + int(h//4 * math.sin(math.radians(angle)))
            points.append((px, py))
        # Top right curve  
        for angle in range(180, 360, 10):
            px = x + w//4 + int(w//4 * math.cos(math.radians(angle)))
            py = y - h//4 + int(h//4 * math.sin(math.radians(angle)))
            points.append((px, py))
        # Bottom point
        points.append((x, y + h//2))
        
        draw.polygon(points, fill=color)

    def _draw_eye(self, draw, x, y, scale_x=1.0, scale_y=1.0, angle=0.0, color=(0, 220, 255), is_left=True, is_heart=False):
        """Draw a single eye - no pupils, just solid shapes"""
        
        # Special case: draw heart for love emotion
        if is_heart:
            size = int(self.eye_size * scale_x * self.eye_width_scale)
            self._draw_heart(draw, x, y, size, color)
            return
        
        size_x = int(self.eye_size * scale_x * self.eye_width_scale)
        size_y = int(self.eye_size * scale_y * self.eye_height_scale * self.base_height_scale * self.blink_value)

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
            # Wide, thin happy eyes
            self.target_x = 0
            self.target_y = -5  # Slightly up for happy look
            self.target_width_scale = 1.3  # Wide
            self.target_height_scale = 0.4  # Thin
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

        elif state == "focused":
            # Attentive, alert, slightly narrowed
            self.target_x = 0
            self.target_y = 0
            self.target_width_scale = 0.95  # Slightly narrower
            self.target_height_scale = 1.25  # Taller, alert
            self.target_angle = 0.0
            self.target_color = (20, 200, 255)  # Sharp blue

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
            # Heart-shaped eyes!
            self.target_x = 0
            self.target_y = 0
            self.target_width_scale = 1.1
            self.target_height_scale = 1.1  # Hearts maintain proportion
            self.target_angle = 0.0
            self.target_color = (255, 80, 120)  # Red-pink for hearts

        # ================= ANIMATION ================= #

        self._update_motion()
        self._update_blink()
        
        # Add micro-movements for organic feel
        micro_x, micro_y = self._add_micro_movements()
        
        # Add breathing effect
        breath_scale = self._update_breathing()

        # Combine all movement layers (primary + secondary + micro)
        eye_y = int(self.center_y + self.current_y + self.secondary_offset_y + micro_y)
        left_x = int(self.left_eye_x + self.current_x + self.secondary_offset_x + micro_x)
        right_x = int(self.right_eye_x + self.current_x + self.secondary_offset_x + micro_x)

        # Perspective scaling (depth illusion) - Cozmo style
        direction = self.current_x / 18.0
        direction = max(-1.0, min(1.0, direction))

        left_scale_x = 1.0 - (direction * 0.25)
        right_scale_x = 1.0 + (direction * 0.25)

        left_scale_x = max(0.75, min(1.4, left_scale_x))
        right_scale_x = max(0.75, min(1.4, right_scale_x))

        # Apply breathing scale
        left_scale_x *= breath_scale
        right_scale_x *= breath_scale
        scale_y = 1.0 * breath_scale

        # ================= DRAW ================= #

        color = tuple(int(c) for c in self.current_color)
        
        # Check if we should draw hearts (love emotion)
        is_heart = (state == "love")
        
        self._draw_eye(draw, left_x, eye_y, left_scale_x, scale_y, self.eye_angle, color, is_left=True, is_heart=is_heart)
        self._draw_eye(draw, right_x, eye_y, right_scale_x, scale_y, self.eye_angle, color, is_left=False, is_heart=is_heart)

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
