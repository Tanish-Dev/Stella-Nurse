from luma.core.interface.serial import spi
from luma.lcd.device import st7735


def init_display():
    serial = spi(
        port=0,
        device=0,
        gpio_DC=25,
        gpio_RST=27,   # <-- DISABLE RESET
        bus_speed_hz=8000000
    )

    device = st7735(
        serial,
        width=128,
        height=128,
        rotate=2,      # VERY common fix
        bgr=True
    )

    return device