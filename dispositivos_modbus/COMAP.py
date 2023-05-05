import time, traceback

from bsp.common.Config import Config

from bsp.v3.modbus_generic import RegisterModBus, ModbusDeviceBase

from dataclasses import dataclass, field, InitVar

from typing import Union

# Endianess
# >         big endian
# <         little endian

# Format    C Type	Standard	size
# c			char				1
# b			signed char			1
# B			unsigned char		1
# ?			_Bool				1
# h			short				2
# H			unsigned short		2
# i			int					4
# I			unsigned int		4
# l			long				4
# L			unsigned long		4
# q			long  long			8
# Q			unsigned long long	8
# f			float   			4
# d			double				8


ENDIANESS = ">"


@dataclass
class COMAP:
    MODBUS_OFFSET: int = 40001

    # REGISTER MAINS
    UBAT: RegisterModBus = RegisterModBus(40013 - MODBUS_OFFSET, 1, 1, ENDIANESS, "h")
    CPU_TEMP: RegisterModBus = RegisterModBus(40014 - MODBUS_OFFSET, 1, 1, ENDIANESS, "h")
    MAINS_V_L1_N: RegisterModBus = RegisterModBus(40217 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_V_L2_N: RegisterModBus = RegisterModBus(40218 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_V_L3_N: RegisterModBus = RegisterModBus(40219 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_V_L1_L2: RegisterModBus = RegisterModBus(40221 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_V_L2_L3: RegisterModBus = RegisterModBus(40222 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_V_L3_L1: RegisterModBus = RegisterModBus(40223 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_FREQ: RegisterModBus = RegisterModBus(40224 - MODBUS_OFFSET, 1, 1, ENDIANESS, "H")
    MAINS_CURR_L1: RegisterModBus = RegisterModBus(40226 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_CURR_L2: RegisterModBus = RegisterModBus(40227 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    MAINS_CURR_L3: RegisterModBus = RegisterModBus(40228 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    # OBJECT_PQFP: int = 40273 - BASE

    # GENERATOR
    BUS_V_L1_N: RegisterModBus = RegisterModBus(40256 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    BUS_V_L2_N: RegisterModBus = RegisterModBus(40257 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    BUS_V_L3_N: RegisterModBus = RegisterModBus(40258 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    BUS_V_L1_L2: RegisterModBus = RegisterModBus(40260 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    BUS_V_L2_L3: RegisterModBus = RegisterModBus(40261 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    BUS_V_L3_L1: RegisterModBus = RegisterModBus(40262 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")

    BREAKER_STATE: RegisterModBus = RegisterModBus(40137 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")

    COMAP_STATUS: RegisterModBus = RegisterModBus(40146 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")


@dataclass
class ComapStatus:
    stream: InitVar[int]

    mgcb_closed: int = 0
    mcb_closed: int = 0
    btb_appl: int = 0
    intelimains: int = 0

    def __post_init__(self, stream: int):
        self.mgcb_closed = (stream >> 1) & 1
        self.mcb_closed = (stream >> 2) & 1
        self.btb_appl = (stream >> 3) & 1
        self.intelimains = (stream >> 5) & 1


@dataclass
class BreakerState:
    value: int
    status: str = field(init=False)

    def __post_init__(self):
        state_lst = [
            "Init",
            "BrksOff",
            "IslOper",
            "MainsOper",
            "ParalOper",
            "RevSync",
            "Synchro",
            "MainsFlt",
            "MainsRet",
            "ValidFlt",
            "MCB Off",
            "BTB off",
            "BTB on",
            "EmergMan",
            "LCB off",
            "LCB on",
        ]

        if self.value < len(state_lst):
            self.status = state_lst[self.value]
        else:
            self.status = "Unknown"


@dataclass
class ControladoDeGeneracion(ModbusDeviceBase):
    is_master: InitVar[bool]

    # REGISTER MAINS
    ubat: float = field(init=False)
    cpu_temp: float = field(init=False)

    mains_v_l1_n: float = field(init=False)
    mains_v_l2_n: float = field(init=False)
    mains_v_l3_n: float = field(init=False)

    mains_v_l1_l2: float = field(init=False)
    mains_v_l2_l3: float = field(init=False)
    mains_v_l3_l1: float = field(init=False)

    mains_freq: float = field(init=False)

    mains_curr_l1: float = field(init=False)
    mains_curr_l2: float = field(init=False)
    mains_curr_l3: float = field(init=False)

    # GENERATOR
    bus_v_l1_n: float = field(init=False)
    bus_v_l2_n: float = field(init=False)
    bus_v_l3_n: float = field(init=False)

    bus_v_l1_l2: float = field(init=False)
    bus_v_l2_l3: float = field(init=False)
    bus_v_l3_l1: float = field(init=False)

    breaker_state: BreakerState = field(init=False)

    comap_status: ComapStatus = field(init=False)

    def __post_init__(self, is_master: bool):
        retry = Config.RETRY
        while retry > 0:
            try:
                # modbus client tcp
                with self.get_client() as client:

                    slave = self.address.slave

                    # REGISTER MAINS

                    self.ubat = COMAP.UBAT.get_value(client, slave)
                    self.cpu_temp = COMAP.CPU_TEMP.get_value(client, slave)

                    self.mains_v_l1_n = COMAP.MAINS_V_L1_N.get_value(client, slave)
                    self.mains_v_l2_n = COMAP.MAINS_V_L2_N.get_value(client, slave)
                    self.mains_v_l3_n = COMAP.MAINS_V_L3_N.get_value(client, slave)

                    self.mains_v_l1_l2 = COMAP.MAINS_V_L1_L2.get_value(client, slave)
                    self.mains_v_l2_l3 = COMAP.MAINS_V_L2_L3.get_value(client, slave)
                    self.mains_v_l3_l1 = COMAP.MAINS_V_L3_L1.get_value(client, slave)

                    self.mains_freq = COMAP.MAINS_FREQ.get_value(client, slave)

                    self.mains_curr_l1 = COMAP.MAINS_CURR_L1.get_value(client, slave)
                    self.mains_curr_l2 = COMAP.MAINS_CURR_L2.get_value(client, slave)
                    self.mains_curr_l3 = COMAP.MAINS_CURR_L3.get_value(client, slave)

                    # GENERATOR
                    self.bus_v_l1_n = COMAP.BUS_V_L1_N.get_value(client, slave)
                    self.bus_v_l2_n = COMAP.BUS_V_L2_N.get_value(client, slave)
                    self.bus_v_l3_n = COMAP.BUS_V_L3_N.get_value(client, slave)

                    self.bus_v_l1_l2 = COMAP.BUS_V_L1_L2.get_value(client, slave)
                    self.bus_v_l2_l3 = COMAP.BUS_V_L2_L3.get_value(client, slave)
                    self.bus_v_l3_l1 = COMAP.BUS_V_L3_L1.get_value(client, slave)

                    breaker_state = COMAP.BREAKER_STATE.get_value(client, slave)
                    self.breaker_state = BreakerState(breaker_state)

                    if is_master:
                        comap_status_code = COMAP.COMAP_STATUS.get_value(client, slave)
                        self.comap_status = ComapStatus(comap_status_code)

                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
