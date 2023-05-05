
import time, traceback, datetime

from bsp.common.util import GYE as GYE
from bsp.common.Config import Config

from bsp.v3.modbus_generic import RegisterModBus, ModbusDeviceBase

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
class JSY_MK_322TK:
    ENDIANNESS = ">"

    PHASE_A_VOLTAGE: RegisterModBus = RegisterModBus(0x00A0, 2, 0, ENDIANNESS, "f")
    PHASE_B_VOLTAGE: RegisterModBus = RegisterModBus(0x00A2, 2, 0, ENDIANNESS, "f")
    PHASE_C_VOLTAGE: RegisterModBus = RegisterModBus(0x00A4, 2, 0, ENDIANNESS, "f")

    PHASE_A_CURRENT: RegisterModBus = RegisterModBus(0x00A6, 2, 0, ENDIANNESS, "f")
    PHASE_B_CURRENT: RegisterModBus = RegisterModBus(0x00A8, 2, 0, ENDIANNESS, "f")
    PHASE_C_CURRENT: RegisterModBus = RegisterModBus(0x00AA, 2, 0, ENDIANNESS, "f")

    PHASE_A_POWER: RegisterModBus = RegisterModBus(0x00AC, 2, 0, ENDIANNESS, "f")
    PHASE_B_POWER: RegisterModBus = RegisterModBus(0x00AE, 2, 0, ENDIANNESS, "f")
    PHASE_C_POWER: RegisterModBus = RegisterModBus(0x00B0, 2, 0, ENDIANNESS, "f")
    THREE_PHASE_TOTAL_POWER: RegisterModBus = RegisterModBus(0x00B2, 2, 0, ENDIANNESS, "f")

    PHASE_A_ACTIVE_ENERGY: RegisterModBus = RegisterModBus(0x00B4, 2, 0, ENDIANNESS, "f")
    PHASE_B_ACTIVE_ENERGY: RegisterModBus = RegisterModBus(0x00B6, 2, 0, ENDIANNESS, "f")
    PHASE_C_ACTIVE_ENERGY: RegisterModBus = RegisterModBus(0x00B8, 2, 0, ENDIANNESS, "f")
    THREE_PHASE_TOTAL_ACTIVE_ENERGY: RegisterModBus = RegisterModBus(0x00BA, 2, 0, ENDIANNESS, "f")

    PHASE_A_POWER_FACTOR: RegisterModBus = RegisterModBus(0x00BC, 2, 0, ENDIANNESS, "f")
    PHASE_B_POWER_FACTOR: RegisterModBus = RegisterModBus(0x00BE, 2, 0, ENDIANNESS, "f")
    PHASE_C_POWER_FACTOR: RegisterModBus = RegisterModBus(0x00C0, 2, 0, ENDIANNESS, "f")
    THREE_PHASE_TOTAL_POWER_FACTOR: RegisterModBus = RegisterModBus(0x00C2, 2, 0, ENDIANNESS, "f")

    PHASE_A_FREQUENCY: RegisterModBus = RegisterModBus(0x00C4, 2, 0, ENDIANNESS, "f")
    PHASE_B_FREQUENCY: RegisterModBus = RegisterModBus(0x00C6, 2, 0, ENDIANNESS, "f")
    PHASE_C_FREQUENCY: RegisterModBus = RegisterModBus(0x00C8, 2, 0, ENDIANNESS, "f")


@dataclass
class MedidorDeEnergia(ModbusDeviceBase):
    phase_a_voltage: float = field(init=False)
    phase_b_voltage: float = field(init=False)
    phase_c_voltage: float = field(init=False)

    phase_a_current: float = field(init=False)
    phase_b_current: float = field(init=False)
    phase_c_current: float = field(init=False)

    phase_a_power: float = field(init=False)
    phase_b_power: float = field(init=False)
    phase_c_powerx: float = field(init=False)
    three_phase_total_power: float = field(init=False)

    phase_a_active_energy: float = field(init=False)
    phase_b_active_energy: float = field(init=False)
    phase_c_active_energy: float = field(init=False)
    three_phase_total_active_energy: float = field(init=False)

    phase_a_power_factor: float = field(init=False)
    phase_b_power_factor: float = field(init=False)
    phase_c_power_factor: float = field(init=False)
    three_phase_total_power_factor: float = field(init=False)

    phase_a_frequency: float = field(init=False)
    phase_b_frequency: float = field(init=False)
    phase_c_frequency: float = field(init=False)

    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:

                    slave = self.address.slave

                    self.phase_a_voltage = JSY_MK_322TK.PHASE_A_VOLTAGE.get_value(client, slave)
                    self.phase_b_voltage = JSY_MK_322TK.PHASE_B_VOLTAGE.get_value(client, slave)
                    self.phase_c_voltage = JSY_MK_322TK.PHASE_C_VOLTAGE.get_value(client, slave)

                    self.phase_a_current = JSY_MK_322TK.PHASE_A_CURRENT.get_value(client, slave)
                    self.phase_b_current = JSY_MK_322TK.PHASE_B_CURRENT.get_value(client, slave)
                    self.phase_c_current = JSY_MK_322TK.PHASE_C_CURRENT.get_value(client, slave)

                    self.phase_a_power = JSY_MK_322TK.PHASE_A_POWER.get_value(client, slave)
                    self.phase_b_power = JSY_MK_322TK.PHASE_B_POWER.get_value(client, slave)
                    self.phase_c_power = JSY_MK_322TK.PHASE_C_POWER.get_value(client, slave)
                    self.three_phase_total_power = JSY_MK_322TK.THREE_PHASE_TOTAL_POWER.get_value(client, slave)

                    self.phase_a_active_energy = JSY_MK_322TK.PHASE_A_ACTIVE_ENERGY.get_value(client, slave)
                    self.phase_b_active_energy = JSY_MK_322TK.PHASE_B_ACTIVE_ENERGY.get_value(client, slave)
                    self.phase_c_active_energy = JSY_MK_322TK.PHASE_C_ACTIVE_ENERGY.get_value(client, slave)
                    self.three_phase_total_active_energy = JSY_MK_322TK.THREE_PHASE_TOTAL_ACTIVE_ENERGY.get_value(
                        client, slave)

                    self.phase_a_power_factor = JSY_MK_322TK.PHASE_A_POWER_FACTOR.get_value(client, slave)
                    self.phase_b_power_factor = JSY_MK_322TK.PHASE_B_POWER_FACTOR.get_value(client, slave)
                    self.phase_c_power_factor = JSY_MK_322TK.PHASE_C_POWER_FACTOR.get_value(client, slave)
                    self.three_phase_total_power_factor = JSY_MK_322TK.THREE_PHASE_TOTAL_POWER_FACTOR.get_value(client,
                                                                                                                slave)

                    self.phase_a_frequency = JSY_MK_322TK.PHASE_A_FREQUENCY.get_value(client, slave)
                    self.phase_b_frequency = JSY_MK_322TK.PHASE_B_FREQUENCY.get_value(client, slave)
                    self.phase_c_frequency = JSY_MK_322TK.PHASE_C_FREQUENCY.get_value(client, slave)

                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
