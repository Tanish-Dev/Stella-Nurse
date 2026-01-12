import time
import digitalio
import board
from adafruit_rgb_display import st7735
from PIL import Image

# SPI setup
spi = board.SPI()

cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D25)
reset = digitalio.DigitalInOut(board.D27)

# Display init (OFFSET FIX INCLUDED)
disp = st7735.ST7735R(
    spi,
    cs=cs,
    dc=dc,
    rst=reset,
    width=128,
    height=128,
    rotation=90,
    x_offset=2,    # <-- FIX rainbow pixels
    y_offset=1,    # <-- FIX rainbow pixels
    bgr=False
)

# Solid RED test
img = Image.new("RGB", (128, 128), (255, 0, 0))
disp.image(img)

print("RED SCREEN (no rainbow pixels)")
while True:
    time.sleep(1)