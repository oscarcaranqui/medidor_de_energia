
import time, traceback, datetime

from bsp.common.util import GYE as GYE
from bsp.common.Config import Config

from bsp.v3.modbus_generic import RegisterModBus, ModbusDeviceBase, RegistersModbus, get_value2

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
class DYN200:
    ENDIANNESS = ">"

    # torque1: RegisterModBus = RegisterModBus(0x00, 2, 0, ENDIANNESS, "i")
    # rpm_registers1: RegisterModBus = RegisterModBus(0x02, 2, 0, ENDIANNESS, "i")


    # potencia_registers: RegisterModBus = RegisterModBus(4, 2, 0, ENDIANNESS, "i")

    registers2: RegistersModbus = RegistersModbus(0, 6)




@dataclass
class MedidorDeEnergia(ModbusDeviceBase):
    registers_torque: float = field(init=False)
    registers_rpm: float = field(init=False)
    registers_potencia: float = field(init=False)
    registers: list = field(init=False)


    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:

                    slave = self.address.slave
                    registers = DYN200.registers2.get_registers(client, slave)

                    torque_registers = registers[0:2]
                    rpm_registers = registers[2:4]
                    potencia_registers = registers[4:6]

                    self.registers_torque = get_value2(torque_registers, ">", "i") / 1000
                    self.registers_rpm = get_value2(rpm_registers, ">", "i")
                    self.registers_potencia = get_value2(potencia_registers, ">", "i")


                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()


