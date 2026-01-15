import digitalio
import board
from adafruit_rgb_display import st7735


def init_display():
    spi = board.SPI()

    cs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D25)
    rst = digitalio.DigitalInOut(board.D27)

    # Offsets align the active area so the first column isn't a stray blue line
    disp = st7735.ST7735R(
        spi,
        cs=cs,
        dc=dc,
        rst=rst,
        width=128,
        height=128,
        rotation=90,
        x_offset=2,
        y_offset=3,
        bgr=False
    )

    return disp