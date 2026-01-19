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
        width=240,
        height=240,
        rotation=90,
        x_offset=0,
        y_offset=1,
        bgr=True
    )

    return disp