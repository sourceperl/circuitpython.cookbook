"""
Test of Waveshare RP2040-LCD-0.96 board with CircuitPython.

Display some text on internal display.
"""

import board
from busio import SPI
import displayio
import terminalio
import time
import microcontroller
from adafruit_display_text import label
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
# init display interface
spi = SPI(clock=TFT_CLK, MOSI=TFT_DIN)
display_bus = displayio.FourWire(spi, command=TFT_DC, chip_select=TFT_CS, reset=TFT_RST)
display = ST7735R(display_bus, rotation=90, width=161, height=106, invert=True, backlight_pin=TFT_BL)
display.brightness = 0.75

# make display context
main_group = displayio.Group()
display.show(main_group)

# create a text label
name_lbl = label.Label(terminalio.FONT, text='CPU temp', scale=2, color=0x008000)
name_lbl.anchor_point = (.5, .5)
name_lbl.anchored_position = (display.width//2, 20)
main_group.append(name_lbl)
val_lbl = label.Label(terminalio.FONT, text='', scale=2, color=0x0000D0)
val_lbl.anchor_point = (.5, .5)
val_lbl.anchored_position = (display.width//2, 40)
main_group.append(val_lbl)

# update value loop
while True:
    val_lbl.text = f'{microcontroller.cpu.temperature:.2f} C'
    time.sleep(1)
