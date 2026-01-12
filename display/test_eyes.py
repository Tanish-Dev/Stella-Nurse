import time
from display.display_driver import init_display
from display.eyes import RoboEyes

device = init_display()

eyes = RoboEyes(
    device=device,
    width=128,
    height=128,
    fps=30
)

eyes.start()

try:
    eyes.set_state("idle")
    time.sleep(5)

    eyes.set_state("listening")
    time.sleep(5)

    eyes.set_state("speaking")
    time.sleep(5)

    eyes.set_state("alert")
    time.sleep(5)

finally:
    eyes.stop()