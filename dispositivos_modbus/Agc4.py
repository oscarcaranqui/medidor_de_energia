import time, traceback

from bsp.common.Config import Config

from bsp.v3.modbus_generic import DiscreteInputModBus, ModbusDeviceBase

from dataclasses import dataclass, field

from typing import Union

# Endianess
# >         big endian
# <         little endian

# Format    C Type  Standard    size
# c         char                1
# b         signed char         1
# B         unsigned char       1
# ?         _Bool               1
# h         short               2
# H         unsigned short      2
# i         int                 4
# I         unsigned int        4
# l         long                4
# L         unsigned long       4
# q         long  long          8
# Q         unsigned long long  8
# f         float               4
# d         double              8

@dataclass
class Agc4:
    DIGITAL_INPUT_23: DiscreteInputModBus = DiscreteInputModBus(22541, 1)
    DIGITAL_INPUT_24: DiscreteInputModBus = DiscreteInputModBus(22542, 1)
    DIGITAL_INPUT_25: DiscreteInputModBus = DiscreteInputModBus(22543, 1)
    DIGITAL_INPUT_26: DiscreteInputModBus = DiscreteInputModBus(22544, 1)
    DIGITAL_INPUT_27: DiscreteInputModBus = DiscreteInputModBus(22545, 1)

    DIGITAL_INPUT_112: DiscreteInputModBus = DiscreteInputModBus(22589, 1)
    DIGITAL_INPUT_113: DiscreteInputModBus = DiscreteInputModBus(22588, 1)
    DIGITAL_INPUT_114: DiscreteInputModBus = DiscreteInputModBus(22587, 1)
    DIGITAL_INPUT_115: DiscreteInputModBus = DiscreteInputModBus(22586, 1)
    DIGITAL_INPUT_116: DiscreteInputModBus = DiscreteInputModBus(22585, 1)
    DIGITAL_INPUT_117: DiscreteInputModBus = DiscreteInputModBus(22584, 1)
    DIGITAL_INPUT_118: DiscreteInputModBus = DiscreteInputModBus(22583, 1)

    DIGITAL_OUTPUT_119: DiscreteInputModBus = DiscreteInputModBus(23049, 1)
    DIGITAL_OUTPUT_120: DiscreteInputModBus = DiscreteInputModBus(23050, 1)
    DIGITAL_OUTPUT_121: DiscreteInputModBus = DiscreteInputModBus(23051, 1)
    DIGITAL_OUTPUT_123: DiscreteInputModBus = DiscreteInputModBus(23052, 1)

    DIGITAL_OUTPUT_5: DiscreteInputModBus = DiscreteInputModBus(23025, 1)
    DIGITAL_OUTPUT_8: DiscreteInputModBus = DiscreteInputModBus(23026, 1)
    DIGITAL_OUTPUT_11: DiscreteInputModBus = DiscreteInputModBus(23027, 1)
    DIGITAL_OUTPUT_14: DiscreteInputModBus = DiscreteInputModBus(23028, 1)
    DIGITAL_OUTPUT_17: DiscreteInputModBus = DiscreteInputModBus(23029, 1)
    DIGITAL_OUTPUT_20: DiscreteInputModBus = DiscreteInputModBus(23030, 1)
    DIGITAL_OUTPUT_21: DiscreteInputModBus = DiscreteInputModBus(23031, 1)


@dataclass
class EstadoGenerador(ModbusDeviceBase):

    digital_input_23: bool = field(init=False)
    digital_input_24: bool = field(init=False)
    digital_input_25: bool = field(init=False)
    digital_input_26: bool = field(init=False)
    digital_input_27: bool = field(init=False)
    digital_input_112: bool = field(init=False)
    digital_input_113: bool = field(init=False)
    digital_input_114: bool = field(init=False)
    digital_input_115: bool = field(init=False)
    digital_input_116: bool = field(init=False)
    digital_input_117: bool = field(init=False)
    digital_input_118: bool = field(init=False)

    digital_output_119: bool = field(init=False)
    digital_output_120: bool = field(init=False)
    digital_output_121: bool = field(init=False)
    digital_output_123: bool = field(init=False)
    digital_output_5: bool = field(init=False)
    digital_output_8: bool = field(init=False)
    digital_output_11: bool = field(init=False)
    digital_output_14: bool = field(init=False)
    digital_output_17: bool = field(init=False)
    digital_output_20: bool = field(init=False)
    digital_output_21: bool = field(init=False)

    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:
                    slave = self.address.slave

                    self.digital_input_23 = Agc4.DIGITAL_INPUT_23.get_value(client, slave)[0]
                    self.digital_input_24 = Agc4.DIGITAL_INPUT_24.get_value(client, slave)[0]
                    self.digital_input_25 = Agc4.DIGITAL_INPUT_25.get_value(client, slave)[0]
                    self.digital_input_26 = Agc4.DIGITAL_INPUT_26.get_value(client, slave)[0]
                    self.digital_input_27 = Agc4.DIGITAL_INPUT_27.get_value(client, slave)[0]
                    self.digital_input_112 = Agc4.DIGITAL_INPUT_112.get_value(client, slave)[0]
                    self.digital_input_113 = Agc4.DIGITAL_INPUT_113.get_value(client, slave)[0]
                    self.digital_input_114 = Agc4.DIGITAL_INPUT_114.get_value(client, slave)[0]
                    self.digital_input_115 = Agc4.DIGITAL_INPUT_115.get_value(client, slave)[0]
                    self.digital_input_116 = Agc4.DIGITAL_INPUT_116.get_value(client, slave)[0]
                    self.digital_input_117 = Agc4.DIGITAL_INPUT_117.get_value(client, slave)[0]
                    self.digital_input_118 = Agc4.DIGITAL_INPUT_118.get_value(client, slave)[0]

                    self.digital_output_119 = Agc4.DIGITAL_OUTPUT_119.get_value(client, slave)[0]
                    self.digital_output_120 = Agc4.DIGITAL_OUTPUT_120.get_value(client, slave)[0]
                    self.digital_output_121 = Agc4.DIGITAL_OUTPUT_121.get_value(client, slave)[0]
                    self.digital_output_123 = Agc4.DIGITAL_OUTPUT_123.get_value(client, slave)[0]
                    self.digital_output_5 = Agc4.DIGITAL_OUTPUT_5.get_value(client, slave)[0]
                    self.digital_output_8 = Agc4.DIGITAL_OUTPUT_8.get_value(client, slave)[0]
                    self.digital_output_11 = Agc4.DIGITAL_OUTPUT_11.get_value(client, slave)[0]
                    self.digital_output_14 = Agc4.DIGITAL_OUTPUT_14.get_value(client, slave)[0]
                    self.digital_output_17 = Agc4.DIGITAL_OUTPUT_17.get_value(client, slave)[0]
                    self.digital_output_20 = Agc4.DIGITAL_OUTPUT_20.get_value(client, slave)[0]
                    self.digital_output_21 = Agc4.DIGITAL_OUTPUT_21.get_value(client, slave)[0]

                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
                
                
