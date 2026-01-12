import time
from luma.core.interface.serial import spi
from luma.lcd.device import st7789

from display.eyes import RoboEyes

# SPI CONFIG — match your wiring
serial = spi(
    port=0,
    device=0,
    gpio_DC=25,
    gpio_RST=27
)

device = st7789(
    serial,
    width=128,
    height=128,
    rotate=0
)

eyes = RoboEyes(
    device=device,
    width=128,
    height=128,
    fps=30
)

eyes.start()

print("👀 RoboEyes running...")

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
    print("🛑 Stopped")