import asyncio
import gc
import board
import digitalio


# task 1
async def led_blink():
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    while True:
        led.value = True
        await asyncio.sleep_ms(100)
        led.value = False
        await asyncio.sleep_ms(100)


# task 2
async def say_hello():
    while True:
        print('time to say hello !')
        await asyncio.sleep_ms(1_000)


# task 3
async def mem_report():
    while True:
        gc.collect()
        print(f'free mem = {gc.mem_free()}')
        await asyncio.sleep_ms(2_000)


# create asyncio task and run it
loop = asyncio.get_event_loop()
loop.create_task(led_blink())
loop.create_task(say_hello())
loop.create_task(mem_report())
loop.run_forever()

