import time
import threading
import random
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

        # State
        self.state = "idle"
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
        # Smooth easing
        self.current_x += (self.target_x - self.current_x) * self.move_speed
        self.current_y += (self.target_y - self.current_y) * self.move_speed

    def _update_blink(self):
        now = time.time()

        # Blink every 4–7 seconds (natural)
        if now - self.last_blink > random.uniform(4.0, 7.0):
            self.blink_target = 0.05
            self.last_blink = now

        # Animate blink
        self.blink_value += (self.blink_target - self.blink_value) * 0.45

        if self.blink_value < 0.1:
            self.blink_target = 1.0

    def _draw_eye(self, draw, x, y, scale_x=1.0, scale_y=1.0, color=(0, 220, 255)):
        size_x = int(self.eye_size * scale_x)
        size_y = int(self.eye_size * scale_y * self.blink_value)

        half_w = size_x // 2
        half_h = size_y // 2

        bbox = [
            x - half_w,
            y - half_h,
            x + half_w,
            y + half_h,
        ]

        draw.rounded_rectangle(
            bbox,
            radius=int(self.corner_radius * scale_x),
            fill=color
        )

    def _render(self):
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)

        with self._lock:
            state = self.state

        now = time.time()

        # ================= STATE LOGIC ================= #

        if state == "idle":
            if now - self.last_idle_move > 1.6:
                self.target_x = random.uniform(-14, 14)
                self.target_y = random.uniform(-6, 6)
                self.last_idle_move = now

        elif state == "listening":
            self.target_x = 0
            self.target_y = -16

        elif state == "speaking":
            self.target_x = 0
            self.target_y = 0

        elif state == "alert":
            self.target_x = 0
            self.target_y = -20

        elif state == "concerned":
            self.target_x = 0
            self.target_y = 10

        # ================= ANIMATION ================= #

        self._update_motion()
        self._update_blink()

        eye_y = int(self.center_y + self.current_y)
        left_x = int(self.left_eye_x + self.current_x)
        right_x = int(self.right_eye_x + self.current_x)

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