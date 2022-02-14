import board
import busio
import adafruit_ssd1306


# some functions
def bits_iter(bytes_l):
    """Iterator over bits of a bytes list.
    Return [MSB byte0, ..., LSB byte0, MSB byte1, ...]
    """
    for b in bytes_l:
        for i in range(8):
            yield bool((b << i) & 0x80)


# init I/O and SSD display
i2c = busio.I2C(board.GP9, board.GP8)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# load image from pbm file (same size as ssd display 128*64)
with open('img.pbm', 'rb') as f:
    # skip headers
    f.readline()
    f.readline()
    f.readline()
    # load raw img
    raw_img = bytearray(f.read())

# init frame buffer with color 0
display.fill(0)
# populate buffer with color 1 on empty area (bit = 0) of raw img
for index, bit in enumerate(bits_iter(raw_img)):
    if not bit:
        x = index % 128
        y = index // 128
        display.pixel(x, y, 1)
# send frame buffer to display
display.show()
