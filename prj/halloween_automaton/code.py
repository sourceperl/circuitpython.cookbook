"""Lego Halloween house automaton.

platform: Cytron Maker Pi RP2040 with rp2040
"""

import asyncio
import random
import board
import neopixel


# some const
PIEZO_PIN = board.GP22
PIXELS_PIN = board.GP26


# define async tasks
# lighning animation
async def lightning_anim_task():
    while True:
        # lightning series with one or more flash
        for _ in range(random.choice([1, 2, 4])):
            # lightning as LED flash
            pixels.fill(0xffffff)
            await asyncio.sleep_ms(10)
            pixels.fill(0x000000)
            await asyncio.sleep_ms(random.randint(50, 400))
        # wait for next lightning series
        await asyncio.sleep_ms(random.randint(1_500, 5_000))


# hello message task
async def hello_task():
    while True:
        print('hello')
        await asyncio.sleep_ms(1_000)


# main pogram
if __name__ == '__main__':
    # init pixels
    pixels = neopixel.NeoPixel(PIXELS_PIN, 6)
    # create asyncio task and run it
    loop = asyncio.get_event_loop()
    loop.create_task(lightning_anim_task())
    loop.create_task(hello_task())
    loop.run_forever()
