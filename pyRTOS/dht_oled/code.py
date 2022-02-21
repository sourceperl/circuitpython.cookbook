import board
import busio
import digitalio
import pyRTOS
import adafruit_dht
import adafruit_ssd1306


def led_task(self):
    # setup
    yield
    # loop
    while True:
        led.value = not led.value
        yield [pyRTOS.timeout(.5)]


def oled_task(self):
    # setup
    global temp, hum, refresh
    yield
    # loop
    while True:
        refresh += 1
        display.fill(0)
        display.text(f'T = {temp:.1f} C', 0, 0, 1)
        display.text(f'H = {hum:.1f} %', 0, 10, 1)
        display.text(f'R = {refresh}', 0, 20, 1)
        display.show()
        yield [pyRTOS.timeout(1.0)]


def dht_task(self):
    # setup
    global temp, hum
    yield
    # loop
    while True:
        try:
            temp = dht.temperature
            hum = dht.humidity
            print(f'T: {temp:.1f} C \t H: {hum:.1f} %')
        except RuntimeError as e:
            # reading doesn't always work!
            # just print error and try again later
            print(f'DHT reading failure: {e.args}')
        yield [pyRTOS.timeout(1.0)]


# init I/O and peripherial
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
i2c = busio.I2C(board.GP9, board.GP8)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
dht = adafruit_dht.DHT22(board.GP7)

# init global vars
temp = 0.0
hum = 0.0
refresh = 0

# start tasks
pyRTOS.add_task(pyRTOS.Task(led_task, name="led_task"))
pyRTOS.add_task(pyRTOS.Task(oled_task, name="oled_task"))
pyRTOS.add_task(pyRTOS.Task(dht_task, name="dht_task"))
pyRTOS.start()
