import time
from display_driver import init_display
from eyes import RoboEyes

disp = init_display()

eyes = RoboEyes(
    device=disp,
    fps=30,
    display_type="adafruit"  # 👈 THIS IS KEY
)

eyes.start()

eyes.set_state("idle")
time.sleep(5)

eyes.set_state("listening")
time.sleep(5)

eyes.set_state("speaking")
time.sleep(5)

eyes.set_state("alert")
time.sleep(5)

eyes.stop()