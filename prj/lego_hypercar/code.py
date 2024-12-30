import board
import lib.asyncio as aio
from pwmio import PWMOut


# some functions
def set_pulse(pwm: PWMOut, pulse_us: int, debug=False):
    period_us = 1_000_000 // pwm.frequency
    pwm.duty_cycle = 0xffff * pulse_us//period_us
    if debug:
        print(f'set pulse to {pulse_us} us ({pwm.duty_cycle=})')


# aio tasks
async def motor_task():
    global pwm_motor_bwd, pwm_motor_fwd
    # main loop
    while True:
        # forward mode 0% -> 100% -> 0%
        pwm_motor_bwd.duty_cycle = 0
        for d in range(0, 0xffff, 0x100):
            pwm_motor_fwd.duty_cycle = d
            print(d)
            await aio.sleep_ms(50)
        await aio.sleep_ms(1500)
        for d in range(0xffff, 0, -0x100):
            pwm_motor_fwd.duty_cycle = d
            print(d)
            await aio.sleep_ms(50)
        # backward mode 0% -> 100% -> 0%
        pwm_motor_fwd.duty_cycle = 0
        for d in range(0, 0xffff, 0x100):
            pwm_motor_bwd.duty_cycle = d
            print(d)
            await aio.sleep_ms(50)
        await aio.sleep_ms(1500)
        for d in range(0xffff, 0, -0x100):
            pwm_motor_bwd.duty_cycle = d
            print(d)
            await aio.sleep_ms(50)


async def steer_task():
    global pwm_steer
    # main loop
    while True:
        for pulse_us in range(1_500, 2_400, 40):
            set_pulse(pwm_steer, pulse_us)
            await aio.sleep_ms(100)

        for pulse_us in range(2_400, 1_500, -40):
            set_pulse(pwm_steer, pulse_us)
            await aio.sleep_ms(100)


# main pogram
if __name__ == '__main__':
    # init steering column servo at GPIO 12
    pwm_steer = PWMOut(board.GP12, duty_cycle=0, frequency=50)
    # init forward/backward motor command
    pwm_motor_fwd = PWMOut(board.GP9, duty_cycle=0, frequency=50)
    pwm_motor_bwd = PWMOut(board.GP8, duty_cycle=0, frequency=50)
    # create asyncio task(s) and run it
    loop = aio.get_event_loop()
    loop.create_task(motor_task())
    loop.create_task(steer_task())
    loop.run_forever()
