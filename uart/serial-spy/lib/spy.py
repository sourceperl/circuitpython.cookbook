import board
import busio
import struct


# some class
class Frame:
    def __init__(self, raw: bytes=b'') -> None:
        self.raw = raw

    def __repr__(self) -> str:
        return self.as_hex

    def __len__(self) -> int:
        return len(self.raw)

    @property
    def crc_ok(self) -> bool:
        return self.crc16(self.raw[:-2]) == struct.unpack('<H', self.raw[-2:])[0]

    @property
    def as_hex(self) -> str:
        return '-'.join(['%02X' % x for x in self.raw])

    @staticmethod
    def crc16(frame: bytes) -> int:
        crc = 0xFFFF
        for byte in frame:
            crc ^= byte
            for _ in range(8):
                lsb = crc & 1
                crc >>= 1
                if lsb:
                    crc ^= 0xA001
        return crc


class Spy:
    uart = busio.UART(tx=board.GP4, rx=board.GP5)

    @classmethod
    def frames(cls, limit: int=2):
        cls.uart.timeout = 0.003
        cls.uart.reset_input_buffer()
        while True:
            b = cls.uart.read()
            if b:
                yield Frame(b)
                limit -= 1
                if limit <= 0:
                    return
