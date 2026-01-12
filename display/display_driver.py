import digitalio
import board
from adafruit_rgb_display import st7735


def init_display():
    spi = board.SPI()

    cs = digitalio.DigitalInOut(board.CE0)
    dc = digitalio.DigitalInOut(board.D25)
    rst = digitalio.DigitalInOut(board.D27)

    disp = st7735.ST7735R(
        spi,
        cs=cs,
        dc=dc,
        rst=rst,
        width=128,
        height=128,
        rotation=90,
        x_offset=3,
        y_offset=3,     # 👈 your magic number
        bgr=False
    )

    return disp