""" a basic example of the waveshare RP2040-Keyboard-3 board with CircuitPython

more at https://www.waveshare.com/wiki/RP2040-Keyboard-3
"""

import time

import board
import keypad
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# init neopixels
pixels = neopixel.NeoPixel(board.GP18, 3, auto_write=True)

# init keypad
keys = keypad.Keys(pins=(board.GP14, board.GP13, board.GP12), value_when_pressed=False, pull=True, max_events=128)
keymap = (('Ctrl', 0), ('C', 1), ('V', 2))

# init HID keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# main loop
while True:
    # scan keypad
    key_evt = keys.events.get()
    if key_evt:
        key, pix_id = keymap[key_evt.key_number]
        if key_evt.pressed:
            print(f'press "{key}"')
            pixels[pix_id] = (255, 0, 0)
            layout.write(key)
        else:
            print(f'release "{key}"')
            pixels[pix_id] = (0, 0, 0)
    time.sleep(.05)
