"""Lego Halloween house automaton.

platform: Cytron Maker Pi RP2040 with rp2040
"""

import random
import time

import board
import digitalio
import lib.asyncio as aio
import neopixel
from audiomp3 import MP3Decoder
from audiopwmio import PWMAudioOut

# colors
HOUSE_BGD = 0x040808

# Melody
MELODY_NOTE = [659, 659, 0, 659, 0, 523, 659, 0, 784]
MELODY_DURATION = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.2]

# IO map
AUDIO_PWM_L_PIN = board.GP18
AUDIO_PWM_R_PIN = board.GP19
PIR_PIN = board.GP17
STORM_PIX_PIN = board.GP0
FIRE_PIX_PIN = board.GP2


# define async tasks
# lighning animation
async def lightning_anim_task():
    storm_pix.fill(HOUSE_BGD)
    while True:
        if device_active:
            # lightning series with one or more flash
            for _ in range(random.choice([1, 2, 4])):
                # lightning as LED flash
                storm_pix.fill(0xffffff)
                await aio.sleep_ms(10)
                storm_pix.fill(HOUSE_BGD)
                await aio.sleep_ms(random.randint(50, 400))
        # wait for next lightning series
        await aio.sleep_ms(random.randint(1_500, 5_000))


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
        await aio.sleep_ms(20)


# manage device active state from PIR sensor status (idle if no PIR trigger since 2 mn)
async def device_active_task():
    global device_active
    pir_trig_m = 0.0
    while True:
        if pir_input.value:
            pir_trig_m = time.monotonic()
        device_active = time.monotonic() - pir_trig_m < 120
        await aio.sleep_ms(500)


# sound task
async def sound_task():
    mp3 = open('storm.mp3', 'rb')
    decoder = MP3Decoder(mp3)
    audio = PWMAudioOut(left_channel=AUDIO_PWM_R_PIN)
    while True:
        decoder.file = open('storm.mp3', 'rb')
        audio.play(decoder)
        await aio.sleep_ms(16_000)


# debug task
async def debug_task():
    global device_active
    while True:
        print(f'{device_active=}')
        await aio.sleep_ms(1_000)


# main pogram
if __name__ == '__main__':
    # init pixels for led effects
    storm_pix = neopixel.NeoPixel(STORM_PIX_PIN, 6)
    fire_pix = neopixel.NeoPixel(FIRE_PIX_PIN, 9)
    # PIR sensor digital input
    pir_input = digitalio.DigitalInOut(PIR_PIN)
    pir_input.direction = digitalio.Direction.INPUT
    # turn on unused audio channel
    left_audio = digitalio.DigitalInOut(AUDIO_PWM_L_PIN)
    left_audio = digitalio.Direction.OUTPUT
    # init global vars
    device_active = True
    # create asyncio task and run it
    loop = aio.get_event_loop()
    loop.create_task(lightning_anim_task())
    loop.create_task(fire_anim_task())
    # loop.create_task(device_active_task())
    loop.create_task(sound_task())
    # loop.create_task(debug_task())
    loop.run_forever()
