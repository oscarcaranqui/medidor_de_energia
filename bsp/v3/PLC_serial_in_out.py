
import spidev
from bsp.common.PlatformDetector import GPIO, spi_bus, spi_device


class PLC_serial_in_out():
    bus = spi_bus
    device = spi_device

    bit_order = [
        [6 - 1, 5 - 1, 4 - 1, 3 - 1, 1 - 1, 2 - 1, 7 - 1, 8 - 1],
        [1 - 1, 2 - 1, 3 - 1, 4 - 1, 5 - 1, 6 - 1, 7 - 1, 8 - 1]
    ]

    load_output_pin = 16
    load_input_pin = 18
    en_pin = 15

    def __init__(self, ext_boards: int):
        self._init_pins()
        self.max_board = ext_boards + 1
        self.last_out_lst = [0] * self.max_board
        self._serial_in_out(self.last_out_lst, True)

    def _init_pins(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.load_output_pin, GPIO.OUT)
        GPIO.setup(self.load_input_pin, GPIO.OUT)
        GPIO.setup(self.en_pin, GPIO.OUT)

        GPIO.output(self.load_output_pin, GPIO.LOW)
        GPIO.output(self.load_input_pin, GPIO.HIGH)
        GPIO.output(self.en_pin, GPIO.LOW)

    def _spi_transmit_receive(self, buffer):
        spi = spidev.SpiDev()
        spi.open(self.bus, self.device)
        spi.max_speed_hz = 500000
        spi.mode = 2
        # spi.no_cs = True
        spi.xfer2(buffer)
        spi.close()

    def _serial_in_out(self, inout: list, load_output: bool):
        if len(inout) > self.max_board + 1:
            raise PLC_serial_in_out_Error('Se excede el numero de boards de expansion instaladas %d' % self.max_board)

        buffer = [0] + [0] * 2 * len(inout)

        # mapping byte test for future check
        for i in range(8):
            buffer[0] |= ((0xaa >> self.bit_order[1][i]) & 1) << i

        GPIO.output(self.load_input_pin, GPIO.HIGH)
        if load_output:
            self.last_out_lst = inout.copy()

            # mapping output in spi buffer
            for j in range(len(inout)):
                for i in range(8):
                    buffer[2 + j * 2] |= ((inout[- j - 1] >> self.bit_order[1][i]) & 1) << i

            GPIO.output(self.load_output_pin, GPIO.LOW)

        #########################################
        # transmit adn receive spi buffer
        self._spi_transmit_receive(buffer)
        #########################################

        GPIO.output(self.load_output_pin, GPIO.HIGH)
        GPIO.output(self.load_input_pin, GPIO.LOW)

        # getting byte test from spi receive buffer
        _byte_test = 0
        for i in range(8):
            _byte_test |= ((buffer[-1] >> self.bit_order[1][i]) & 1) << i

        # getting input from spi receive buffer
        inout.clear()
        for j in range(self.max_board):
            elem = 0
            for i in range(8):
                elem |= (((~buffer[- 2 * (j + 1) - 1]) >> i) & 1) << self.bit_order[0][i]
            inout.append(elem)

        # checking byte test
        if _byte_test != 0xaa:
            raise PLC_serial_in_out_Error('Fallo de comunicacion con shift register')

    def port_output(self, out: int):
        if out > 2 ** (self.max_board * 8) or out < 0:
            raise PLC_serial_in_out_Error('salida supera el rango permitido')

        inout = []
        for idx in range(self.max_board):
            inout.append((out >> (idx * 8)) & 0xff)

        self._serial_in_out(inout=inout, load_output=True)

    def pin_output(self, pin: int, level: int):
        # pin init in 0

        if pin > (self.max_board * 8) - 1 or pin < 0:
            raise PLC_serial_in_out_Error('pin incorrecto')

        if not (level in [0, 1]):
            raise PLC_serial_in_out_Error('level incorrecto')

        idx = int(pin / 8)
        out_lst = self.last_out_lst.copy()

        if level == 0:
            out_lst[idx] &= ~(1 << (pin - (idx * 8)))
        elif level == 1:
            out_lst[idx] |= (1 << (pin - (idx * 8)))

        self._serial_in_out(inout=out_lst, load_output=True)

    def port_input(self) -> int:
        inout_lst = [0] * self.max_board
        self._serial_in_out(inout=inout_lst, load_output=False)

        port_in = 0
        for idx, elem in enumerate(inout_lst):
            port_in += elem * (2 ** (idx * 8))

        return port_in

    def pin_input(self, pin: int) -> int:
        # pin init in 0

        if pin > (self.max_board * 8) - 1 or pin < 0:
            raise PLC_serial_in_out_Error('pin incorrecto')

        port_in = self.port_input()

        return (port_in >> pin) & 1


class PLC_serial_in_out_Error(Exception):
    """Base class for config related exceptions."""
