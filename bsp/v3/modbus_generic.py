
import struct
from bsp.common.PlatformDetector import GPIO

from dataclasses import dataclass

# import for modbus tcp
from bsp.common.my_pymodbus.sync import ModbusTcpClient
from pymodbus.transaction import ModbusSocketFramer

# import for modbus serial
from bsp.common.my_pymodbus.sync import ModbusSerialClient

from bsp.common.Config import Config

from dataclasses import field
from typing import Union, Callable


@dataclass
class AddressTCP:
    aplicacion: str
    ip: str
    port: int
    slave: int


@dataclass
class AddressSerialPort:
    #############################################
    # necesita sudo nano /boot/config
    # enable_uart=1     # rs485_x_1 -> serial0
    # dtoverlay=uart3   # rs485_x_2 -> ttyAMA1
    # #dtoverlay=uart4  # rs485_x_3 -> ttyAMA2
    # dtoverlay=uart5   # rs485_x_4 -> ttyAMA3
    #############################################

    rs485_1 = 'rs485_1'
    rs485_isolated_1 = 'rs485_isolated_1'
    rs485_2 = 'rs485_2'
    rs485_isolated_2 = 'rs485_isolated_2'
    rs485_3 = 'rs485_3'
    rs485_isolated_3 = 'rs485_isolated_3'
    rs485_4 = 'rs485_2'
    rs485_isolated_4 = 'rs485_isolated_4'

@dataclass
class AddressSerial:
    aplicacion: str
    method: str
    port: str
    baudrate: int
    slave: int

    dev_port: str = field(init=False, repr=False)
    fn_init_de_re: Callable = field(init=False, repr=False)
    fn_de_re_send: Callable = field(init=False, repr=False)
    fn_de_re_receive: Callable = field(init=False, repr=False)

    def __post_init__(self):
        def init_de_re(pin):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(pin, GPIO.OUT)

        if self.port == AddressSerialPort.rs485_1:
            self.dev_port = '/dev/serial0'
            pin = 12
            send_logic = GPIO.HIGH
            receive_logic = GPIO.LOW

        elif self.port == AddressSerialPort.rs485_isolated_1:
            self.dev_port = '/dev/serial0'
            pin = 12
            send_logic = GPIO.LOW
            receive_logic = GPIO.HIGH

        elif self.port == AddressSerialPort.rs485_2:
            self.dev_port = '/dev/ttyAMA1'
            pin = 11
            send_logic = GPIO.HIGH
            receive_logic = GPIO.LOW

        elif self.port == AddressSerialPort.rs485_isolated_2:
            self.dev_port = '/dev/ttyAMA1'
            pin = 11
            send_logic = GPIO.LOW
            receive_logic = GPIO.HIGH

        elif self.port == AddressSerialPort.rs485_3:
            self.dev_port = '/dev/ttyAMA2'
            pin = 13
            send_logic = GPIO.HIGH
            receive_logic = GPIO.LOW

        elif self.port == AddressSerialPort.rs485_isolated_3:
            self.dev_port = '/dev/ttyAMA2'
            pin = 13
            send_logic = GPIO.LOW
            receive_logic = GPIO.HIGH

        elif self.port == AddressSerialPort.rs485_4:
            self.dev_port = '/dev/ttyAMA3'
            pin = 22
            send_logic = GPIO.HIGH
            receive_logic = GPIO.LOW

        elif self.port == AddressSerialPort.rs485_isolated_4:
            self.dev_port = '/dev/ttyAMA3'
            pin = 22
            send_logic = GPIO.LOW
            receive_logic = GPIO.HIGH

        else:
            raise 'Puerto serial desconocido'

        self.fn_init_de_re = lambda: init_de_re(pin)
        self.fn_de_re_send = lambda: GPIO.output(pin, send_logic)
        self.fn_de_re_receive = lambda: GPIO.output(pin, receive_logic)

# used to umpack data
def get_value(stream: list, len: int, dec: int, endianness: str, to_umpack: str):
    bytes_stream = struct.pack(endianness + "%sH" % len, *stream)
    value = struct.unpack(endianness + to_umpack, bytes_stream)[0]

    if dec == 0:
        return value

    return value / (10 ** dec)


@dataclass
class CoilsModBus:
    reg: int
    len: int

    def get_value(self, modbus_client: Union[ModbusTcpClient, ModbusSerialClient], slave: int):
        r = modbus_client.read_coils(self.reg, self.len, unit=slave)
        return r.bits


@dataclass
class DiscreteInputModBus:
    reg: int
    len: int

    def get_value(self, modbus_client: Union[ModbusTcpClient, ModbusSerialClient], slave: int):
        r = modbus_client.read_discrete_inputs(self.reg, self.len, unit=slave)
        return r.bits


# commonly used in modbus tcp because there is no problem reading each register each time
@dataclass
class RegisterModBus:
    reg: int
    len: int
    dec: int
    endianness: str
    to_umpack: str

    def get_value(self, modbus_client: Union[ModbusTcpClient, ModbusSerialClient], slave: int):
        r = modbus_client.read_holding_registers(self.reg, self.len, unit=slave)
        stream = r.registers

        return get_value(stream=stream,
                         len=self.len,
                         dec=self.dec,
                         endianness=self.endianness,
                         to_umpack=self.to_umpack)


# commonly used in modbus serial because it is better read multiple registers
@dataclass
class RegistersModbus:
    reg: int
    len: int

    def get_registers(self, modbus_client: Union[ModbusTcpClient, ModbusSerialClient], slave: int):
        r = modbus_client.read_holding_registers(self.reg, self.len, unit=slave)
        stream = r.registers
        return stream


def get_value2(stream: list, endianness: str, to_umpack: str):
    bytes_stream = struct.pack(endianness + "%sH" % len(stream), *stream)
    value = struct.unpack(endianness + to_umpack, bytes_stream)[0]
    return value


@dataclass
class ModbusDeviceBase:
    address: Union[AddressTCP, AddressSerial]
    status: str = field(init=False)

    def get_client(self) -> Union[ModbusTcpClient, ModbusSerialClient]:
        client = None

        if type(self.address) is AddressSerial:
            self.address.fn_init_de_re()
            client = ModbusSerialClient(method=self.address.method,
                                        fn_de_re_send=self.address.fn_de_re_send,
                                        fn_de_re_receive=self.address.fn_de_re_receive,
                                        port=self.address.dev_port,
                                        baudrate=self.address.baudrate)

        elif type(self.address) is AddressTCP:
            client = ModbusTcpClient(host=self.address.ip,
                                     port=self.address.port,
                                     framer=ModbusSocketFramer,
                                     timeout=Config.TIMEOUT_MODBUS)

        return client

