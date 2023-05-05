import time, traceback

from bsp.common.Config import Config

from bsp.v3.modbus_generic import RegisterModBus, RegistersModbus, get_value, ModbusDeviceBase

from dataclasses import dataclass, field, InitVar

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

@dataclass
class SampleRaw:
    data: InitVar[list]

    MEASURED_VALUE: float = field(init=False)
    PARAMETER_ID: int = field(init=False)
    UNIT_ID: int = field(init=False)
    DATA_QUALITY_ID: int = field(init=False)
    SENTINEL_VALUE: float = field(init=False)
    AVAILABLE_UNITS: int = field(init=False)

    def __post_init__(self, data: list):
        if len(data) < 8:
            return

        self.MEASURED_VALUE = get_value(data[:2], 2, 0, ENDIANNESS, "f")
        self.PARAMETER_ID = get_value(data[2:3], 1, 0, ENDIANNESS, "H")
        self.UNIT_ID = get_value(data[3:4], 1, 0, ENDIANNESS, "H")
        self.SENTINEL_VALUE = get_value(data[4:6], 2, 0, ENDIANNESS, "f")
        self.AVAILABLE_UNITS = get_value(data[7:8], 1, 0, ENDIANNESS, "H")


@dataclass
class Sample:
    data: InitVar[list]

    DO_CONCENTRATION: SampleRaw = field(init=False)
    TEMPERATURE: SampleRaw = field(init=False)
    DO_SATURATION: SampleRaw = field(init=False)
    OXYGEN_PARTIAL_PRESSURE: SampleRaw = field(init=False)

    def __post_init__(self, data: list):
        if len(data) < 8 * 4:
            return

        self.DO_CONCENTRATION = SampleRaw(data[:8])
        self.TEMPERATURE = SampleRaw(data[8:16])
        self.DO_SATURATION = SampleRaw(data[16:24])
        self.OXYGEN_PARTIAL_PRESSURE = SampleRaw(data[24:32])


@dataclass
class RDOBLUE:
    SERIAL_NUMBER: RegisterModBus = RegisterModBus(2 - 1, 2, 0, ENDIANNESS, "I")

    # SAMPLE
    # check page 56 n-Situ Modbus Communication Protocol Version 5.10
    SAMPLE: RegistersModbus = RegistersModbus(38 - 1, 0x20)


@dataclass
class SensorOxigenometro(ModbusDeviceBase):
    serial_number: int = field(init=False)
    sample: Sample = field(init=False)


    def __post_init__(self):
        retry = Config.RETRY
        while retry > 0:
            try:
                with self.get_client() as client:

                    slave = self.address.slave

                    self.serial_number = RDOBLUE.SERIAL_NUMBER.get_value(client, slave)

                    # read twice samples, because the datasheet
                    try:
                        RDOBLUE.SAMPLE.get_registers(client, slave)
                    except Exception as e:
                        pass
                    sample_registers = RDOBLUE.SAMPLE.get_registers(client, slave)

                    self.sample = Sample(sample_registers)

                    self.status = "OK"
                    return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
