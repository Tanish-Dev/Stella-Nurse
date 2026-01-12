"""
Stella Nurse - Eye Animation Controller
Easy API for controlling robot emotions from any module
"""

from eyes import RoboEyes
from display_driver import init_display


class EyeController:
    """
    High-level controller for Stella's expressive eyes.
    Use this in your main robot code for easy emotion control.
    """
    
    def __init__(self, fps=60, auto_start=True):
        """
        Initialize the eye controller.
        
        Args:
            fps: Frames per second (60 recommended for smooth Cozmo-style animation)
            auto_start: If True, starts the animation loop immediately
        """
        self.display = init_display()
        self.eyes = RoboEyes(
            device=self.display,
            fps=fps,
            display_type="adafruit"
        )
        
        if auto_start:
            self.eyes.start()
    
    # ===== Core Emotion Controls ===== #
    
    def idle(self):
        """Default resting state with gentle wandering"""
        self.eyes.set_state("idle")
    
    def happy(self):
        """Joyful, bouncing expression"""
        self.eyes.set_state("happy")
    
    def sad(self):
        """Droopy, downward-looking expression"""
        self.eyes.set_state("sad")
    
    def angry(self):
        """Intense, narrowed eyes"""
        self.eyes.set_state("angry")
    
    def surprised(self):
        """Wide-eyed shock with visible pupils"""
        self.eyes.set_state("surprised")
    
    def curious(self):
        """Inquisitive head-tilt look with pupils"""
        self.eyes.set_state("curious")
    
    def thinking(self):
        """Contemplative, eyes drifting to the side"""
        self.eyes.set_state("thinking")
    
    def listening(self):
        """Attentive, focused upward"""
        self.eyes.set_state("listening")
    
    def speaking(self):
        """Gentle bobbing while talking"""
        self.eyes.set_state("speaking")
    
    def alert(self):
        """Wide, focused, intense attention"""
        self.eyes.set_state("alert")
    
    def concerned(self):
        """Worried, wobbling expression"""
        self.eyes.set_state("concerned")
    
    def sleepy(self):
        """Drowsy, droopy with slow blinks"""
        self.eyes.set_state("sleepy")
    
    def excited(self):
        """Energetic, bouncy, wiggling"""
        self.eyes.set_state("excited")
    
    def love(self):
        """Affectionate, warm, pulsing"""
        self.eyes.set_state("love")
    
    def focused(self):
        """Alert, attentive, slightly narrowed"""
        self.eyes.set_state("focused")
    
    # ===== Utility Methods ===== #
    
    def set_emotion(self, emotion: str):
        """
        Set emotion by name.
        
        Args:
            emotion: One of: idle, happy, sad, angry, surprised, curious,
                    thinking, listening, speaking, alert, concerned, 
                    sleepy, excited, love, focused
        """
        self.eyes.set_state(emotion)
    
    def express_sequence(self, emotions: list, durations: list):
        """
        Play a sequence of emotions with timing for complex expressions.
        
        Args:
            emotions: List of emotion names
            durations: List of duration in seconds for each emotion
            
        Example:
            eyes.express_sequence(
                ["surprised", "curious", "happy"],
                [0.5, 1.0, 2.0]
            )
        """
        import threading
        
        def play():
            for emotion, duration in zip(emotions, durations):
                self.eyes.set_state(emotion)
                time.sleep(duration)
        
        threading.Thread(target=play, daemon=True).start()
    
    def enable_micro_movements(self, enable=True):
        """
        Enable/disable subtle organic micro-movements.
        
        Args:
            enable: True to add constant subtle motion (more lifelike)
        """
        self.eyes.micro_movement_enabled = enable
    
    def enable_breathing(self, enable=True):
        """
        Enable/disable subtle breathing scale effect.
        
        Args:
            enable: True to add gentle breathing animation
        """
        self.eyes.breathing_enabled = enable
    
    def set_movement_speed(self, speed: float):
        """
        Adjust eye movement speed.
        
        Args:
            speed: 0.3 (slow/smooth) to 1.0 (instant). Default 0.75
        """
        self.eyes.move_speed = max(0.1, min(1.0, speed))
    
    def stop(self):
        """Stop the animation loop"""
        self.eyes.stop()
    
    def start(self):
        """Start the animation loop"""
        if not self.eyes.running:
            self.eyes.start()


# Example usage patterns:
if __name__ == "__main__":
    import time
    
    # Simple usage
    controller = EyeController()
    
    controller.happy()
    time.sleep(3)
    
    controller.thinking()
    time.sleep(3)
    
    controller.excited()
    time.sleep(3)
    
    controller.idle()
    time.sleep(2)
    
    controller.stop()
