import time
from random import randint, random

import board
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

led.value = False
time.sleep(randint(5, 10))

while True:
    led.value = True
    x_move = randint(4, 8)
    y_move = randint(4, 8)
    if random() > 0.5:
        mouse.move(x=x_move)
        time.sleep(0.5 * random())
        mouse.move(x=-x_move)
    else:
        mouse.move(y=y_move)
        time.sleep(0.5 * random())
        mouse.move(y=-y_move)
    led.value = False
    time.sleep(randint(60, 120))
