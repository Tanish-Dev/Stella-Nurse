import digitalio
import board
from adafruit_rgb_display import st7735
from PIL import Image, ImageDraw

cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D25)
reset = digitalio.DigitalInOut(board.D27)

spi = board.SPI()

disp = st7735.ST7735R(
    spi,
    cs=cs,
    dc=dc,
    rst=reset,
    width=128,
    height=128,
    rotation=90
)

img = Image.new("RGB", (128,128), (255,0,0))
disp.image(img)