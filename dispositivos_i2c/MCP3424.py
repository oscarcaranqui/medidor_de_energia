import struct
import time
from dataclasses import dataclass, field

from bsp.v3.i2c_generic import AddressI2C

######################################################
# MCP3424 is connected to i2c0
######################################################
# it provides 4 adc channels which are connected to:
# channel 2 for batt -> adc.value_v * 110 / 10
# channel 4 for 4-20ma 1 -> adc.value_v / 75
# channel 1 for 4-20ma 2 -> adc.value_v / 75
# channel 3 is not used
######################################################

@dataclass
class ChannelSelection:
    channel_1: int = 0
    channel_2: int = 1
    channel_3: int = 2
    channel_4: int = 3


@dataclass
class SampleRate:
    sr_12bits_240sps: int = 0
    sr_14bits_60sps: int = 1
    sr_16bits_15sps: int = 2
    sr_18bits_3_75sps: int = 3


@dataclass
class PGA:
    x1: int = 0
    x2: int = 1
    x3: int = 2
    x4: int = 3


time_sample_rate = [
    0.01 + 1/240,
    0.01 + 1/60,
    0.01 + 1/15,
    0.01 + 1/3.75
]


@dataclass
class MCP3424:
    address: AddressI2C = field(repr=False)
    channel: int
    sample_rate: int
    pga: int

    value_v: int = field(init=False)
    opt_byte: int = field(init=False, repr=False)
    bytes_to_read: int = field(init=False, repr=False)

    def __post_init__(self):
        self.opt_byte = (1 << 7) | ((self.channel & 0x3) << 5) | ((self.sample_rate & 0x3) << 2) | (self.pga & 0x3)
        self.bytes_to_read = 3 if self.sample_rate == SampleRate.sr_18bits_3_75sps else 2
        self.bytes_to_read += 1
        self.read_value()

    def read_value(self):
        self.address.write_block([self.opt_byte])

        buffer = [(1 << 7)]
        while buffer[-1] & (1 << 7) != 0:
            time.sleep(time_sample_rate[self.sample_rate])
            buffer = self.address.read_block(self.bytes_to_read)

        if self.sample_rate == SampleRate.sr_18bits_3_75sps:
            new_value = struct.unpack('>i', bytearray(buffer[:-1] + [0]))[0] >> 8
        else:
            new_value = struct.unpack('>h', bytearray(buffer[:-1]))[0]

        self.value_v = new_value * (0.001 / (4 ** self.sample_rate))
