from PIL import Image
from display.display_driver import init_display
import time

device = init_display()

img = Image.new("RGB", (128, 128), (255, 0, 0))  # RED
device.display(img)

print("RED SCREEN SHOULD SHOW")
time.sleep(10)