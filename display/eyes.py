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

    def _draw_idle_eye(self, draw, x, y, size=36, radius=12, color=(0, 220, 255)):
        half = size // 2
        bbox = [
            x - half,
            y - half,
            x + half,
            y + half
        ]
        draw.rounded_rectangle(
            bbox,
            radius=radius,
            fill=color
        )

    def _render(self):
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)

        with self._lock:
            bx = self.eye_offset_x
            by = self.eye_offset_y
            state = self.state

        # ---------------- IDLE ---------------- #
        if state == "idle":
            if random.random() < 0.02:
                self.look(random.randint(-6, 6), random.randint(-3, 3))

            eye_y = self.center_y + by
            left_x = self.left_eye_x + bx
            right_x = self.right_eye_x + bx

            self._draw_idle_eye(draw, left_x, eye_y)
            self._draw_idle_eye(draw, right_x, eye_y)

        # ---------------- LISTENING (placeholder) ---------------- #
        elif state == "listening":
            eye_y = self.center_y - 4
            self._draw_idle_eye(draw, self.left_eye_x, eye_y)
            self._draw_idle_eye(draw, self.right_eye_x, eye_y)

        # ---------------- SPEAKING (placeholder) ---------------- #
        elif state == "speaking":
            self._draw_idle_eye(draw, self.left_eye_x, self.center_y)
            self._draw_idle_eye(draw, self.right_eye_x, self.center_y)

        # ---------------- ALERT (placeholder) ---------------- #
        elif state == "alert":
            self._draw_idle_eye(draw, self.left_eye_x, self.center_y)
            self._draw_idle_eye(draw, self.right_eye_x, self.center_y)

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