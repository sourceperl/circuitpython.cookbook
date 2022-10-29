"""Lego Halloween house automaton.

platform: Cytron Maker Pi RP2040 with rp2040
"""

import asyncio
import random
import time
import board
import digitalio
import neopixel


# IO map
PIEZO_PIN = board.GP22
PIR_PIN = board.GP17
STORM_PIX_PIN = board.GP26
FIRE_PIX_PIN = board.GP2


# define async tasks
# lighning animation
async def lightning_anim_task():
    while True:
        if device_active:
            # lightning series with one or more flash
            for _ in range(random.choice([1, 2, 4])):
                # lightning as LED flash
                storm_pix.fill(0xffffff)
                await asyncio.sleep_ms(10)
                storm_pix.fill(0)
                await asyncio.sleep_ms(random.randint(50, 400))
        # wait for next lightning series
        await asyncio.sleep_ms(random.randint(1_500, 5_000))


# fire animation
async def fire_anim_task():
    fire_color_t = (0xff, 0x66, 0x00)
    col_fade_by = -12
    while True:
        if device_active:
            # apply fire color to a random LED
            fire_pix[random.randint(0, len(fire_pix)-1)] = fire_color_t
            # fade down all LEDs
            fire_pix[:] = [[min(max(col+col_fade_by, 0), 255) for col in px] for px in fire_pix]
            fire_pix.show()
        else:
            fire_pix.fill(0)
        # wait for next refresh
        await asyncio.sleep_ms(20)


# manage device active state from PIR sensor status (idle if no PIR trigger since 2 mn)
async def device_active_task():
    global device_active
    pir_trig_m = 0.0
    while True:
        if pir_input.value:
            pir_trig_m = time.monotonic()
        device_active = time.monotonic() - pir_trig_m < 120
        await asyncio.sleep_ms(1_000)


# debug task
async def debug_task():
    global device_active
    while True:
        print(f'{device_active=}')
        await asyncio.sleep_ms(1_000)


# main pogram
if __name__ == '__main__':
    # init pixels for led effects
    storm_pix = neopixel.NeoPixel(STORM_PIX_PIN, 6)
    fire_pix = neopixel.NeoPixel(FIRE_PIX_PIN, 9)
    # PIR sensor digital input
    pir_input = digitalio.DigitalInOut(PIR_PIN)
    pir_input.direction = digitalio.Direction.INPUT
    # init global vars
    device_active = False
    # create asyncio task and run it
    loop = asyncio.get_event_loop()
    loop.create_task(lightning_anim_task())
    loop.create_task(fire_anim_task())
    loop.create_task(device_active_task())
    loop.create_task(debug_task())
    loop.run_forever()
