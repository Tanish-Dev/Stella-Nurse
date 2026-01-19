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
        width=160,
        height=128,
        fps=60,
        eye_size=44,
        eye_spacing=58,
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
        self.eye_spacing = eye_spacing
        self.corner_radius = 16
        
        self.center_y = height // 2
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
        self.current_color = [255, 255, 255]
        self.target_color = [255, 255, 255]

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
        col = (255, 255, 255) # Default White

        if state == "idle":
            col = (255, 255, 255)
            
        elif state == "happy":
            ty = -5
            tw, th = 1.1, 0.9
            tll = 0.55  # Push lower lid up significantly (cheek smile)
            col = (255, 255, 255)
            
        elif state == "sad":
            ty = 10
            tw, th = 0.95, 0.9
            tul = 0.5  # Droop upper lid
            tang = 0.1 # Slight droop tilt outer
            col = (0, 100, 255)
            
        elif state == "angry":
            ty = -5
            th = 0.8
            tul = 0.65 # Heavy upper browser
            tang = -0.25 # Inward tilt
            col = (255, 30, 30)
            
        elif state == "surprised":
            ty = -5
            tw, th = 1.25, 1.3
            tul, tll = -0.1, -0.1 # Widen eyes beyond normal
            col = (255, 255, 255)
            
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
            col = (255, 255, 255)
            
        elif state == "suspicious": # New state
            ty = 0
            th = 0.6
            tul = 0.4
            tll = 0.4
            col = (255, 200, 0)
            
        elif state == "excited":
            ty = -8
            tw, th = 1.2, 1.2
            tul, tll = -0.05, 0.1 # Wide but active
            col = (255, 255, 255)
            
        elif state == "love": # Handle heart in render separately usually, but here we prep
            tw, th = 1.1, 1.1
            col = (255, 50, 150)
        
        # Apply targets
        self.spring_x.set_target(tx)
        self.spring_y.set_target(ty)
        self.spring_width.set_target(tw)
        self.spring_height.set_target(th)
        self.spring_angle.set_target(tang)
        self.spring_upper_lid.set_target(tul)
        self.spring_lower_lid.set_target(tll)
        self.target_color = list(col)

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
                # Closing
                blink_lid_offset = math.sin(progress * math.pi) * 2.5 # multiplier for full closure
            else:
                # Opening
                blink_lid_offset = math.sin(progress * math.pi) * 2.5
            
            if progress >= 1.0:
                self.is_blinking = False
                self.next_blink_time = t + random.uniform(1.5, 6.0)
                blink_lid_offset = 0.0 # Force zero to prevent glitches

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
            # REDUCED AMPLITUDE: was 1.5, now 0.5
            jitter_x = (math.sin(t * 1.5 + self.noise_seed) + math.sin(t * 3.7)) * 0.5
            jitter_y = (math.cos(t * 2.1 + self.noise_seed) + math.cos(t * 5.3)) * 0.5

        return blink_lid_offset, breath_scale, jitter_x, jitter_y

    def _render(self):
        blink_offset, breath_scale, jitter_x, jitter_y = self._update_behaviors()
        self._update_physics()

        img = Image.new("RGB", (self.width, self.height), "black")
        
        # Resolve final render values
        val_x = self.spring_x.value + jitter_x
        val_y = self.spring_y.value + jitter_y
        val_w = self.spring_width.value * breath_scale
        val_h = self.spring_height.value * breath_scale
        val_rot = self.spring_angle.value
        
        # Eyelids (0-1 range + blink)
        val_ul = max(0.0, min(1.0, self.spring_upper_lid.value + blink_offset))
        val_ll = max(0.0, min(1.0, self.spring_lower_lid.value)) # Lower lid doesn't blink usually

        col = tuple(int(c) for c in self.current_color)

        # Draw eyes
        self._draw_eye(img, self.left_eye_x_base, val_x, val_y, val_w, val_h, val_rot, val_ul, val_ll, col, is_left=True)
        self._draw_eye(img, self.right_eye_x_base, val_x, val_y, val_w, val_h, val_rot, val_ul, val_ll, col, is_left=False)

        return img

    def _draw_eye(self, img, base_x, off_x, off_y, scale_w, scale_h, rot, upper_lid, lower_lid, color, is_left):
        draw = ImageDraw.Draw(img)
        
        # Calculate depth perspective
        # If looking right (off_x > 0), right eye gets bigger, left gets smaller
        # Max shift is ~20px
        
        perspective = (off_x / 50.0) # -0.4 to 0.4
        if is_left:
            scale_local = 1.0 - (perspective * 0.3)
        else:
            scale_local = 1.0 + (perspective * 0.3)
            
        # Final geometry
        w = self.eye_size * scale_w * scale_local
        h = self.eye_size * scale_h * 1.2 # Base height factor
        
        cx = base_x + off_x
        cy = self.center_y + off_y
        
        # Bounding box
        x0 = cx - w/2
        y0 = cy - h/2
        x1 = cx + w/2
        y1 = cy + h/2
        
        # 1. Simple Axis Aligned (Fast Path)
        if abs(rot) < 0.05:
            # Simple axis aligned
            # Ensure coordinates are integers for sharper rendering
            draw.rounded_rectangle([x0, y0, x1, y1], radius=self.corner_radius, fill=color)
            
            # Eyelids (Axis aligned)
            # Expand mask X by 2px each side to ensure coverage
            mask_x0 = x0 - 2
            mask_x1 = x1 + 2
            
            if upper_lid > 0.05:
                # Cover top portion - extend UPWARDS to ensure top edge is clean coverage
                lid_h = h * upper_lid
                coord_y_cut = y0 + lid_h
                # Mask from way above (y0-10) to cut line
                draw.rectangle([mask_x0, y0 - 10, mask_x1, coord_y_cut], fill="black")
                
            if lower_lid > 0.05:
                # Cover bottom portion - extend DOWNWARDS
                lid_h = h * lower_lid
                coord_y_cut = y1 - lid_h
                # Mask from cut line to way below (y1+10)
                draw.rectangle([mask_x0, coord_y_cut, mask_x1, y1 + 10], fill="black")
                
        # 2. Rotated (Quality Path with Rounding)
        else:
            # Create a larger canvas to draw the unrotated eye, then rotate it
            diag_size = int(math.hypot(w, h)) + 20
            # Ensure even size for center alignment
            if diag_size % 2 != 0: diag_size += 1
            
            # 2a. Draw unrotated eye on temp buffer
            # Use RGBA for transparency
            temp_img = Image.new("RGBA", (diag_size, diag_size), (0,0,0,0))
            temp_draw = ImageDraw.Draw(temp_img)
            
            tx = diag_size / 2
            ty = diag_size / 2
            
            # Unrotated coords centered at tx, ty
            rx0 = tx - w/2
            ry0 = ty - h/2
            rx1 = tx + w/2
            ry1 = ty + h/2
            
            # Draw rounded eye
            temp_draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=self.corner_radius, fill=color)
            
            # Draw eyelids on temp buffer (also unrotated)
            rmask_x0 = rx0 - 2
            rmask_x1 = rx1 + 2
            
            if upper_lid > 0.05:
                lid_h = h * upper_lid
                r_y_cut = ry0 + lid_h
                temp_draw.rectangle([rmask_x0, ry0 - 10, rmask_x1, r_y_cut], fill="black")
            
            if lower_lid > 0.05:
                lid_h = h * lower_lid
                r_y_cut = ry1 - lid_h
                temp_draw.rectangle([rmask_x0, r_y_cut, rmask_x1, ry1 + 10], fill="black")
            
            # 2b. Rotate
            # PIL rotate is counter-clockwise. Positive rot (radians) usually means clockwise movement on screen.
            # So we rotate by negative degrees.
            rot_deg = math.degrees(rot)
            rotated_img = temp_img.rotate(-rot_deg, resample=Image.BICUBIC)
            
            # 2c. Paste onto main image
            # Align centers
            # cx, cy is center on main img
            # tx, ty was center on temp img (which is also center of rotated_img)
            
            paste_x = int(cx - (diag_size / 2))
            paste_y = int(cy - (diag_size / 2))
            
            # Paste with alpha mask
            img.paste(rotated_img, (paste_x, paste_y), rotated_img)


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
