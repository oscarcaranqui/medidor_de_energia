import time, traceback, datetime

from bsp.common.util import GYE as GYE

from bsp.common.Config import Config

from bsp.v3.modbus_generic import RegisterModBus, ModbusDeviceBase

from dataclasses import dataclass, field

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
class PM5100:
    ENDIANNESS = ">"

    # PRESENT DATE & TIME
    YEAR: RegisterModBus = RegisterModBus(1837 - 1, 1, 0, ENDIANNESS, "H")
    MONTH: RegisterModBus = RegisterModBus(1838 - 1, 1, 0, ENDIANNESS, "H")
    DAY: RegisterModBus = RegisterModBus(1839 - 1, 1, 0, ENDIANNESS, "H")
    HOUR: RegisterModBus = RegisterModBus(1840 - 1, 1, 0, ENDIANNESS, "H")
    MINUTE: RegisterModBus = RegisterModBus(1841 - 1, 1, 0, ENDIANNESS, "H")
    SECOND: RegisterModBus = RegisterModBus(1842 - 1, 1, 0, ENDIANNESS, "H")

    # ACCUMULATED ENERGY - 32 BIT FLOATING POINT VALUES
    ACTIVE_ENERGY_DELIVERED: RegisterModBus = RegisterModBus(2700 - 1, 2, 0, ENDIANNESS, "f")
    ACTIVE_ENERGY_RECEIVED: RegisterModBus = RegisterModBus(2702 - 1, 2, 0, ENDIANNESS, "f")
    ACTIVE_ENERGY_DELIVERED_MORE_RECEIVED: RegisterModBus = RegisterModBus(2704 - 1, 2, 0, ENDIANNESS, "f")
    ACTIVE_ENERGY_DELIVERD_LESS_RECEIVED: RegisterModBus = RegisterModBus(2706 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_ENERGY_DELIVERED: RegisterModBus = RegisterModBus(2708 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_ENERGY_RECEIVED: RegisterModBus = RegisterModBus(2710 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_ENERGY_DELIVERED_MORE_RECEIVED: RegisterModBus = RegisterModBus(2712 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_ENERGY_DELIVERED_LESS_RECEIVED: RegisterModBus = RegisterModBus(2714 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_ENERGY_DELIVERED: RegisterModBus = RegisterModBus(2716 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_ENERGY_RECEIVED: RegisterModBus = RegisterModBus(2718 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_ENERGY_DELIVERD_MORE_RECEIVED: RegisterModBus = RegisterModBus(2720 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_ENERGY_DELIVERD_LESS_RECEIVED: RegisterModBus = RegisterModBus(2722 - 1, 2, 0, ENDIANNESS, "f")

    # CURRENT
    CURRENT_A: RegisterModBus = RegisterModBus(3000 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_B: RegisterModBus = RegisterModBus(3002 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_C: RegisterModBus = RegisterModBus(3004 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_N: RegisterModBus = RegisterModBus(3006 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_G: RegisterModBus = RegisterModBus(3008 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_AVG: RegisterModBus = RegisterModBus(3010 - 1, 2, 0, ENDIANNESS, "f")

    # CURRENT UNBALANCE
    CURRENT_UNBALANCE_A: RegisterModBus = RegisterModBus(3012 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_UNBALANCE_B: RegisterModBus = RegisterModBus(3014 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_UNBALANCE_C: RegisterModBus = RegisterModBus(3016 - 1, 2, 0, ENDIANNESS, "f")
    CURRENT_UNBALANCE_WORST: RegisterModBus = RegisterModBus(3018 - 1, 2, 0, ENDIANNESS, "f")

    # VOLTAGE
    VOLTAGE_AB: RegisterModBus = RegisterModBus(3020 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_BC: RegisterModBus = RegisterModBus(3022 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_CA: RegisterModBus = RegisterModBus(3024 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_LL_AVG: RegisterModBus = RegisterModBus(3026 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_AN: RegisterModBus = RegisterModBus(3028 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_BN: RegisterModBus = RegisterModBus(3030 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_CN: RegisterModBus = RegisterModBus(3032 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_NG: RegisterModBus = RegisterModBus(3034 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_LN_AVG: RegisterModBus = RegisterModBus(3036 - 1, 2, 0, ENDIANNESS, "f")

    # VOLTAGE UNBALANCE
    VOLTAGE_UNBALANCE_AB: RegisterModBus = RegisterModBus(3038 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_BC: RegisterModBus = RegisterModBus(3040 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_CA: RegisterModBus = RegisterModBus(3042 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_LL_WORST: RegisterModBus = RegisterModBus(3044 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_AN: RegisterModBus = RegisterModBus(3046 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_BN: RegisterModBus = RegisterModBus(3048 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_CN: RegisterModBus = RegisterModBus(3050 - 1, 2, 0, ENDIANNESS, "f")
    VOLTAGE_UNBALANCE_LN_WORST: RegisterModBus = RegisterModBus(3052 - 1, 2, 0, ENDIANNESS, "f")

    # POWER
    ACTIVE_POWER_A: RegisterModBus = RegisterModBus(3054 - 1, 2, 0, ENDIANNESS, "f")
    ACTIVE_POWER_B: RegisterModBus = RegisterModBus(3056 - 1, 2, 0, ENDIANNESS, "f")
    ACTIVE_POWER_C: RegisterModBus = RegisterModBus(3058 - 1, 2, 0, ENDIANNESS, "f")
    ACTIVE_POWER_TOTAL: RegisterModBus = RegisterModBus(3060 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_POWER_A: RegisterModBus = RegisterModBus(3062 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_POWER_B: RegisterModBus = RegisterModBus(3064 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_POWER_C: RegisterModBus = RegisterModBus(3066 - 1, 2, 0, ENDIANNESS, "f")
    REACTIVE_POWER_TOTAL: RegisterModBus = RegisterModBus(3068 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_POWER_A: RegisterModBus = RegisterModBus(3070 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_POWER_B: RegisterModBus = RegisterModBus(3072 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_POWER_C: RegisterModBus = RegisterModBus(3074 - 1, 2, 0, ENDIANNESS, "f")
    APPARENT_POWER_TOTAL: RegisterModBus = RegisterModBus(3076 - 1, 2, 0, ENDIANNESS, "f")

    # POWER FACTOR
    POWER_FACTOR_A: RegisterModBus = RegisterModBus(3078 - 1, 2, 0, ENDIANNESS, "f")
    POWER_FACTOR_B: RegisterModBus = RegisterModBus(3080 - 1, 2, 0, ENDIANNESS, "f")
    POWER_FACTOR_C: RegisterModBus = RegisterModBus(3082 - 1, 2, 0, ENDIANNESS, "f")
    POWER_FACTOR_TOTAL: RegisterModBus = RegisterModBus(3084 - 1, 2, 0, ENDIANNESS, "f")
    DISPLACEMENT_POWER_FACTOR_A: RegisterModBus = RegisterModBus(3086 - 1, 2, 0, ENDIANNESS, "f")
    DISPLACEMENT_POWER_FACTOR_B: RegisterModBus = RegisterModBus(3088 - 1, 2, 0, ENDIANNESS, "f")
    DISPLACEMENT_POWER_FACTOR_C: RegisterModBus = RegisterModBus(3090 - 1, 2, 0, ENDIANNESS, "f")
    DISPLACEMENT_POWER_FACTOR_TOTAL: RegisterModBus = RegisterModBus(3092 - 1, 2, 0, ENDIANNESS, "f")

    # TOTAL HARMONIC DISTORTION, CURRENT
    THD_CURRENT_A: RegisterModBus = RegisterModBus(21300 - 1, 2, 0, ENDIANNESS, "f")
    THD_CURRENT_B: RegisterModBus = RegisterModBus(21302 - 1, 2, 0, ENDIANNESS, "f")
    THD_CURRENT_C: RegisterModBus = RegisterModBus(21304 - 1, 2, 0, ENDIANNESS, "f")
    THD_CURRENT_N: RegisterModBus = RegisterModBus(21306 - 1, 2, 0, ENDIANNESS, "f")
    THD_CURRENT_G: RegisterModBus = RegisterModBus(21308 - 1, 2, 0, ENDIANNESS, "f")

    # TOTAL HARMONIC DISTORTION, VOLTAGE
    THD_VOLTAGE_AB: RegisterModBus = RegisterModBus(21322 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_BC: RegisterModBus = RegisterModBus(21324 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_CA: RegisterModBus = RegisterModBus(21326 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_LL: RegisterModBus = RegisterModBus(21328 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_AN: RegisterModBus = RegisterModBus(21330 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_BN: RegisterModBus = RegisterModBus(21332 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_CN: RegisterModBus = RegisterModBus(21334 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_NG: RegisterModBus = RegisterModBus(21336 - 1, 2, 0, ENDIANNESS, "f")
    THD_VOLTAGE_LN: RegisterModBus = RegisterModBus(21338 - 1, 2, 0, ENDIANNESS, "f")

    # TOTAL DEMAND DISTORTION
    TOTAL_DEMAND_DISTORTION: RegisterModBus = RegisterModBus(21320 - 1, 2, 0, ENDIANNESS, "f")

    # FRECUENCY
    FRECUENCY: RegisterModBus = RegisterModBus(3110 - 1, 2, 0, ENDIANNESS, "f")


@dataclass
class MedidorDeEnergia(ModbusDeviceBase):
    # PRESENT DATE & TIME
    date: datetime = field(init=False)

    # ACCUMULATED ENERGY - 32 BIT FLOATING POINT VALUES
    active_energy_delivered: float = field(init=False)
    active_energy_received: float = field(init=False)
    active_energy_delivered_more_received: float = field(init=False)
    active_energy_deliverd_less_received: float = field(init=False)
    reactive_energy_delivered: float = field(init=False)
    reactive_energy_received: float = field(init=False)
    reactive_energy_delivered_more_received: float = field(init=False)
    reactive_energy_delivered_less_received: float = field(init=False)
    apparent_energy_delivered: float = field(init=False)
    apparent_energy_received: float = field(init=False)
    apparent_energy_deliverd_more_received: float = field(init=False)
    apparent_energy_deliverd_less_received: float = field(init=False)

    # CURRENT
    current_a: float = field(init=False)
    current_b: float = field(init=False)
    current_c: float = field(init=False)
    current_n: float = field(init=False)
    current_g: float = field(init=False)
    current_avg: float = field(init=False)

    # CURRENT UNBALANCE
    current_unbalance_a: float = field(init=False)
    current_unbalance_b: float = field(init=False)
    current_unbalance_c: float = field(init=False)
    current_unbalance_worst: float = field(init=False)

    # VOLTAGE
    voltage_ab: float = field(init=False)
    voltage_bc: float = field(init=False)
    voltage_ca: float = field(init=False)
    voltage_ll_avg: float = field(init=False)
    voltage_an: float = field(init=False)
    voltage_bn: float = field(init=False)
    voltage_cn: float = field(init=False)
    voltage_ng: float = field(init=False)
    voltage_ln_avg: float = field(init=False)

    # VOLTAGE UNBALANCE
    voltage_unbalance_ab: float = field(init=False)
    voltage_unbalance_bc: float = field(init=False)
    voltage_unbalance_ca: float = field(init=False)
    voltage_unbalance_ll_worst: float = field(init=False)
    voltage_unbalance_an: float = field(init=False)
    voltage_unbalance_bn: float = field(init=False)
    voltage_unbalance_cn: float = field(init=False)
    voltage_unbalance_ln_worst: float = field(init=False)

    # POWER
    active_power_a: float = field(init=False)
    active_power_b: float = field(init=False)
    active_power_c: float = field(init=False)
    active_power_total: float = field(init=False)
    reactive_power_a: float = field(init=False)
    reactive_power_b: float = field(init=False)
    reactive_power_c: float = field(init=False)
    reactive_power_total: float = field(init=False)
    apparent_power_a: float = field(init=False)
    apparent_power_b: float = field(init=False)
    apparent_power_c: float = field(init=False)
    apparent_power_total: float = field(init=False)

    # POWER FACTOR
    power_factor_a: float = field(init=False)
    power_factor_b: float = field(init=False)
    power_factor_c: float = field(init=False)
    power_factor_total: float = field(init=False)
    displacement_power_factor_a: float = field(init=False)
    displacement_power_factor_b: float = field(init=False)
    displacement_power_factor_c: float = field(init=False)
    displacement_power_factor_total: float = field(init=False)

    # TOTAL HARMONIC DISTORTION, CURRENT
    thd_current_a: float = field(init=False)
    thd_current_b: float = field(init=False)
    thd_current_c: float = field(init=False)
    thd_current_n: float = field(init=False)
    thd_current_g: float = field(init=False)

    # TOTAL HARMONIC DISTORTION, VOLTAGE
    thd_voltage_ab: float = field(init=False)
    thd_voltage_bc: float = field(init=False)
    thd_voltage_ca: float = field(init=False)
    thd_voltage_ll: float = field(init=False)
    thd_voltage_an: float = field(init=False)
    thd_voltage_bn: float = field(init=False)
    thd_voltage_cn: float = field(init=False)
    thd_voltage_ng: float = field(init=False)
    thd_voltage_ln: float = field(init=False)

    # TOTAL DEMAND DISTORTION
    total_demand_distortion: float = field(init=False)

    # FRECUENCY
    frequency: float = field(init=False)

    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:
                    slave = self.address.slave

                    # # ACCUMULATED ENERGY - 32 BIT FLOATING POINT VALUES
                    self.active_energy_delivered = PM5100.ACTIVE_ENERGY_DELIVERED.get_value(client, slave)
                    # self.active_energy_received = PM5100.ACTIVE_ENERGY_RECEIVED.get_value(client, slave)
                    # self.active_energy_delivered_more_received = \
                    #     PM5100.ACTIVE_ENERGY_DELIVERED_MORE_RECEIVED.get_value(client, slave)
                    # self.active_energy_deliverd_less_received = \
                    #     PM5100.ACTIVE_ENERGY_DELIVERD_LESS_RECEIVED.get_value(client, slave)
                    # self.reactive_energy_delivered = PM5100.REACTIVE_ENERGY_DELIVERED.get_value(client, slave)
                    # self.reactive_energy_received = PM5100.REACTIVE_ENERGY_RECEIVED.get_value(client, slave)
                    # self.reactive_energy_delivered_more_received = \
                    #     PM5100.REACTIVE_ENERGY_DELIVERED_MORE_RECEIVED.get_value(client, slave)
                    # self.reactive_energy_delivered_less_received = \
                    #     PM5100.REACTIVE_ENERGY_DELIVERED_LESS_RECEIVED.get_value(client, slave)
                    # self.apparent_energy_delivered = PM5100.APPARENT_ENERGY_DELIVERED.get_value(client, slave)
                    # self.apparent_energy_received = PM5100.APPARENT_ENERGY_RECEIVED.get_value(client, slave)
                    # self.apparent_energy_deliverd_more_received = \
                    #     PM5100.APPARENT_ENERGY_DELIVERD_MORE_RECEIVED.get_value(client, slave)
                    # self.apparent_energy_deliverd_less_received = \
                    #     PM5100.APPARENT_ENERGY_DELIVERD_LESS_RECEIVED.get_value(client, slave)
                    #
                    # CURRENT
                    self.current_a = PM5100.CURRENT_A.get_value(client, slave)
                    self.current_b = PM5100.CURRENT_B.get_value(client, slave)
                    self.current_c = PM5100.CURRENT_C.get_value(client, slave)
                    # self.current_n = PM5100.CURRENT_N.get_value(client, slave)
                    # self.current_g = PM5100.CURRENT_G.get_value(client, slave)
                    # self.current_avg = PM5100.CURRENT_AVG.get_value(client, slave)

                    # # CURRENT UNBALANCE
                    # self.current_unbalance_a = PM5100.CURRENT_UNBALANCE_A.get_value(client, slave)
                    # self.current_unbalance_b = PM5100.CURRENT_UNBALANCE_B.get_value(client, slave)
                    # self.current_unbalance_c = PM5100.CURRENT_UNBALANCE_C.get_value(client, slave)
                    # self.current_unbalance_worst = PM5100.CURRENT_UNBALANCE_WORST.get_value(client, slave)
                    #
                    # # VOLTAGE
                    self.voltage_ab = PM5100.VOLTAGE_AB.get_value(client, slave)
                    self.voltage_bc = PM5100.VOLTAGE_BC.get_value(client, slave)
                    self.voltage_ca = PM5100.VOLTAGE_CA.get_value(client, slave)
                    # self.voltage_ll_avg = PM5100.VOLTAGE_LL_AVG.get_value(client, slave)
                    # self.voltage_an = PM5100.VOLTAGE_AN.get_value(client, slave)
                    # self.voltage_bn = PM5100.VOLTAGE_BN.get_value(client, slave)
                    # self.voltage_cn = PM5100.VOLTAGE_CN.get_value(client, slave)
                    # self.voltage_ng = PM5100.VOLTAGE_NG.get_value(client, slave)
                    # self.voltage_ln_avg = PM5100.VOLTAGE_LN_AVG.get_value(client, slave)
                    #
                    # # VOLTAGE UNBALANCE
                    # self.voltage_unbalance_ab = PM5100.VOLTAGE_UNBALANCE_AB.get_value(client, slave)
                    # self.voltage_unbalance_bc = PM5100.VOLTAGE_UNBALANCE_BC.get_value(client, slave)
                    # self.voltage_unbalance_ca = PM5100.VOLTAGE_UNBALANCE_CA.get_value(client, slave)
                    # self.voltage_unbalance_ll_worst = PM5100.VOLTAGE_UNBALANCE_LL_WORST.get_value(client, slave)
                    # self.voltage_unbalance_an = PM5100.VOLTAGE_UNBALANCE_AN.get_value(client, slave)
                    # self.voltage_unbalance_bn = PM5100.VOLTAGE_UNBALANCE_BN.get_value(client, slave)
                    # self.voltage_unbalance_cn = PM5100.VOLTAGE_UNBALANCE_CN.get_value(client, slave)
                    # self.voltage_unbalance_ln_worst = PM5100.VOLTAGE_UNBALANCE_LN_WORST.get_value(client, slave)
                    #
                    # # POWER
                    self.active_power_a = PM5100.ACTIVE_POWER_A.get_value(client, slave)
                    self.active_power_b = PM5100.ACTIVE_POWER_B.get_value(client, slave)
                    self.active_power_c = PM5100.ACTIVE_POWER_C.get_value(client, slave)
                    # self.active_power_total = PM5100.ACTIVE_POWER_TOTAL.get_value(client, slave)
                    # self.reactive_power_a = PM5100.REACTIVE_POWER_A.get_value(client, slave)
                    # self.reactive_power_b = PM5100.REACTIVE_POWER_B.get_value(client, slave)
                    # self.reactive_power_c = PM5100.REACTIVE_POWER_C.get_value(client, slave)
                    # self.reactive_power_total = PM5100.REACTIVE_POWER_TOTAL.get_value(client, slave)
                    # self.apparent_power_a = PM5100.APPARENT_POWER_A.get_value(client, slave)
                    # self.apparent_power_b = PM5100.APPARENT_POWER_B.get_value(client, slave)
                    # self.apparent_power_c = PM5100.APPARENT_POWER_C.get_value(client, slave)
                    # self.apparent_power_total = PM5100.APPARENT_POWER_TOTAL.get_value(client, slave)
                    #
                    # # POWER FACTOR
                    # self.power_factor_a = PM5100.POWER_FACTOR_A.get_value(client, slave)
                    # self.power_factor_b = PM5100.POWER_FACTOR_B.get_value(client, slave)
                    # self.power_factor_c = PM5100.POWER_FACTOR_C.get_value(client, slave)
                    # self.power_factor_total = PM5100.POWER_FACTOR_TOTAL.get_value(client, slave)
                    # self.displacement_power_factor_a = PM5100.DISPLACEMENT_POWER_FACTOR_A.get_value(client, slave)
                    # self.displacement_power_factor_b = PM5100.DISPLACEMENT_POWER_FACTOR_B.get_value(client, slave)
                    # self.displacement_power_factor_c = PM5100.DISPLACEMENT_POWER_FACTOR_C.get_value(client, slave)
                    # self.displacement_power_factor_total = \
                    #     PM5100.DISPLACEMENT_POWER_FACTOR_TOTAL.get_value(client, slave)
                    #
                    # # TOTAL HARMONIC DISTORTION, CURRENT
                    # self.thd_current_a = PM5100.THD_CURRENT_A.get_value(client, slave)
                    # self.thd_current_b = PM5100.THD_CURRENT_B.get_value(client, slave)
                    # self.thd_current_c = PM5100.THD_CURRENT_C.get_value(client, slave)
                    # self.thd_current_n = PM5100.THD_CURRENT_N.get_value(client, slave)
                    # self.thd_current_g = PM5100.THD_CURRENT_G.get_value(client, slave)
                    #
                    # # TOTAL HARMONIC DISTORTION, VOLTAGE
                    # self.thd_voltage_ab = PM5100.THD_VOLTAGE_AB.get_value(client, slave)
                    # self.thd_voltage_bc = PM5100.THD_VOLTAGE_BC.get_value(client, slave)
                    # self.thd_voltage_ca = PM5100.THD_VOLTAGE_CA.get_value(client, slave)
                    # self.thd_voltage_ll = PM5100.THD_VOLTAGE_LL.get_value(client, slave)
                    # self.thd_voltage_an = PM5100.THD_VOLTAGE_AN.get_value(client, slave)
                    # self.thd_voltage_bn = PM5100.THD_VOLTAGE_BN.get_value(client, slave)
                    # self.thd_voltage_cn = PM5100.THD_VOLTAGE_CN.get_value(client, slave)
                    # self.thd_voltage_ng = PM5100.THD_VOLTAGE_NG.get_value(client, slave)
                    # self.thd_voltage_ln = PM5100.THD_VOLTAGE_LN.get_value(client, slave)
                    #
                    # # TOTAL DEMAND DISTORTION
                    # self.total_demand_distortion = PM5100.TOTAL_DEMAND_DISTORTION.get_value(client, slave)
                    #
                    # # FRECUENCY
                    # self.frequency = PM5100.FRECUENCY.get_value(client, slave)
                    #







                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
