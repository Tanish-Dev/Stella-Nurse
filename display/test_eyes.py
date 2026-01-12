import time
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from roboeyes.eyes import RoboEyes

# SPI setup
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

# Start eyes
eyes = RoboEyes(device, fps=30)
eyes.start()

print("Testing RoboEyes...")

eyes.set_state("idle")
time.sleep(5)

eyes.set_state("listening")
time.sleep(4)

eyes.set_state("speaking")
time.sleep(4)

eyes.set_state("alert")
time.sleep(5)

eyes.stop()
print("Done.")