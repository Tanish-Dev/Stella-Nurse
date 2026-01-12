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
        fps=30,
        eye_radius=22,
        eye_spacing=40,
        display_type="adafruit",  # 👈 NEW
    ):
        """
        device        -> display object
        display_type  -> "adafruit" | "luma"
        """
        self.device = device
        self.display_type = display_type

        self.width = width
        self.height = height
        self.fps = fps

        self.eye_radius = eye_radius
        self.eye_spacing = eye_spacing

        self.center_y = height // 2
        self.left_eye_x = (width // 2) - eye_spacing // 2
        self.right_eye_x = (width // 2) + eye_spacing // 2

        self.eye_offset_x = 0
        self.eye_offset_y = 0

        self.blink_amount = 1.0
        self.target_blink = 1.0

        self.state = "idle"
        self.running = False

        self._lock = threading.Lock()

    # ---------------- STATES ---------------- #

    def set_state(self, state):
        with self._lock:
            self.state = state

    def look(self, x=0, y=0):
        with self._lock:
            self.eye_offset_x = max(-10, min(10, x))
            self.eye_offset_y = max(-6, min(6, y))

    def blink(self):
        with self._lock:
            self.target_blink = 0.1

    # ---------------- DRAWING ---------------- #

    def _draw_eye(self, draw, cx, cy, r, blink):
        ry = int(r * blink)
        draw.ellipse(
            (cx - r, cy - ry, cx + r, cy + ry),
            fill="white"
        )

    def _render(self):
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)

        with self._lock:
            bx = self.eye_offset_x
            by = self.eye_offset_y
            blink = self.blink_amount
            state = self.state

        # State-based behavior
        if state == "idle":
            if random.random() < 0.02:
                self.look(random.randint(-6, 6), random.randint(-3, 3))
            if random.random() < 0.01:
                self.blink()

        elif state == "listening":
            self.look(0, -2)

        elif state == "speaking":
            blink *= 0.8

        elif state == "alert":
            blink = 1.2

        # Draw eyes
        self._draw_eye(
            draw,
            self.left_eye_x + bx,
            self.center_y + by,
            self.eye_radius,
            blink
        )

        self._draw_eye(
            draw,
            self.right_eye_x + bx,
            self.center_y + by,
            self.eye_radius,
            blink
        )

        return img

    # ---------------- DISPLAY DISPATCH ---------------- #

    def _display_frame(self, frame):
        if self.display_type == "adafruit":
            self.device.image(frame)
        else:  # luma fallback
            self.device.display(frame)

    # ---------------- LOOP ---------------- #

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        frame_time = 1 / self.fps

        while self.running:
            # Smooth blink animation
            if self.blink_amount > self.target_blink:
                self.blink_amount -= 0.15
            else:
                self.target_blink += 0.15

            self.blink_amount = max(0.1, min(1.2, self.blink_amount))

            frame = self._render()
            self._display_frame(frame)

            time.sleep(frame_time)