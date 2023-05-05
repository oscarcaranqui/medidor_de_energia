import time, traceback

from bsp.common.Config import Config

from bsp.v3.modbus_generic import RegisterModBus, ModbusDeviceBase

from dataclasses import dataclass, field

from typing import Union

# Endianess
# >			big endian
# <			little endian

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

ENDIANNESS = ">"

# note:
# only function 03 and 06 are allowed
# 03 read multiple registers
# 06 write multiple registers
@dataclass
class DSEcontroler:
    OFFSET_GENERATING_SET_STATUS_INFORMATION = 3 * 256

    MODO: RegisterModBus = RegisterModBus(OFFSET_GENERATING_SET_STATUS_INFORMATION + 4, 1, 0, ENDIANNESS, "H")

    OFFSET_BASIC_INSTRUMENTATION = 4 * 256

    OIL_PRESSURE: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 0, 1, 0, ENDIANNESS, "H")
    COOLANT_TEMPERATURE: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 1, 1, 0, ENDIANNESS, "H")
    OIL_TEMPERATURE: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 2, 1, 0, ENDIANNESS, "H")
    FUEL_LEVEL: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 3, 1, 0, ENDIANNESS, "H")
    CHARGE_ALTERNATOR_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 4, 1, 1, ENDIANNESS, "H")
    ENGINE_BATTERY_VOLTAGE: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 5, 1, 1, ENDIANNESS, "H")
    ENGINE_SPEED: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 6, 1, 0, ENDIANNESS, "H")
    GENERATOR_FREQUENCY: RegisterModBus = RegisterModBus(OFFSET_BASIC_INSTRUMENTATION + 7, 1, 1, ENDIANNESS, "H")

    OFFSET_EXTENDED_INSTRUMENTATION = 5 * 256

    ENGINE_STATE: RegisterModBus = RegisterModBus(OFFSET_EXTENDED_INSTRUMENTATION + 128, 1, 0, ENDIANNESS, "H")

    OFFSET_ACCUMULATED_INSTRUMENTATION = 7 * 256

    RUN_HRS: RegisterModBus = RegisterModBus(OFFSET_ACCUMULATED_INSTRUMENTATION + 6, 2, 0, ENDIANNESS, "i")


@dataclass
class ControllerMode:
    value: int
    status: str = field(init=False)

    def __post_init__(self):
        modes = [
            "Stop mode",
            "Auto mode",
            "Manual mode",
            "Test on load mode",
            "Auto with manual restore mode/Prohibit Return",
            "User configuration mode",
            "Test off load mode",
            "Off Mode",
        ]

        if self.value > len(modes) or self.value < 0:
            self.status = 'unknown'
        else:
            self.status = modes[self.value]


@dataclass
class EngineOperatingState:
    value: int
    status: str = field(init=False)

    def __post_init__(self):
        modes = [
            "Engine stopped",
            "Pre-Start",
            "Warning up",
            "Running",
            "Cooling down",
            "Engine Stopped",
            ""
        ] + ["Available for SAE assignment"] * 6 + [
            "Reserved",
            "Not available"
        ]

        if self.value > len(modes) or self.value < 0:
            self.status = 'unknown'
        else:
            self.status = modes[self.value]


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

    mode: ControllerMode = field(init=False)
    engine_state: EngineOperatingState = field(init=False)
    run_hrs: int = field(init=False)
    oil_pressure: int = field(init=False)
    coolant_temperature: int = field(init=False)
    oil_temperature: int = field(init=False)
    fuel_level: int = field(init=False)
    charge_alternator_voltage: float = field(init=False)
    engine_battery_voltage: float = field(init=False)
    engine_speed: int = field(init=False)
    generator_frequency: float = field(init=False)

    alarmas: Alarmas = field(init=False)

    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:

                    slave = self.address.slave

                    mode = DSEcontroler.MODO.get_value(client, slave)
                    self.mode = ControllerMode(mode)

                    engine_state = DSEcontroler.ENGINE_STATE.get_value(client, slave)
                    self.engine_state = EngineOperatingState(engine_state)

                    self.run_hrs = DSEcontroler.RUN_HRS.get_value(client, slave)
                    self.oil_pressure = DSEcontroler.OIL_PRESSURE.get_value(client, slave)
                    self.coolant_temperature = DSEcontroler.COOLANT_TEMPERATURE.get_value(client, slave)
                    self.oil_temperature = DSEcontroler.OIL_TEMPERATURE.get_value(client, slave)
                    self.fuel_level = DSEcontroler.FUEL_LEVEL.get_value(client, slave)
                    self.charge_alternator_voltage = DSEcontroler.CHARGE_ALTERNATOR_VOLTAGE.get_value(client, slave)
                    self.engine_battery_voltage = DSEcontroler.ENGINE_BATTERY_VOLTAGE.get_value(client, slave)
                    self.engine_speed = DSEcontroler.ENGINE_SPEED.get_value(client, slave)
                    self.generator_frequency = DSEcontroler.GENERATOR_FREQUENCY.get_value(client, slave)

                    if type(self.reglas_alarma) is ReglasAlarmas:
                        self.alarmas = Alarmas()

                        self.alarmas.low_eng_temp = self.coolant_temperature < self.reglas_alarma.low_eng_temp
                        self.alarmas.high_eng_temp = self.coolant_temperature > self.reglas_alarma.high_eng_temp
                        self.alarmas.low_oil_press = self.oil_pressure < self.reglas_alarma.low_oil_press
                        self.alarmas.low_rpm = self.engine_speed < self.reglas_alarma.low_rpm
                        self.alarmas.high_rpm = self.engine_speed > self.reglas_alarma.high_rpm

                        if type(self.id) is Identificacion:
                            if self.id.tipo_motor[:2] in ['NT', 'KT']:
                                self.alarmas.low_ubat = self.engine_battery_voltage < self.reglas_alarma.low_ubat_NT_KT
                                self.alarmas.high_ubat = self.engine_battery_voltage > self.reglas_alarma.high_ubat_NT_KT

                            elif self.id.tipo_motor[:2] in ['6C']:
                                self.alarmas.low_ubat = self.engine_battery_voltage < self.reglas_alarma.low_ubat_6C
                                self.alarmas.high_ubat = self.engine_battery_voltage > self.reglas_alarma.high_ubat_6C

                            else:
                                print('Error, motor desconocido')
                                exit()

                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
