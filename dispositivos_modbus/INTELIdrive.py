import time, traceback

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


ENDIANESS = ">"


@dataclass
class INTELIdrive: 
    MODBUS_OFFSET = 40001

    RPM: RegisterModBus = RegisterModBus(40011 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    SPEEDREQ_ABS: RegisterModBus = RegisterModBus(40211 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    RUN_HRS: RegisterModBus = RegisterModBus(43001 - MODBUS_OFFSET, 2, 1, ENDIANESS, "i")
    NUM_STARTS: RegisterModBus = RegisterModBus(43005 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    UBAT: RegisterModBus = RegisterModBus(40051 - MODBUS_OFFSET, 1, 1, ENDIANESS, "h")
    ENG_TEMP: RegisterModBus = RegisterModBus(40055 - MODBUS_OFFSET, 1, 0, ENDIANESS, "h")
    OIL_PRESS: RegisterModBus = RegisterModBus(40054 - MODBUS_OFFSET, 1, 0, ENDIANESS, "h")

    ENGINE_STATE: RegisterModBus = RegisterModBus(40072 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    CONTROLLER_MODE: RegisterModBus = RegisterModBus(43143 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")

    BIN: RegisterModBus = RegisterModBus(40062 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")
    BOUT: RegisterModBus = RegisterModBus(40063 - MODBUS_OFFSET, 1, 0, ENDIANESS, "H")


@dataclass
class EngineState:
    value: int
    status: str = field(init=False)

    def __post_init__(self):
        state_lst = [
            "Init",
            "Not ready",
            "Prestart",
            "Cranking",
            "Pause",
            "Starting",
            "Running",
            "Loaded",
            "Stop",
            "Shutdown",
            "Ready",
            "Cooling",
            "EmergMan",
            "MainsOper",
            "MainsFlt",
            "ValidFlt",
            "IslOper",
            "MainsRet",
            "Brks Off",
            "No Timer",
            "MCB close",
            "RetTransf",
            "FwRet Brk",
            "Idle Run",
            "MinStabTO",
            "MaxStabTO",
            "AfterCool",
            "GCB open",
            "StopValve",
            "(1Ph)",
            "(3PD)",
            "(3PY)",
            "Run Timer",
            "SdVentil",
            "Ventil",
            "Idle"
        ]

        if 0 <= self.value - 23 < len(state_lst):
            self.status = state_lst[self.value]
        else:
            self.status = "unknown"


@dataclass
class ControllerMode:
    value: int
    status: str = field(init=False)

    def __post_init__(self):
        state_lst = [
            "OFF",
            "MAN",
            "AUT"
        ]

        if self.value < len(state_lst):
            self.status = state_lst[self.value]
        else:
            self.status = "unknown"


@dataclass
class BINTable:
    value: int

    emergency_stop: bool = field(init=False)
    rem_start_stop: bool = field(init=False)
    access_lock: bool = field(init=False)
    remote_off: bool = field(init=False)

    def __post_init__(self):
        self.emergency_stop = (self.value & 0x01) == 1
        self.rem_start_stop = ((self.value & 0x02)>>1) == 1
        self.access_lock = ((self.value & 0x04)>>2) == 1
        self.remote_off = ((self.value & 0x08)>>3) == 1


@dataclass
class BOUTTable:
    value: int

    starter: bool = field(init=False)
    fuel_solenoid: bool = field(init=False)
    access_lock: bool = field(init=False)
    prestart: bool = field(init=False)
    alarm: bool = field(init=False)

    def __post_init__(self):
        self.starter = (self.value & 0x01) == 1
        self.fuel_solenoid = ((self.value & 0x02)>>1) == 1
        self.access_lock = ((self.value & 0x04)>>2) == 1
        self.prestart = ((self.value & 0x08)>>3) == 1
        self.alarm = ((self.value & 0x10)>>4) == 1


@dataclass
class ReglasAlarmas:
    low_eng_temp: int
    high_eng_temp: int

    low_oil_press: int

    low_rpm: int
    high_rpm: int

    low_ubat_NT_KT: int
    high_ubat_NT_KT: int

    low_ubat_6C: int
    high_ubat_6C: int

    slow_rpm_value: int
    slow_rpm_minutes: int


@dataclass
class Alarmas:
    low_eng_temp: bool = False
    high_eng_temp: bool = False

    low_oil_press: bool = False

    low_rpm: bool = False
    high_rpm: bool = False

    low_ubat: bool = False
    high_ubat: bool = False

    slow_rpm: bool = False


@dataclass
class Identificacion:
    id_equipo: str
    tipo_motor: str
    serie_equipo: str


@dataclass
class ControlBomba(ModbusDeviceBase):
    id: Union[Identificacion, None]
    reglas_alarma: Union[ReglasAlarmas, None] = field(repr=False)

    rpm: int = field(init=False)
    speedreq_abs: int = field(init=False)
    run_hrs: float = field(init=False)
    num_starts: int = field(init=False)
    ubat: float = field(init=False)
    eng_temp: int = field(init=False)
    oil_press: int = field(init=False)

    engine_state: EngineState = field(init=False)
    controller_mode: ControllerMode = field(init=False)

    bin: BINTable = field(init=False)
    bout: BOUTTable = field(init=False)

    alarmas: Alarmas = field(init=False)

    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                # modbus client tcp
                with self.get_client() as client:

                    slave = self.address.slave

                    # REGISTER MAINS

                    self.rpm = INTELIdrive.RPM.get_value(client, slave)
                    self.speedreq_abs = INTELIdrive.SPEEDREQ_ABS.get_value(client, slave)
                    self.run_hrs = INTELIdrive.RUN_HRS.get_value(client, slave)
                    self.num_starts = INTELIdrive.NUM_STARTS.get_value(client, slave)
                    self.ubat = INTELIdrive.UBAT.get_value(client, slave)
                    self.eng_temp = INTELIdrive.ENG_TEMP.get_value(client, slave)
                    self.oil_press = INTELIdrive.OIL_PRESS.get_value(client, slave)

                    engine_state = INTELIdrive.ENGINE_STATE.get_value(client, slave)
                    self.engine_state = EngineState(engine_state)

                    controller_mode = INTELIdrive.CONTROLLER_MODE.get_value(client, slave) & 0xFF
                    self.controller_mode = ControllerMode(controller_mode)

                    bin = INTELIdrive.BIN.get_value(client, slave) & 0xFF
                    self.bin = BINTable(bin)

                    bout = INTELIdrive.BOUT.get_value(client, slave) & 0xFF
                    self.bout = BOUTTable(bout)

                    if type(self.reglas_alarma) is ReglasAlarmas:
                        self.alarmas = Alarmas()

                        self.alarmas.low_eng_temp = self.eng_temp < self.reglas_alarma.low_eng_temp
                        self.alarmas.high_eng_temp = self.eng_temp > self.reglas_alarma.high_eng_temp
                        self.alarmas.low_oil_press = self.oil_press < self.reglas_alarma.low_oil_press
                        self.alarmas.low_rpm = self.rpm < self.reglas_alarma.low_rpm
                        self.alarmas.high_rpm = self.rpm > self.reglas_alarma.high_rpm

                        if type(self.id) is Identificacion:
                            if self.id.tipo_motor[:2] in ['NT', 'KT']:
                                self.alarmas.low_ubat = self.ubat < self.reglas_alarma.low_ubat_NT_KT
                                self.alarmas.high_ubat = self.ubat > self.reglas_alarma.high_ubat_NT_KT

                            elif self.id.tipo_motor[:2] in ['6C']:
                                self.alarmas.low_ubat = self.ubat < self.reglas_alarma.low_ubat_6C
                                self.alarmas.high_ubat = self.ubat > self.reglas_alarma.high_ubat_6C

                            else:
                                print('Error, motor desconocido')
                                exit()

                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
