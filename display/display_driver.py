from luma.core.interface.serial import spi
from luma.lcd.device import st7735


def init_display():
    """
    Initializes ST7735 SPI display and returns device object
    """

    serial = spi(
        port=0,
        device=0,          # CE0
        gpio_DC=25,        # Data/Command
        gpio_RST=27,       # Reset
        bus_speed_hz=32000000
    )

    device = st7735(
        serial,
        width=128,
        height=128,
        rotate=0,          # try 2 if upside down
        bgr=True           # ST7735 uses BGR
    )

    return device