"""
Test of Waveshare RP2040-LCD-0.96 board with CircuitPython.

Load a BMP image and show it on internal display.
"""

import board
from busio import SPI
import displayio
import pwmio
import adafruit_imageload
from adafruit_st7735r import ST7735R


# some const
TFT_CLK = board.GP10
TFT_DIN = board.GP11
TFT_CS = board.GP9
TFT_DC = board.GP8
TFT_RST = board.GP12
TFT_BL = board.GP25

# avoid "in use" error on auto-reload
displayio.release_displays()
# init display backlight at 75%
display_bl = pwmio.PWMOut(TFT_BL, frequency=5_000)
display_bl.duty_cycle = 2*0xffff//3
# init display interface
spi = SPI(clock=TFT_CLK, MOSI=TFT_DIN)
display_bus = displayio.FourWire(spi, command=TFT_DC, chip_select=TFT_CS, reset=TFT_RST)
display = ST7735R(display_bus, rotation=90, width=160, height=106, invert=True)

# load a BMP (8-bits color) and show-it
bitmap, palette = adafruit_imageload.load("/img/pico.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)
display.show(group)

# loop forever
while True:
    pass
