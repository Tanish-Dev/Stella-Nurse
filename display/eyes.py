import time
import threading
import random
import math
from PIL import Image, ImageDraw, ImageFont

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
        self.eye_spacing = eye_spacing
        self.corner_radius = 12
        
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
        self.current_color = [0, 220, 255]
        self.target_color = [0, 220, 255]

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

        # Particles (for ZZZs)
        self.particles = []
        try:
            self.font = ImageFont.truetype("arial.ttf", 24)
        except:
            self.font = ImageFont.load_default()


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
            col = (100, 255, 255)
            
        elif state == "love": # Handle heart in render separately usually, but here we prep
            tw, th = 1.1, 1.1
            col = (255, 50, 150)

        elif state == "alert":
            # Siren animation handled in render
            tw, th = 1.1, 1.1
            col = (255, 0, 0)

        elif state == "sleeping":
            ty = 10
            tul = 1.0 # Fully closed
            tll = 0.0
            col = (0, 100, 200) # Dim dormant color
        
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

    def _update_particles(self, dt):
        # Spawn Zs if sleeping
        if self.state == "sleeping":
            if random.random() < (0.8 * dt): # approx 0.8 per second
                self.particles.append({
                    'x': random.uniform(self.width * 0.2, self.width * 0.8),
                    'y': self.height - 20,
                    'vx': random.uniform(-5, 5),
                    'vy': random.uniform(-15, -25),
                    'life': 1.0,
                    'text': "Z" if random.random() > 0.3 else "z"
                })

        # Update particles
        alive = []
        for p in self.particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['life'] -= 0.4 * dt # Fade out
            
            # Wiggle
            p['x'] += math.sin(time.time() * 5 + p['y']) * 10 * dt
            
            if p['life'] > 0:
                alive.append(p)
        self.particles = alive


    def _render(self):
        blink_offset, breath_scale, jitter_x, jitter_y = self._update_behaviors()
        self._update_physics()

        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)
        
        # Resolve final render values
        val_x = self.spring_x.value + jitter_x
        val_y = self.spring_y.value + jitter_y
        val_w = self.spring_width.value * breath_scale
        val_h = self.spring_height.value * breath_scale
        val_rot = self.spring_angle.value
        
        # Eyelids (0-1 range + blink)
        val_ul = max(0.0, min(1.0, self.spring_upper_lid.value + blink_offset))
        val_ll = max(0.0, min(1.0, self.spring_lower_lid.value)) # Lower lid doesn't blink usually

        # Update particles
        self._update_particles(self.dt)

        # Default color from physics
        col = tuple(int(c) for c in self.current_color)

        # Alert siren effect override
        if self.state == "alert":
            # Oscillate Red/Blue
            siren_phase = (time.time() * 8) % 2.0 # Fast flash
            if siren_phase < 1.0:
                 col = (255, 0, 0)
            else:
                 col = (0, 0, 255)

        # Draw eyes
        self._draw_eye(img, self.left_eye_x_base, val_x, val_y, val_w, val_h, val_rot, val_ul, val_ll, col, is_left=True)
        self._draw_eye(img, self.right_eye_x_base, val_x, val_y, val_w, val_h, val_rot, val_ul, val_ll, col, is_left=False)

        # Draw particles
        for p in self.particles:
             alpha = int(255 * p['life'])
             # Simple simulated text drawing if we can't do transparent text easily on RGB
             # We can't draw RGBA text on RGB image directly with alpha blending using 'draw.text' easily in old PIL?
             # actually we can just draw white.
             draw.text((p['x'], p['y']), p['text'], font=self.font, fill=(200, 200, 255))

        return img

    def _draw_eye(self, img, base_x, off_x, off_y, scale_w, scale_h, rot, upper_lid, lower_lid, color, is_left):
        # Calculate depth perspective
        perspective = (off_x / 50.0) 
        if is_left:
            scale_local = 1.0 - (perspective * 0.3)
        else:
            scale_local = 1.0 + (perspective * 0.3)
            
        # Final geometry
        w = self.eye_size * scale_w * scale_local
        h = self.eye_size * scale_h * 1.2
        
        # Center position on main image
        cx = base_x + off_x
        cy = self.center_y + off_y
        
        # We render the eye into a temporary RGBA image to handle rotation + rounded corners cleanly
        # Size must accommodate the rotated eye
        diag = int(math.ceil(math.sqrt(w*w + h*h))) + 6
        s_size = diag + (diag % 2) # Make even
        
        scratch = Image.new("RGBA", (s_size, s_size), (0,0,0,0))
        s_draw = ImageDraw.Draw(scratch)
        
        # Center of scratch
        sc = s_size / 2.0
        
        # Bounding box of eye in scratch
        x0 = sc - w/2
        y0 = sc - h/2
        x1 = sc + w/2
        y1 = sc + h/2
        
        # Draw base rounded rect
        s_draw.rounded_rectangle([x0, y0, x1, y1], radius=self.corner_radius, fill=color)
        
        # Eyelids (Draw black/transparent to mask)
        # Using 'composite' mode or just drawing black (since background is black)
        # We'll draw Clear (0,0,0,0) or Black? 
        # Since we paste this onto a black background, Transparent is better IF we want to see background stars etc.
        # But for now, drawing Clear is tricky with standard draw. 
        # Let's draw Clear using erase mode? PIL draw doesn't support 'erase' easily.
        # Better: Draw Black. The background is black.
        lid_color = (0, 0, 0, 0) # Transparent? No, that won't overwrite the eye color.
        # We need to erase.
        # Use 'fill=(0,0,0,0)' and mode? No.
        # We can just draw Black (0,0,0,255) effectively masking it if the final bg is black.
        # Since line 275 is Image.new("RGB", ..., "black"), drawing black on top is perfect.
        lid_fill = (0, 0, 0, 255)

        if upper_lid > 0.01:
            lid_h = h * upper_lid
            # Top down
            s_draw.rectangle([0, 0, s_size, y0 + lid_h], fill=lid_fill)
            
        if lower_lid > 0.01:
            lid_h = h * lower_lid
            # Bottom up
            s_draw.rectangle([0, y1 - lid_h, s_size, s_size], fill=lid_fill)

        # Rotate
        # PIL rotate is counter-clockwise (degrees)
        # self.spring_angle is usually radians (math functions use radians)
        # Check usage: math.cos(rot) in old code implies radians.
        # math.degrees converts radians to degrees.
        # Negative sign might be needed depending on coordinate system.
        # Usual screen coords: Y down.
        # Clockwise rotation in screen coords (Y down) corresponds to negative angle in standard math (Y up)? 
        # Let's stick to math.degrees(rot) and see. If it rotates wrong way, we flip.
        # Since the old code used: cx + px*c - py*s (standard rotation matrix),
        # PIL rotate direction matches standard math positive angle (CCW on standard plane).
        # But screen Y is down, so CCW visually looks CW?? 
        # Let's just use -math.degrees(rot) as a guess or math.degrees(rot).
        # Actually, let's look at old code:
        # px*c - py*s for X.
        # rotation matrix [[c, -s], [s, c]] corresponds to CCW rotation.
        # old code had 'tang = -0.25' for "inward tilt" (angry).
        # If left eye (base < center), inward tilt means top goes right? No, top goes in (right).
        # -0.25 rad is ~ -14 deg.
        # If we want consistent behavior, we use standard mapping.
        rotated = scratch.rotate(math.degrees(rot), resample=Image.BICUBIC)
        
        # Paste onto main image
        # Offset to center
        px = int(cx - s_size/2)
        py = int(cy - s_size/2)
        
        # Paste using itself as mask to handle transparency
        img.paste(rotated, (px, py), rotated)


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
