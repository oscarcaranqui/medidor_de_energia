#!/usr/bin/python3

import struct
from dataclasses import dataclass, field, InitVar
from typing import List, Union, Type, Callable

from smbus2 import SMBus, i2c_msg
from bsp.common import BitbangIO


#############################
# i2c with bit banding mode
#############################
# you can choose whatever pins to emulate i2c protocol
# find in board class the available pins for rpi 4
@dataclass
class AddressI2Cbb:
    aplicacion: str
    scl_pin: int = field(repr=False)
    sda_pin: int = field(repr=False)
    address: int = field(repr=False)

    def read_block(self, bytes_to_read: int) -> list:
        i2c = BitbangIO.I2C(self.scl_pin, self.sda_pin)
        while not i2c.try_lock():
            pass
        result = bytearray(bytes_to_read)
        i2c.readfrom_into(self.address, result)
        i2c.unlock()

        return list(result)

    def write_block(self, buffer: list):
        i2c = BitbangIO.I2C(self.scl_pin, self.sda_pin)
        while not i2c.try_lock():
            pass
        i2c.writeto(self.address, bytearray(buffer))
        i2c.unlock()

    def write_then_read(self, reg: int, bytes_to_read: int) -> list:
        to_read = bytearray(bytes_to_read)
        i2c = BitbangIO.I2C(self.scl_pin, self.sda_pin)
        while not i2c.try_lock():
            pass
        i2c.writeto_then_readfrom(self.address, bytes([reg]), to_read)
        i2c.unlock()

        return list(to_read)


#########################
# i2c with hw
#########################
# you can use channel 0 or channel 1
# i2cdetect -y 0 -> channel 0
# i2cdetect -y 1 -> channel 1
@dataclass
class AddressI2Chw:
    aplicacion: str
    channel: int = field(repr=False)
    address: int = field(repr=False)

    def read_block(self, bytes_to_read: int) -> list:
        with SMBus(self.channel) as bus:
            msg = i2c_msg.read(self.address, bytes_to_read)
            bus.i2c_rdwr(msg)

            return list(msg)

    def write_block(self, buffer: list):
        with SMBus(self.channel) as bus:
            msg = i2c_msg.write(self.address, buffer)
            bus.i2c_rdwr(msg)

    def write_then_read(self, reg: int, bytes_to_read: int) -> list:
        with SMBus(self.channel) as bus:
            msg = i2c_msg.write(self.address, [reg])
            bus.i2c_rdwr(msg)

            msg = i2c_msg.read(self.address, bytes_to_read)
            bus.i2c_rdwr(msg)

            return list(msg)


AddressI2C = Union[AddressI2Cbb, AddressI2Chw]


@dataclass
class BitRegister:
    raw_value: InitVar[int]


@dataclass
class Register:
    code: int = field(repr=False)
    bit_rang: int = field(repr=False)
    unpack: str = field(repr=False)

    raw_value: Union[int, None] = field(init=False)

    def __post_init__(self):
        self.raw_value = None

    def read_raw_lst(self, address: AddressI2C) -> List[int]:
        return address.write_then_read(self.code, int((self.bit_rang + 7) / 8))

    def read_raw_value(self, address: AddressI2C):
        val_lst = self.read_raw_lst(address=address)
        self.raw_value = struct.unpack(self.unpack, bytearray(val_lst))[0]


@dataclass
class RegisterREG(Register):
    reg: Union[Type[BitRegister], BitRegister, None]

    def __post_init__(self):
        super().__post_init__()

    def read_value(self, address: AddressI2C):
        self.read_raw_value(address=address)

        self.reg: BitRegister = self.reg(raw_value=self.raw_value)


@dataclass
class RegisterVAL(Register):
    fn_conv: Union[Callable, None] = field(repr=False)

    value: Union[int, float, None] = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.value = None

    def read_value(self, address: AddressI2C, arg_conv: Union[int, None]):
        self.read_raw_value(address=address)

        if self.fn_conv is not None:
            self.value = self.fn_conv(self.raw_value, arg_conv)
        else:
            self.value = self.raw_value
