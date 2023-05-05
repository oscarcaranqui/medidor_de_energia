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
class PM135:
    ENDIANNESS = "<"

    OFFSET_BASIC_SETUP = 2304
    OFFSET_DEVICE_OPTIONS_SETUP = 2376
    OFFSET_CLOCK_INDICATION_AND_SETUP = 4352
    OFFSET_1_CYCLE_PHASE_VALUES = 13312
    OFFSET_1_CYCLE_TOTAL_VALUES = 13696
    OFFSET_PRESENT_V_A_P_DEMANDS = 14592
    OFFSET_TOTAL_ENERGIES = 14720

    PT_RATIO: RegisterModBus = RegisterModBus(OFFSET_BASIC_SETUP + 1, 1, 1, ENDIANNESS, "H")
    PT_RATIO_MULTIPLICATION_FACTOR: RegisterModBus = RegisterModBus(OFFSET_BASIC_SETUP + 20, 1, 0, ENDIANNESS, "H")
    DEVICE_RESOLUTION: RegisterModBus = RegisterModBus(OFFSET_DEVICE_OPTIONS_SETUP + 14, 1, 0, ENDIANNESS, "H")

    # Clock Indication and Setup
    SECONDS: RegisterModBus = RegisterModBus(OFFSET_CLOCK_INDICATION_AND_SETUP + 0, 1, 0, ENDIANNESS, "H")
    MINUTES: RegisterModBus = RegisterModBus(OFFSET_CLOCK_INDICATION_AND_SETUP + 1, 1, 0, ENDIANNESS, "H")
    HOUR: RegisterModBus = RegisterModBus(OFFSET_CLOCK_INDICATION_AND_SETUP + 2, 1, 0, ENDIANNESS, "H")
    DAY_MONTH: RegisterModBus = RegisterModBus(OFFSET_CLOCK_INDICATION_AND_SETUP + 3, 1, 0, ENDIANNESS, "H")
    MONTH: RegisterModBus = RegisterModBus(OFFSET_CLOCK_INDICATION_AND_SETUP + 4, 1, 0, ENDIANNESS, "H")
    YEAR: RegisterModBus = RegisterModBus(OFFSET_CLOCK_INDICATION_AND_SETUP + 5, 1, 0, ENDIANNESS, "H")

    # 1 cycle phase values
    V1_V12_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 0, 2, 0, ENDIANNESS, "I")
    V2_V23_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 2, 2, 0, ENDIANNESS, "I")
    V3_V31_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 4, 2, 0, ENDIANNESS, "I")

    I1_CURRENT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 6, 2, 0, ENDIANNESS, "I")
    I2_CURRENT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 8, 2, 0, ENDIANNESS, "I")
    I3_CURRENT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 10, 2, 0, ENDIANNESS, "I")

    kW_L1: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 12, 2, 0, ENDIANNESS, "i")
    kW_L2: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 14, 2, 0, ENDIANNESS, "i")
    kW_L3: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 16, 2, 0, ENDIANNESS, "i")

    kvar_L1: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 18, 2, 0, ENDIANNESS, "i")
    kvar_L2: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 20, 2, 0, ENDIANNESS, "i")
    kvar_L3: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 22, 2, 0, ENDIANNESS, "i")

    KVA_L1: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 24, 2, 0, ENDIANNESS, "I")
    KVA_L2: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 26, 2, 0, ENDIANNESS, "I")
    KVA_L3: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 28, 2, 0, ENDIANNESS, "I")

    POWER_FACTOR_L1: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 30, 2, 3, ENDIANNESS, "i")
    POWER_FACTOR_L2: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 32, 2, 3, ENDIANNESS, "i")
    POWER_FACTOR_L3: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 34, 2, 3, ENDIANNESS, "i")

    V1_V12_THD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 36, 2, 1, ENDIANNESS, "I")
    V2_V23_THD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 38, 2, 1, ENDIANNESS, "I")
    V3_V31_THD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 40, 2, 1, ENDIANNESS, "I")

    I1_CURRENT_THD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 42, 2, 1, ENDIANNESS, "I")
    I2_CURRENT_THD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 44, 2, 1, ENDIANNESS, "I")
    I3_CURRENT_THD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 46, 2, 1, ENDIANNESS, "I")

    I1_K_FACTOR: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 48, 2, 1, ENDIANNESS, "I")
    I2_K_FACTOR: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 50, 2, 1, ENDIANNESS, "I")
    I3_K_FACTOR: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 52, 2, 1, ENDIANNESS, "I")

    I1_CURRENT_TDD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 54, 2, 1, ENDIANNESS, "I")
    I2_CURRENT_TDD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 56, 2, 1, ENDIANNESS, "I")
    I3_CURRENT_TDD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 58, 2, 1, ENDIANNESS, "I")

    V12_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 60, 2, 0, ENDIANNESS, "I")
    V23_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 62, 2, 0, ENDIANNESS, "I")
    V31_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_PHASE_VALUES + 64, 2, 0, ENDIANNESS, "I")

    # # 1_cycle_total_values
    TOTAL_KW: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 0, 2, 0, ENDIANNESS, "i")
    TOTAL_kvar: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 2, 2, 0, ENDIANNESS, "i")
    TOTAL_KVA: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 4, 2, 0, ENDIANNESS, "I")
    TOTAL_PF: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 6, 2, 3, ENDIANNESS, "i")
    TOTAL_PF_LAG: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 8, 2, 3, ENDIANNESS, "I")
    TOTAL_PF_LEAD: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 10, 2, 3, ENDIANNESS, "I")
    TOTAL_KW_IMPORT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 12, 2, 0, ENDIANNESS, "I")
    TOTAL_KW_EXPORT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 14, 2, 0, ENDIANNESS, "I")
    TOTAL_KVAR_IMPORT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 16, 2, 0, ENDIANNESS, "I")
    TOTAL_KVAR_EXPORT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 18, 2, 0, ENDIANNESS, "I")
    THREE_PHASE_AVERAGE_LN_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 20, 2, 0, ENDIANNESS, "I")
    THREE_PHASE_AVERAGE_LL_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 22, 2, 0, ENDIANNESS, "I")
    THREE_PHASE_AVERAGE_CURRENT: RegisterModBus = RegisterModBus(OFFSET_1_CYCLE_TOTAL_VALUES + 24, 2, 0, ENDIANNESS, "I")

    # # present_V_A_P_demands
    V1_V12_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 0, 2, 0, ENDIANNESS, "I")
    V2_V23_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 2, 2, 0, ENDIANNESS, "I")
    V3_V31_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 4, 2, 0, ENDIANNESS, "I")
    I1_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 6, 2, 0, ENDIANNESS, "I")
    I2_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 8, 2, 0, ENDIANNESS, "I")
    I3_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 10, 2, 0, ENDIANNESS, "I")
    KW_IMPORT_BLOCK_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 12, 2, 0, ENDIANNESS, "I")
    KVAR_IMPORT_BLOCK_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 14, 2, 0, ENDIANNESS, "I")
    KVA_BLOCK_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 16, 2, 0, ENDIANNESS, "I")
    KW_IMPORT_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 18, 2, 0, ENDIANNESS, "I")
    KVAR_IMPORT_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 20, 2, 0, ENDIANNESS, "I")
    KVA_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 22, 2, 0, ENDIANNESS, "I")
    KW_IMPORT_ACCUMULATED_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 30, 2, 0, ENDIANNESS, "I")
    KVAR_IMPORT_ACCUMULATED_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 32, 2, 0, ENDIANNESS, "I")
    KVA_ACCUMULATED_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 34, 2, 0, ENDIANNESS, "I")
    KW_IMPORT_PREDICTED_SLIDING_: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 36, 2, 0, ENDIANNESS, "I")
    KVAR_IMPORT_PREDICTED_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 38, 2, 0, ENDIANNESS, "I")
    KVA_PREDICTED_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 40, 2, 0, ENDIANNESS, "I")
    PF_IMPORT_AT_MAX_KVA_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 42, 2, 3, ENDIANNESS, "I")
    KW_EXPORT_BLOCK_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 44, 2, 0, ENDIANNESS, "I")
    KVAR_EXPORT_BLOCK_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 46, 2, 0, ENDIANNESS, "I")
    KW_EXPORT_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 48, 2, 0, ENDIANNESS, "I")
    KVAR_EXPORT_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 50, 2, 0, ENDIANNESS, "I")
    KW_EXPORT_ACCUMULATED_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 52, 2, 0, ENDIANNESS, "I")
    KVAR_EXPORT_ACCUMULATED_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 54, 2, 0, ENDIANNESS, "I")
    KW_EXPORT_PREDICTED_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 56, 2, 0, ENDIANNESS, "I")
    KVAR_EXPORT_PREDICTED_SLIDING_WINDOW_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 58, 2, 0, ENDIANNESS, "I")
    IN_A_DEMAND: RegisterModBus = RegisterModBus(OFFSET_PRESENT_V_A_P_DEMANDS + 68, 2, 0, ENDIANNESS, "I")

    # # total_energies
    KWH_IMPORT: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 0, 2, 0, ENDIANNESS, "I")
    KWH_EXPORT: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 2, 2, 0, ENDIANNESS, "I")
    KVARH_IMPORT: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 8, 2, 0, ENDIANNESS, "I")
    KVARH_EXPORT: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 10, 2, 0, ENDIANNESS, "I")
    KVAH_TOTAL: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 16, 2, 0, ENDIANNESS, "I")
    KVAH_IMPORT: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 22, 2, 0, ENDIANNESS, "I")
    KVAH_EXPORT: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 24, 2, 0, ENDIANNESS, "I")
    KVARH_Q1: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 26, 2, 0, ENDIANNESS, "I")
    KVARH_Q2: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 28, 2, 0, ENDIANNESS, "I")
    KVARH_Q3: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 30, 2, 0, ENDIANNESS, "I")
    KVARH_Q4: RegisterModBus = RegisterModBus(OFFSET_TOTAL_ENERGIES + 32, 2, 0, ENDIANNESS, "I")


@dataclass
class MedidorDeEnergia(ModbusDeviceBase):
    pt_ratio: float = field(init=False)
    device_resolution: float = field(init=False)

    # PRESENT DATE & TIME
    date: datetime = field(init=False)

    # 1 cycle phase values
    v1_v12_voltage: float = field(init=False)
    v2_v23_voltage: float = field(init=False)
    v3_v31_voltage: float = field(init=False)

    i1_current: float = field(init=False)
    i2_current: float = field(init=False)
    i3_current: float = field(init=False)

    kw_l1: float = field(init=False)
    kw_l2: float = field(init=False)
    kw_l3: float = field(init=False)

    kvar_l1: float = field(init=False)
    kvar_l2: float = field(init=False)
    kvar_l3: float = field(init=False)

    kva_l1: float = field(init=False)
    kva_l2: float = field(init=False)
    kva_l3: float = field(init=False)

    power_factor_l1: float = field(init=False)
    power_factor_l2: float = field(init=False)
    power_factor_l3: float = field(init=False)

    v1_v12_thd: float = field(init=False)
    v2_v23_thd: float = field(init=False)
    v3_v31_thd: float = field(init=False)

    i1_current_thd: float = field(init=False)
    i2_current_thd: float = field(init=False)
    i3_current_thd: float = field(init=False)

    i1_k_factor: float = field(init=False)
    i2_k_factor: float = field(init=False)
    i3_k_factor: float = field(init=False)

    i1_current_tdd: float = field(init=False)
    i2_current_tdd: float = field(init=False)
    i3_current_tdd: float = field(init=False)

    v12_voltage: float = field(init=False)
    v23_voltage: float = field(init=False)
    v31_voltage: float = field(init=False)

    # # 1_cycle_total_values
    total_kw: float = field(init=False)
    total_kvar: float = field(init=False)
    total_kva: float = field(init=False)
    total_pf: float = field(init=False)
    total_pf_lag: float = field(init=False)
    total_pf_lead: float = field(init=False)
    total_kw_import: float = field(init=False)
    total_kw_export: float = field(init=False)
    total_kvar_import: float = field(init=False)
    total_kvar_export: float = field(init=False)
    three_phase_average_ln_voltage: float = field(init=False)
    three_phase_average_ll_voltage: float = field(init=False)
    three_phase_average_current: float = field(init=False)

    # # present_v_a_p_demands
    v1_v12_demand: float = field(init=False)
    v2_v23_demand: float = field(init=False)
    v3_v31_demand: float = field(init=False)
    i1_demand: float = field(init=False)
    i2_demand: float = field(init=False)
    i3_demand: float = field(init=False)
    kw_import_block_demand: float = field(init=False)
    kvar_import_block_demand: float = field(init=False)
    kva_block_demand: float = field(init=False)
    kw_import_sliding_window_demand: float = field(init=False)
    kvar_import_sliding_window_demand: float = field(init=False)
    kva_sliding_window_demand: float = field(init=False)
    kw_import_accumulated_demand: float = field(init=False)
    kvar_import_accumulated_demand: float = field(init=False)
    kva_accumulated_demand: float = field(init=False)
    kw_import_predicted_sliding_: float = field(init=False)
    kvar_import_predicted_sliding_window_demand: float = field(init=False)
    kva_predicted_sliding_window_demand: float = field(init=False)
    pf_import_at_max_kva_demand: float = field(init=False)
    kw_export_block_demand: float = field(init=False)
    kvar_export_block_demand: float = field(init=False)
    kw_export_sliding_window_demand: float = field(init=False)
    kvar_export_sliding_window_demand: float = field(init=False)
    kw_export_accumulated_demand: float = field(init=False)
    kvar_export_accumulated_demand: float = field(init=False)
    kw_export_predicted_sliding_window_demand: float = field(init=False)
    kvar_export_predicted_sliding_window_demand: float = field(init=False)
    in_a_demand: float = field(init=False)

    # # total_energies
    kwh_import: float = field(init=False)
    kwh_export: float = field(init=False)
    kvarh_import: float = field(init=False)
    kvarh_export: float = field(init=False)
    kvah_total: float = field(init=False)
    kvah_import: float = field(init=False)
    kvah_export: float = field(init=False)
    kvarh_q1: float = field(init=False)
    kvarh_q2: float = field(init=False)
    kvarh_q3: float = field(init=False)
    kvarh_q4: float = field(init=False)

    def set_unit_U1(self, value: int):
        if self.device_resolution == 0:
            return value

        if self.pt_ratio == 1:
            return round(value * 0.1, 1)

        return value

    def set_unit_U2(self, value: int):
        if self.device_resolution == 0:
            return value

        return round(value * 0.01, 2)

    def set_unit_U3(self, value: int):
        if self.device_resolution == 0:
            return value

        if self.pt_ratio == 1:
            return round(value * 0.001, 3)

        return value

    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:

                    slave = self.address.slave

                    self.pt_ratio = PM135.PT_RATIO.get_value(client, slave)
                    self.device_resolution = PM135.DEVICE_RESOLUTION.get_value(client, slave)

                    # PRESENT DATE & TIME
                    year = PM135.YEAR.get_value(client, slave) + 2000
                    month = PM135.MONTH.get_value(client, slave)
                    day = PM135.DAY_MONTH.get_value(client, slave)
                    hour = PM135.HOUR.get_value(client, slave)
                    minute = PM135.MINUTES.get_value(client, slave)
                    second = PM135.SECONDS.get_value(client, slave)

                    self.date = datetime.datetime(year=year, month=month, day=day,
                                                  hour=hour, minute=minute, second=second, tzinfo=GYE)

                    # 1 cycle phase values
                    self.v1_v12_voltage = self.set_unit_U1(PM135.V1_V12_VOLTAGE.get_value(client, slave))
                    self.v2_v23_voltage = self.set_unit_U1(PM135.V2_V23_VOLTAGE.get_value(client, slave))
                    self.v3_v31_voltage = self.set_unit_U1(PM135.V3_V31_VOLTAGE.get_value(client, slave))

                    self.i1_current = self.set_unit_U2(PM135.I1_CURRENT.get_value(client, slave))
                    self.i2_current = self.set_unit_U2(PM135.I2_CURRENT.get_value(client, slave))
                    self.i3_current = self.set_unit_U2(PM135.I3_CURRENT.get_value(client, slave))

                    self.kw_l1 = self.set_unit_U3(PM135.kW_L1.get_value(client, slave))
                    self.kw_l2 = self.set_unit_U3(PM135.kW_L2.get_value(client, slave))
                    self.kw_l3 = self.set_unit_U3(PM135.kW_L3.get_value(client, slave))

                    self.kvar_l1 = self.set_unit_U3(PM135.kvar_L1.get_value(client, slave))
                    self.kvar_l2 = self.set_unit_U3(PM135.kvar_L2.get_value(client, slave))
                    self.kvar_l3 = self.set_unit_U3(PM135.kvar_L3.get_value(client, slave))

                    self.kva_l1 = self.set_unit_U3(PM135.KVA_L1.get_value(client, slave))
                    self.kva_l2 = self.set_unit_U3(PM135.KVA_L2.get_value(client, slave))
                    self.kva_l3 = self.set_unit_U3(PM135.KVA_L3.get_value(client, slave))

                    self.power_factor_l1 = PM135.POWER_FACTOR_L1.get_value(client, slave)
                    self.power_factor_l2 = PM135.POWER_FACTOR_L2.get_value(client, slave)
                    self.power_factor_l3 = PM135.POWER_FACTOR_L3.get_value(client, slave)

                    self.v1_v12_thd = PM135.V1_V12_THD.get_value(client, slave)
                    self.v2_v23_thd = PM135.V2_V23_THD.get_value(client, slave)
                    self.v3_v31_thd = PM135.V3_V31_THD.get_value(client, slave)

                    self.i1_current_thd = PM135.I1_CURRENT_THD.get_value(client, slave)
                    self.i2_current_thd = PM135.I2_CURRENT_THD.get_value(client, slave)
                    self.i3_current_thd = PM135.I3_CURRENT_THD.get_value(client, slave)

                    self.i1_k_factor = PM135.I1_K_FACTOR.get_value(client, slave)
                    self.i2_k_factor = PM135.I2_K_FACTOR.get_value(client, slave)
                    self.i3_k_factor = PM135.I3_K_FACTOR.get_value(client, slave)

                    self.i1_current_tdd = PM135.I1_CURRENT_TDD.get_value(client, slave)
                    self.i2_current_tdd = PM135.I2_CURRENT_TDD.get_value(client, slave)
                    self.i3_current_tdd = PM135.I3_CURRENT_TDD.get_value(client, slave)

                    self.v12_voltage = self.set_unit_U1(PM135.V12_VOLTAGE.get_value(client, slave))
                    self.v23_voltage = self.set_unit_U1(PM135.V23_VOLTAGE.get_value(client, slave))
                    self.v31_voltage = self.set_unit_U1(PM135.V31_VOLTAGE.get_value(client, slave))

                    # # 1_cycle_total_values
                    self.total_kw = self.set_unit_U3(PM135.TOTAL_KW.get_value(client, slave))
                    self.total_kvar = self.set_unit_U3(PM135.TOTAL_kvar.get_value(client, slave))
                    self.total_kva = self.set_unit_U3(PM135.TOTAL_KVA.get_value(client, slave))
                    self.total_pf = PM135.TOTAL_PF.get_value(client, slave)
                    self.total_pf_lag = PM135.TOTAL_PF_LAG.get_value(client, slave)
                    self.total_pf_lead = PM135.TOTAL_PF_LEAD.get_value(client, slave)
                    self.total_kw_import = self.set_unit_U3(PM135.TOTAL_KW_IMPORT.get_value(client, slave))
                    self.total_kw_export = self.set_unit_U3(PM135.TOTAL_KW_EXPORT.get_value(client, slave))
                    self.total_kvar_import = self.set_unit_U3(PM135.TOTAL_KVAR_IMPORT.get_value(client, slave))
                    self.total_kvar_export = self.set_unit_U3(PM135.TOTAL_KVAR_EXPORT.get_value(client, slave))
                    self.three_phase_average_ln_voltage = \
                        self.set_unit_U1(PM135.THREE_PHASE_AVERAGE_LN_VOLTAGE.get_value(client, slave))
                    self.three_phase_average_ll_voltage = \
                        self.set_unit_U1(PM135.THREE_PHASE_AVERAGE_LL_VOLTAGE.get_value(client, slave))
                    self.three_phase_average_current = \
                        self.set_unit_U1(PM135.THREE_PHASE_AVERAGE_CURRENT.get_value(client, slave))

                    # # # present_v_a_p_demands
                    self.v1_v12_demand = self.set_unit_U1(PM135.V1_V12_DEMAND.get_value(client, slave))
                    self.v2_v23_demand = self.set_unit_U1(PM135.V2_V23_DEMAND.get_value(client, slave))
                    self.v3_v31_demand = self.set_unit_U1(PM135.V3_V31_DEMAND.get_value(client, slave))
                    self.i1_demand = self.set_unit_U2(PM135.I1_DEMAND.get_value(client, slave))
                    self.i2_demand = self.set_unit_U2(PM135.I2_DEMAND.get_value(client, slave))
                    self.i3_demand = self.set_unit_U2(PM135.I3_DEMAND.get_value(client, slave))
                    self.kw_import_block_demand = \
                        self.set_unit_U3(PM135.KW_IMPORT_BLOCK_DEMAND.get_value(client, slave))
                    self.kvar_import_block_demand = \
                        self.set_unit_U3(PM135.KVAR_IMPORT_BLOCK_DEMAND.get_value(client, slave))
                    self.kva_block_demand = self.set_unit_U3(PM135.KVA_BLOCK_DEMAND.get_value(client, slave))
                    self.kw_import_sliding_window_demand = \
                        self.set_unit_U3(PM135.KW_IMPORT_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kvar_import_sliding_window_demand = \
                        self.set_unit_U3(PM135.KVAR_IMPORT_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kva_sliding_window_demand = \
                        self.set_unit_U3(PM135.KVA_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kw_import_accumulated_demand = \
                        self.set_unit_U3(PM135.KW_IMPORT_ACCUMULATED_DEMAND.get_value(client, slave))
                    self.kvar_import_accumulated_demand = \
                        self.set_unit_U3(PM135.KVAR_IMPORT_ACCUMULATED_DEMAND.get_value(client, slave))
                    self.kva_accumulated_demand = \
                        self.set_unit_U3(PM135.KVA_ACCUMULATED_DEMAND.get_value(client, slave))
                    self.kw_import_predicted_sliding_ = \
                        self.set_unit_U3(PM135.KW_IMPORT_PREDICTED_SLIDING_.get_value(client, slave))
                    self.kvar_import_predicted_sliding_window_demand = \
                        self.set_unit_U3(PM135.KVAR_IMPORT_PREDICTED_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kva_predicted_sliding_window_demand = \
                        self.set_unit_U3(PM135.KVA_PREDICTED_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.pf_import_at_max_kva_demand = PM135.PF_IMPORT_AT_MAX_KVA_DEMAND.get_value(client, slave)
                    self.kw_export_block_demand = \
                        self.set_unit_U3(PM135.KW_EXPORT_BLOCK_DEMAND.get_value(client, slave))
                    self.kvar_export_block_demand = \
                        self.set_unit_U3(PM135.KVAR_EXPORT_BLOCK_DEMAND.get_value(client, slave))
                    self.kw_export_sliding_window_demand = \
                        self.set_unit_U3(PM135.KW_EXPORT_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kvar_export_sliding_window_demand = \
                        self.set_unit_U3(PM135.KVAR_EXPORT_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kw_export_accumulated_demand = \
                        self.set_unit_U3(PM135.KW_EXPORT_ACCUMULATED_DEMAND.get_value(client, slave))
                    self.kvar_export_accumulated_demand = \
                        self.set_unit_U3(PM135.KVAR_EXPORT_ACCUMULATED_DEMAND.get_value(client, slave))
                    self.kw_export_predicted_sliding_window_demand = \
                        self.set_unit_U3(PM135.KW_EXPORT_PREDICTED_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.kvar_export_predicted_sliding_window_demand = \
                        self.set_unit_U3(PM135.KVAR_EXPORT_PREDICTED_SLIDING_WINDOW_DEMAND.get_value(client, slave))
                    self.in_a_demand = self.set_unit_U2(PM135.IN_A_DEMAND.get_value(client, slave))

                    # # total_energies
                    self.kwh_import = PM135.KWH_IMPORT.get_value(client, slave)
                    self.kwh_export = PM135.KWH_EXPORT.get_value(client, slave)
                    self.kvarh_import = PM135.KVARH_IMPORT.get_value(client, slave)
                    self.kvarh_export = PM135.KVARH_EXPORT.get_value(client, slave)
                    self.kvah_total = PM135.KVAH_TOTAL.get_value(client, slave)
                    self.kvah_import = PM135.KVAH_IMPORT.get_value(client, slave)
                    self.kvah_export = PM135.KVAH_EXPORT.get_value(client, slave)
                    self.kvarh_q1 = PM135.KVARH_Q1.get_value(client, slave)
                    self.kvarh_q2 = PM135.KVARH_Q2.get_value(client, slave)
                    self.kvarh_q3 = PM135.KVARH_Q3.get_value(client, slave)
                    self.kvarh_q4 = PM135.KVARH_Q4.get_value(client, slave)

                    self.status = "OK"

                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()


