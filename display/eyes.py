import time
import threading
import random
import math
from PIL import Image, ImageDraw

class SpringScalar:
    """
    Spring physics solver for a single scalar value.
    Simulates a damped harmonic oscillator for organic movement.
    """
    def __init__(self, value, stiffness=120.0, damping=14.0, mass=1.0):
        self.value = value
        self.target = value
        self.velocity = 0.0
        self.stiffness = stiffness  # Higher = tighter/faster spring
        self.damping = damping      # Higher = less oscillation/friction
        self.mass = mass            # Higher = heavier/slower

    def update(self, dt):
        # F = -kx - cv
        force = (self.target - self.value) * self.stiffness
        force -= self.velocity * self.damping
        
        accel = force / self.mass
        self.velocity += accel * dt
        self.value += self.velocity * dt
        
        return self.value

    def set_target(self, target):
        self.target = target

    def snap_to(self, value):
        self.value = value
        self.target = value
        self.velocity = 0.0

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
        self.dt = 1.0 / fps

        # Eye geometry
        self.eye_size = eye_size
        self.eye_spacing = eye_spacing # Default spacing
        self.corner_radius = 12
        
        self.center_y = height // 2
        # Base positions (will be dynamic based on state potentially)
        self.left_eye_x_base = (width // 2) - eye_spacing // 2
        self.right_eye_x_base = (width // 2) + eye_spacing // 2

        # ================= PHYSICS ENGINE (SPRINGS) ================= #
        # Stiffness 120, Damping 12 is a good "snappy but bouncy" feel
        spring_config = {'stiffness': 180.0, 'damping': 12.0, 'mass': 1.0}
        smooth_config = {'stiffness': 100.0, 'damping': 10.0, 'mass': 1.2}
        
        # Position
        self.spring_x = SpringScalar(0.0, **spring_config)
        self.spring_y = SpringScalar(0.0, **spring_config)
        
        # Scale (Width/Height)
        self.spring_width = SpringScalar(1.0, **spring_config)
        self.spring_height = SpringScalar(1.0, **spring_config)
        
        # Rotation
        self.spring_angle = SpringScalar(0.0, **smooth_config)
        
        # Eyelids (0.0 = open, 1.0 = fully closed)
        self.spring_upper_lid = SpringScalar(0.0, **spring_config)
        self.spring_lower_lid = SpringScalar(0.0, **spring_config)
        
        # Color (RGB)
        self.current_color = [0, 220, 255]
        self.target_color = [0, 220, 255]
        
        self.target_shape = "rect" # rect, heart, etc.
        self.current_shape = "rect"

        # ================= ANIMATION PARAMS ================= #
        self.micro_movement_enabled = True
        self.breathing_enabled = True
        self.breathing_phase = 0.0
        
        self.noise_seed = random.random() * 1000
        self.last_idle_move = time.time()

        # Blink system
        self.next_blink_time = time.time() + random.uniform(2.0, 5.0)
        self.is_blinking = False
        self.blink_duration = 0.15 # seconds
        self.blink_start_time = 0

        # State
        self.state = "idle"
        self.running = False
        self._lock = threading.Lock()

    # ================= PUBLIC API ================= #

    def set_state(self, state):
        with self._lock:
            self.state = state
            self._apply_state_targets(state)

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    # ================= LOGIC ================= #

    def _apply_state_targets(self, state):
        """Map state names to physical target parameters"""
        # Defaults
        tx, ty = 0.0, 0.0
        tw, th = 1.0, 1.0
        tang = 0.0
        tul, tll = 0.0, 0.0 # Upper lid, Lower lid
        col = (0, 220, 255) # Default Cyan
        shape = "rect"

        if state == "idle":
            col = (0, 200, 255)
            
        elif state == "happy":
            ty = -5
            tw, th = 1.1, 0.9
            tll = 0.55  # Push lower lid up significantly (cheek smile)
            col = (50, 255, 150)
            
        elif state == "sad":
            ty = 10
            tw, th = 0.95, 0.9
            tul = 0.5  # Droop upper lid
            tang = 0.15 # Stronger droop tilt outer
            col = (0, 100, 255)
            
        elif state == "angry":
            ty = -5
            th = 0.8
            tul = 0.65 # Heavy upper browser
            tang = -0.25 # Inward tilt
            col = (255, 30, 30)
            
        elif state == "surprised":
            ty = -5
            # Reduced width to prevent merging (was 1.25)
            tw, th = 1.05, 1.3 
            tul, tll = -0.1, -0.1 # Widen eyes beyond normal
            col = (200, 240, 255)
            
        elif state == "sleepy":
            ty = 10
            tul = 0.75 # Heavy drooping
            th = 0.8
            col = (0, 120, 180)
            
        elif state == "curious":
            ty = -5
            tw = 1.1
            tul = 0.1
            tang = 0.05
            col = (0, 210, 255)
            
        elif state == "suspicious":
            ty = 0
            th = 0.6
            tul = 0.4
            tll = 0.4
            col = (255, 200, 0)
            
        elif state == "excited":
            ty = -8
            # Reduced width slightly to be safe (was 1.2)
            tw, th = 1.1, 1.2
            tul, tll = -0.05, 0.1 
            col = (100, 255, 255)
            
        elif state == "love":
            tw, th = 1.2, 1.2
            col = (255, 50, 150)
            shape = "heart"
        
        # Apply targets
        self.spring_x.set_target(tx)
        self.spring_y.set_target(ty)
        self.spring_width.set_target(tw)
        self.spring_height.set_target(th)
        self.spring_angle.set_target(tang)
        self.spring_upper_lid.set_target(tul)
        self.spring_lower_lid.set_target(tll)
        self.target_color = list(col)
        self.target_shape = shape

    def _update_physics(self):
        dt = self.dt
        
        # Step springs
        self.spring_x.update(dt)
        self.spring_y.update(dt)
        self.spring_width.update(dt)
        self.spring_height.update(dt)
        self.spring_angle.update(dt)
        self.spring_upper_lid.update(dt)
        self.spring_lower_lid.update(dt)

        # Smooth color transition
        for i in range(3):
            self.current_color[i] += (self.target_color[i] - self.current_color[i]) * 10.0 * dt
            
        # Immediate shape switch (no transition needed usually, or looks weird morphing)
        self.current_shape = self.target_shape

    def _update_behaviors(self):
        """High level behaviors like blinking, breathing, idle movements"""
        t = time.time()
        
        # 1. Blinking (Independent of state, effectively modulates upper lid)
        if t > self.next_blink_time and not self.is_blinking:
            self.is_blinking = True
            self.blink_start_time = t
            self.blink_duration = random.uniform(0.12, 0.18)
            
        # Calc blink offset
        blink_lid_offset = 0.0
        if self.is_blinking:
            progress = (t - self.blink_start_time) / self.blink_duration
            if progress < 0.5:
                # Closing (0 to 1)
                blink_lid_offset = math.sin(progress * math.pi) * 2.5 
            else:
                # Opening (1 to 0)
                blink_lid_offset = math.sin(progress * math.pi) * 2.5
            
            if progress >= 1.0:
                self.is_blinking = False
                self.next_blink_time = t + random.uniform(1.5, 6.0)

        # 2. Idle wandering
        if self.state == "idle" and self.micro_movement_enabled:
            if t - self.last_idle_move > 2.0:
                # Pick a random point near center
                tgt_x = random.uniform(-15, 15)
                tgt_y = random.uniform(-8, 8)
                self.spring_x.set_target(tgt_x)
                self.spring_y.set_target(tgt_y)
                self.last_idle_move = t + random.uniform(0.0, 1.0) # slight random delay

        # 3. Breathing (Oscillation of size)
        breath_scale = 1.0
        if self.breathing_enabled:
            self.breathing_phase += 3.0 * self.dt # speed
            breath_scale = 1.0 + math.sin(self.breathing_phase) * 0.025
            
        # 4. Micro-movements (Jitter)
        jitter_x, jitter_y = 0, 0
        if self.micro_movement_enabled:
            # Perlin-ish noise using sum of sines
            # MUCH SLOWER AND SUBTLER
            # Reduced freq by factor of 2, amplitude by factor of 3 (from orig)
            jitter_x = (math.sin(t * 0.5 + self.noise_seed) + math.sin(t * 1.5)) * 0.4
            jitter_y = (math.cos(t * 0.7 + self.noise_seed) + math.cos(t * 1.3)) * 0.4

        return blink_lid_offset, breath_scale, jitter_x, jitter_y

    def _render(self):
        blink_offset, breath_scale, jitter_x, jitter_y = self._update_behaviors()
        self._update_physics()

        # Create main canvas (Black background)
        img = Image.new("RGB", (self.width, self.height), "black")
        
        # Resolve final render values
        val_x = self.spring_x.value + jitter_x
        val_y = self.spring_y.value + jitter_y
        val_w = self.spring_width.value * breath_scale
        val_h = self.spring_height.value * breath_scale
        val_rot = self.spring_angle.value
        
        # Eyelids (0-1 range + blink)
        val_ul = max(0.0, min(1.0, self.spring_upper_lid.value + blink_offset))
        val_ll = max(0.0, min(1.0, self.spring_lower_lid.value)) 

        col = tuple(int(c) for c in self.current_color)

        # Draw eyes
        self._draw_eye_composite(img, self.left_eye_x_base, val_x, val_y, val_w, val_h, val_rot, val_ul, val_ll, col, is_left=True, shape=self.current_shape)
        self._draw_eye_composite(img, self.right_eye_x_base, val_x, val_y, val_w, val_h, val_rot, val_ul, val_ll, col, is_left=False, shape=self.current_shape)

        return img

    def _draw_eye_composite(self, dst_img, base_x, off_x, off_y, scale_w, scale_h, rot, upper_lid, lower_lid, color, is_left, shape):
        """
        Draws an eye by rendering it upright on a scratchpad using shapes,
        applying eyelids, rotating the result, and pasting it onto the destination.
        This preserves valid rounded corners even when rotating.
        """
        
        # 1. Perspective
        perspective = (off_x / 50.0) 
        if is_left:
            scale_local = 1.0 - (perspective * 0.3)
        else:
            scale_local = 1.0 + (perspective * 0.3)
            
        w = self.eye_size * scale_w * scale_local
        h = self.eye_size * scale_h * 1.2 # Base height factor
        
        # Ensure minimums
        w = max(4, w)
        h = max(4, h)
        
        # 2. Setup scratchpad
        # Make it large enough to hold rotated version
        diagonal = math.sqrt(w*w + h*h)
        pad_size = int(diagonal + 10)
        pad_size = pad_size + (pad_size % 2) # Make even
        
        cx_pad = pad_size // 2
        cy_pad = pad_size // 2
        
        # Use RGBA for transparency
        scratch = Image.new("RGBA", (pad_size, pad_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(scratch)
        
        # 3. Draw Shape (Centered)
        x0 = cx_pad - w/2
        y0 = cy_pad - h/2
        x1 = cx_pad + w/2
        y1 = cy_pad + h/2
        
        if shape == "heart":
            self._draw_heart(draw, cx_pad, cy_pad, w, h, color)
        else:
            # Rounded Rect
            draw.rounded_rectangle([x0, y0, x1, y1], radius=self.corner_radius, fill=color)
            
        # 4. Draw Eyelids (Black rectangles over the shape)
        mask_color = (0, 0, 0, 255) # Opaque black
        
        if upper_lid > 0.01:
            lid_px = h * upper_lid
            # Draw from top of image down to lid edge
            draw.rectangle([0, 0, pad_size, y0 + lid_px], fill=mask_color)
            
        if lower_lid > 0.01:
            lid_px = h * lower_lid
            # Draw from bottom lid edge to bottom of image
            draw.rectangle([0, y1 - lid_px, pad_size, pad_size], fill=mask_color)
            
        # 5. Rotation
        # Convert rotation to degrees (PIL uses degrees, counter-clockwise)
        deg = math.degrees(rot)
        if is_left:
            # Mirror rotation logic if needed? 
            # Usually symmetric emotions mean:
            #Sad: /  \  (Left rotates + , Right rotates -)
            #Angry: \  / (Left rotates -, Right rotates +)
            # Wait, spring_angle is usually the 'tilt'. 
            # If current_angle is +0.2 (sad), we want eyes like / \
            # Left eye (is_left=True): should rotate +deg (Counter clockwise? No, Clockwise is negative in standard math but PIL?)
            # PIL rotate: positive = counter-clockwise.
            # / shape means top moves right. That is Clockwise. So Negative degrees.
            # \ shape means top moves left. That is Counter-Clockwise. So Positive degrees.
            
            # Let's standardize:
            # Sad (+tilt) -> / \
            # Angry (-tilt) -> \ /
            
            if is_left:
                final_rot = -deg 
            else:
                final_rot = deg
        else:
            if is_left:
                final_rot = deg
            else:
                final_rot = -deg
                
        # Actually, let's look at previous logic:
        # Sad (angle=0.1) -> means positive.
        # Angry (angle=-0.25) -> means negative.
        # If I want / \ for Sad:
        # Left eye / is Clockwise (-). Right eye \ is Counter-Clockwise (+).
        # So if Angle is +, Left should be -, Right should be +.
        
        if is_left:
            final_rot = -deg
        else:
            final_rot = deg

        rotated = scratch.rotate(final_rot, resample=Image.BICUBIC, expand=False)
        
        # 6. Composite onto main image
        # Calculate where the center of the pad should be on the main image
        dest_cx = base_x + off_x
        dest_cy = self.center_y + off_y
        
        dest_x = int(dest_cx - pad_size/2)
        dest_y = int(dest_cy - pad_size/2)
        
        # Paste using alpha channel of rotated image as mask
        dst_img.paste(rotated, (dest_x, dest_y), rotated)

    def _draw_heart(self, draw, cx, cy, w, h, color):
        """Draws a heart shape centered at cx, cy within bounding box w x h"""
        # Basic heart shape using two circles and a triangle
        # Or bezier. Let's use two circles and a polygon which is robust.
        
        # Adjust aspect for heart
        h = h * 1.1 
        
        # Top centers
        r = w / 4
        x_left = cx - w/4
        x_right = cx + w/4
        y_tops = cy - h/4
        
        # Circles
        draw.ellipse([x_left - r, y_tops - r, x_left + r, y_tops + r], fill=color)
        draw.ellipse([x_right - r, y_tops - r, x_right + r, y_tops + r], fill=color)
        
        # Triangle (inverted)
        # Top points are tangent to circles roughly at x_left-r and x_right+r?
        # A simple triangle:
        poly = [
            (cx - w/2, y_tops), # Top left far
            (cx + w/2, y_tops), # Top right far
            (cx, cy + h/2)      # Bottom tip
        ]
        draw.polygon(poly, fill=color)

    def _loop(self):
        while self.running:
            start_t = time.time()
            frame = self._render()
            
            if self.display_type == "adafruit":
                self.device.image(frame)
            else:
                self.device.display(frame)
                
            elapsed = time.time() - start_t
            sleep_t = max(0, self.dt - elapsed)
            time.sleep(sleep_t)
