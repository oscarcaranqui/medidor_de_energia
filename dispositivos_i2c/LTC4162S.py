
from dataclasses import dataclass, fields, field

from bsp.v3.i2c_generic import AddressI2C, BitRegister, RegisterVAL, RegisterREG


@dataclass
class LSBSize:
    RSNB_ohm: float = 0.01
    RSNI_ohm: float = 0.01

    vbat_V: float = 0.0003848
    vin_V: float = 0.001649
    vout_V: float = 0.001653
    iin_A: float = 0.000001466 / RSNI_ohm
    ibat_A: float = 0.000001466 / RSNB_ohm
    die_temp_C: float = 0.0215
    offset_die_temp_C: float = 264.4
    bsr: float = RSNB_ohm / 250
    # thermistor_voltage_uV: float = 45.833

    @staticmethod
    def get_vbat(raw: int, cell_opt: int) -> float:
        return round(raw * LSBSize.vbat_V * cell_opt, 3)

    @staticmethod
    def get_vin(raw: int, cell_opt: int) -> float:
        return round(raw * LSBSize.vin_V, 3)

    @staticmethod
    def get_vout(raw: int, cell_opt: int) -> float:
        return round(raw * LSBSize.vout_V, 3)

    @staticmethod
    def get_ibat(raw: int, cell_opt: int) -> float:
        return round(raw * LSBSize.ibat_A, 3)

    @staticmethod
    def get_iin(raw: int, cell_opt: int) -> float:
        return round(raw * LSBSize.iin_A, 3)

    @staticmethod
    def get_die_temp(raw: int, cell_opt: int) -> float:
        return round(raw * LSBSize.die_temp_C - LSBSize.offset_die_temp_C, 3)

    @staticmethod
    def get_bsr(raw: int, cell_opt: int) -> float:
        return round(cell_opt * raw * LSBSize.RSNB_ohm * LSBSize.bsr, 3)

    #-----------------------------------------------------------------------

    @staticmethod
    def get_iin_lim_target(raw: int, cell_opt: int) -> float:
        return round((raw + 1) * 0.0005 / LSBSize.RSNI_ohm, 3)

    @staticmethod
    def get_input_undervoltage_setting(raw: int, cell_opt: int) -> float:
        return round((raw + 1) * 0.140625, 3)

    @staticmethod
    def get_icharge_setting(raw: int, cell_opt: int) -> float:
        return round((raw + 1) * 0.001 / LSBSize.RSNB_ohm, 3)

    @staticmethod
    def get_vcharge_setting(raw: int, cell_opt: int) -> float:
        return round(cell_opt * (raw * 0.028571 + 6), 3)


@dataclass
class BR_EN_LIMIT_ALERTS_REG(BitRegister):
    en_telemetry_valid_alert: bool = field(init=False)
    en_bsr_done_alert: bool = field(init=False)
    en_vbat_lo_alert: bool = field(init=False)
    en_vbat_hi_alert: bool = field(init=False)
    en_vin_lo_alert: bool = field(init=False)
    en_vin_hi_alert: bool = field(init=False)
    en_vout_lo_alert: bool = field(init=False)
    en_vout_hi_alert: bool = field(init=False)
    en_iin_hi_alert: bool = field(init=False)
    en_ibat_lo_alert: bool = field(init=False)
    en_die_temp_hi_alert: bool = field(init=False)
    en_bsr_hi_alert: bool = field(init=False)
    en_thermistor_voltage_hi_alert: bool = field(init=False)
    en_thermistor_voltage_lo_alert: bool = field(init=False)

    def __post_init__(self, raw_value: int):
        bw = 15
        for dc_field in fields(self):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)

            if bw == 14:
                bw = 11
            else:
                bw -= 1


@dataclass
class BR_EN_CHARGER_STATE_ALERTS_REG(BitRegister):
    en_bat_detect_failed_fault_alert: bool = field(init=False)
    en_battery_detection_alert: bool = field(init=False)
    en_equalize_charge_alert: bool = field(init=False)
    en_absorb_charge_alert: bool = field(init=False)
    en_charger_suspended_alert: bool = field(init=False)
    en_cc_cv_charge_alert: bool = field(init=False)
    en_bat_missing_fault_alert: bool = field(init=False)
    en_bat_short_fault_alert: bool = field(init=False)

    def __post_init__(self, raw_value: int):
        bw = [12, 11, 10, 9, 8, 6, 1, 0]
        for idx, dc_field in enumerate(fields(self)):
            setattr(self, dc_field.name, ((raw_value >> bw[idx]) & 1) == 1)


@dataclass
class BR_EN_CHARGE_STATUS_ALERTS_REG(BitRegister):
    en_ilim_reg_active_alert: bool = field(init=False)
    en_thermal_reg_active_alert: bool = field(init=False)
    en_vin_uvcl_active_alert: bool = field(init=False)
    en_iin_limit_active_alert: bool = field(init=False)
    en_constant_current_alert: bool = field(init=False)
    en_constant_voltage_alert: bool = field(init=False)

    def __post_init__(self, raw_value: int):
        bw = 5
        for idx, dc_field in enumerate(fields(self)):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)
            bw -= 1


@dataclass
class BR_CONFIG_BITS_REG(BitRegister):
    suspend_charger: bool = field(init=False)
    run_bsr: bool = field(init=False)
    telemetry_speed: bool = field(init=False)
    force_telemetry_on: bool = field(init=False)
    mppt_en: bool = field(init=False)
    equalize_req: bool = field(init=False)

    def __post_init__(self, raw_value):
        bw = 5
        for idx, dc_field in enumerate(fields(self)):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)
            bw -= 1


@dataclass
class BR_LIMIT_ALERTS_REG(BitRegister):
    telemetry_valid_alert: bool = field(init=False)
    bsr_done_alert: bool = field(init=False)
    vbat_lo_alert: bool = field(init=False)
    vbat_hi_alert: bool = field(init=False)
    vin_lo_alert: bool = field(init=False)
    vin_hi_alert: bool = field(init=False)
    vout_lo_alert: bool = field(init=False)
    vout_hi_alert: bool = field(init=False)
    iin_hi_alert: bool = field(init=False)
    ibat_lo_alert: bool = field(init=False)
    die_temp_hi_alert: bool = field(init=False)
    bsr_hi_alert: bool = field(init=False)
    thermistor_voltage_hi_alert: bool = field(init=False)
    thermistor_voltage_lo_alert: bool = field(init=False)

    def __post_init__(self, raw_value):
        bw = 15
        for dc_field in fields(self):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)

            if bw == 14:
                bw = 11
            else:
                bw -= 1


@dataclass
class BR_CHARGER_STATE_ALERTS_REG(BitRegister):
    bat_detect_failed_fault_alert: bool = field(init=False)
    battery_detection_alert: bool = field(init=False)
    equalization_charge_alert: bool = field(init=False)
    absorb_charge_alert: bool = field(init=False)
    charger_suspended_alert: bool = field(init=False)
    cc_cv_charge_alert: bool = field(init=False)
    bat_missing_fault_alert: bool = field(init=False)
    bat_short_fault_alert: bool = field(init=False)

    def __post_init__(self, raw_value):
        bw = 12
        for dc_field in fields(self):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)

            if bw == 8:
                bw = 6
            elif bw == 6:
                bw = 1
            else:
                bw -= 1


@dataclass
class BR_CHARGE_STATUS_ALERTS_REG(BitRegister):
    ilim_reg_active_alert: bool = field(init=False)
    thermal_reg_active_alert: bool = field(init=False)
    vin_uvcl_active_alert: bool = field(init=False)
    iin_limit_active_alert: bool = field(init=False)
    constant_current_alert: bool = field(init=False)
    constant_voltage_alert: bool = field(init=False)

    def __post_init__(self, raw_value):
        bw = 5
        for idx, dc_field in enumerate(fields(self)):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)
            bw -= 1


@dataclass
class BR_charger_state(BitRegister):
    charger_state_str: str = field(init=False)

    def __post_init__(self, raw_value):
        if raw_value == 4096:
            self.charger_state_str = 'bat_detect_failed_fault'
        elif raw_value == 2048:
            self.charger_state_str = 'battery_detection'
        elif raw_value == 1024:
            self.charger_state_str = 'equalize_charge'
        elif raw_value == 512:
            self.charger_state_str = 'absorb_charge'
        elif raw_value == 256:
            self.charger_state_str = 'charger_suspended'
        elif raw_value == 64:
            self.charger_state_str = 'cc_cv_charge'
        elif raw_value == 2:
            self.charger_state_str = 'bat_missing_fault'
        elif raw_value == 1:
            self.charger_state_str = 'bat_short_fault'
        else:
            self.charger_state_str = 'unknown'


@dataclass
class BR_charger_status(BitRegister):
    charger_status_str: str = field(init=False)

    def __post_init__(self, raw_value):
        if raw_value == 32:
            self.charger_status_str = 'ilim_reg_active'
        elif raw_value == 16:
            self.charger_status_str = 'thermal_reg_active'
        elif raw_value == 8:
            self.charger_status_str = 'vin_uvcl_active'
        elif raw_value == 4:
            self.charger_status_str = 'iin_limit_active'
        elif raw_value == 2:
            self.charger_status_str = 'constant_current'
        elif raw_value == 1:
            self.charger_status_str = 'constant_voltage'
        elif raw_value == 0:
            self.charger_status_str = 'charger_off'
        else:
            self.charger_status_str = 'unknown'


@dataclass
class BR_SYSTEM_STATUS_REG(BitRegister):
    en_chg: bool = field(init=False)
    cell_count_err: bool = field(init=False)
    no_rt: bool = field(init=False)
    thermal_shutdown: bool = field(init=False)
    vin_ovlo: bool = field(init=False)
    vin_gt_vbat: bool = field(init=False)
    vin_gt_4p2v: bool = field(init=False)
    intvcc_gt_2p8v: bool = field(init=False)

    def __post_init__(self, raw_value):
        bw = 8
        for dc_field in fields(self):
            setattr(self, dc_field.name, ((raw_value >> bw) & 1) == 1)

            if bw == 7:
                bw = 5
            else:
                bw -= 1


@dataclass
class BR_CHEM_CELLS_REG(BitRegister):
    chem: str = field(init=False)
    cell_count_str: str = field(init=False)
    cell_count: int = field(init=False)

    def __post_init__(self, raw_value):
        tmp = (raw_value >> 8) & 0xf

        if tmp == 0:
            self.chem = 'LTC4162_LAD'
        elif tmp == 1:
            self.chem = 'LTC4162_L42'
        elif tmp == 2:
            self.chem = 'LTC4162_L41'
        elif tmp == 3:
            self.chem = 'LTC4162_L40'
        elif tmp == 4:
            self.chem = 'LTC4162_FAD'
        elif tmp == 5:
            self.chem = 'LTC4162_FFS'
        elif tmp == 6:
            self.chem = 'LTC4162_FST'
        elif tmp == 8:
            self.chem = 'LTC4162_SST'
        elif tmp == 9:
            self.chem = 'LTC4162_SAD'
        else:
            self.chem = ''

        self.cell_count = raw_value & 0xf

        if self.cell_count == 0:
            self.cell_count_str = 'Unknown'
        elif self.cell_count == 2:
            self.cell_count_str = '6V Battery'
        elif self.cell_count == 4:
            self.cell_count_str = '12V Battery'
        elif self.cell_count == 6:
            self.cell_count_str = '18V Battery'
        elif self.cell_count == 8:
            self.cell_count_str = '24V Battery'
        else:
            self.cell_count_str = ''


@dataclass
class BR_TELEMETRY_STATUS_REG(BitRegister):
    bsr_questionable: bool = field(init=False)
    telemetry_valid: bool = field(init=False)

    def __post_init__(self, raw_value):
        self.bsr_questionable = (raw_value >> 1) & 1 == 1
        self.telemetry_valid = raw_value & 1 == 1


@dataclass
class AlertLimit:
    vbat_lo: RegisterVAL = RegisterVAL(code=0x01, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vbat)
    vbat_hi: RegisterVAL = RegisterVAL(code=0x02, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vbat)
    vin_lo: RegisterVAL = RegisterVAL(code=0x03, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vin)
    vin_hi: RegisterVAL = RegisterVAL(code=0x04, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vin)
    vout_lo: RegisterVAL = RegisterVAL(code=0x05, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vout)
    vout_hi: RegisterVAL = RegisterVAL(code=0x06, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vout)
    iin_hi: RegisterVAL = RegisterVAL(code=0x07, bit_rang=16, unpack='h', fn_conv=LSBSize.get_iin)
    ibat_lo: RegisterVAL = RegisterVAL(code=0x08, bit_rang=16, unpack='h', fn_conv=LSBSize.get_ibat)
    die_temp: RegisterVAL = RegisterVAL(code=0x09, bit_rang=16, unpack='h', fn_conv=LSBSize.get_die_temp)
    bsr_hi: RegisterVAL = RegisterVAL(code=0x0A, bit_rang=16, unpack='h', fn_conv=LSBSize.get_bsr)

    def read_value(self, address: AddressI2C, cell_opt: int):
        for dc_field in fields(self):
            getattr(self, dc_field.name).read_value(address, cell_opt)


@dataclass
class ADCValues:
    vbat: RegisterVAL = RegisterVAL(code=0x3A, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vbat)
    vbat_filt: RegisterVAL = RegisterVAL(code=0x47, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vbat)
    vin: RegisterVAL = RegisterVAL(code=0x3B, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vin)
    vout: RegisterVAL = RegisterVAL(code=0x3C, bit_rang=16, unpack='h', fn_conv=LSBSize.get_vout)
    ibat: RegisterVAL = RegisterVAL(code=0x3D, bit_rang=16, unpack='h', fn_conv=LSBSize.get_ibat)
    iin: RegisterVAL = RegisterVAL(code=0x3E, bit_rang=16, unpack='h', fn_conv=LSBSize.get_iin)
    die_temp: RegisterVAL = RegisterVAL(code=0x3F, bit_rang=16, unpack='h', fn_conv=LSBSize.get_die_temp)
    bsr: RegisterVAL = RegisterVAL(code=0x41, bit_rang=16, unpack='h', fn_conv=LSBSize.get_bsr)
    bsr_charge_current: RegisterVAL = RegisterVAL(code=0x48, bit_rang=16, unpack='h', fn_conv=LSBSize.get_ibat)

    def read_value(self, address: AddressI2C, cell_opt: int):
        for dc_field in fields(self):
            getattr(self, dc_field.name).read_value(address, cell_opt)


@dataclass
class Settings:
    iin_limit_target: RegisterVAL = RegisterVAL(code=0x15, bit_rang=6, unpack='B', fn_conv=LSBSize.get_iin_lim_target)
    input_undervoltage_setting: RegisterVAL = RegisterVAL(code=0x16, bit_rang=8, unpack='B', fn_conv=LSBSize.get_input_undervoltage_setting)
    charge_current_setting: RegisterVAL = RegisterVAL(code=0x1A, bit_rang=5, unpack='B', fn_conv=LSBSize.get_icharge_setting)
    vcharge_setting: RegisterVAL = RegisterVAL(code=0x1B, bit_rang=6, unpack='B', fn_conv=LSBSize.get_vcharge_setting)
    c_over_x_threshold: RegisterVAL = RegisterVAL(code=0x1C, bit_rang=16, unpack='H', fn_conv=None)
    en_sla_temp_comp: RegisterVAL = RegisterVAL(code=0x29, bit_rang=1, unpack='B', fn_conv=None)
    vabsorb_delta: RegisterVAL = RegisterVAL(code=0x2A, bit_rang=6, unpack='B', fn_conv=None)
    max_absorb_time: RegisterVAL = RegisterVAL(code=0x2B, bit_rang=16, unpack='H', fn_conv=None)
    v_equalize_delta: RegisterVAL = RegisterVAL(code=0x2C, bit_rang=6, unpack='B', fn_conv=None)
    max_equalize_time: RegisterVAL = RegisterVAL(code=0x2D, bit_rang=16, unpack='H', fn_conv=None)
    tabsorbtimer: RegisterVAL = RegisterVAL(code=0x32, bit_rang=16, unpack='H', fn_conv=None)
    tequalizetimer: RegisterVAL = RegisterVAL(code=0x33, bit_rang=16, unpack='H', fn_conv=None)
    charger_state: RegisterREG = RegisterREG(
        code=0x34, bit_rang=13, unpack='H',
        reg=BR_charger_state
    )
    charge_status: RegisterREG = RegisterREG(
        code=0x35, bit_rang=6, unpack='B',
        reg=BR_charger_status
    )
    thermal_reg_start_temp: RegisterVAL = RegisterVAL(code=0x10, bit_rang=16, unpack='h', fn_conv=None)
    thermal_reg_end_temp: RegisterVAL = RegisterVAL(code=0x11, bit_rang=16, unpack='h', fn_conv=None)

    def read_value(self, address: AddressI2C, cell_opt):
        for dc_field in fields(self):
            if dc_field.type is RegisterVAL:
                getattr(self, dc_field.name).read_value(address, cell_opt)
            elif dc_field.type is RegisterREG:
                getattr(self, dc_field.name).read_value(address)


@dataclass
class DACValues:
    icharge_dac: RegisterVAL = RegisterVAL(code=0x44, bit_rang=5, unpack='B', fn_conv=LSBSize.get_icharge_setting)
    vcharge_dac: RegisterVAL = RegisterVAL(code=0x45, bit_rang=6, unpack='B', fn_conv=LSBSize.get_vcharge_setting)
    iin_limit_dac: RegisterVAL = RegisterVAL(code=0x46, bit_rang=6, unpack='B', fn_conv=LSBSize.get_iin_lim_target)
    input_undervoltage_dac: RegisterVAL = RegisterVAL(code=0x4B, bit_rang=8, unpack='B', fn_conv=LSBSize.get_input_undervoltage_setting)

    def read_value(self, address: AddressI2C, cell_opt):
        for dc_field in fields(self):
            getattr(self, dc_field.name).read_value(address, cell_opt)


@dataclass
class REGValues:
    EN_LIMIT_ALERTS_REG: RegisterREG = RegisterREG(
        code=0x0D, bit_rang=16, unpack='H',
        reg=BR_EN_LIMIT_ALERTS_REG
    )
    EN_CHARGER_STATE_ALERTS_REG: RegisterREG = RegisterREG(
        code=0x0E, bit_rang=13, unpack='H',
        reg=BR_EN_CHARGER_STATE_ALERTS_REG
    )
    EN_CHARGE_STATUS_ALERTS_REG: RegisterREG = RegisterREG(
        code=0x0F, bit_rang=6, unpack='B',
        reg=BR_EN_CHARGE_STATUS_ALERTS_REG
    )
    CONFIG_BITS_REG: RegisterREG = RegisterREG(
        code=0x14, bit_rang=6, unpack='B',
        reg=BR_CONFIG_BITS_REG
    )
    LIMIT_ALERTS_REG: RegisterREG = RegisterREG(
        code=0x36, bit_rang=16, unpack='H',
        reg=BR_LIMIT_ALERTS_REG
    )
    CHARGER_STATE_ALERTS_REG: RegisterREG = RegisterREG(
        code=0x37, bit_rang=13, unpack='H',
        reg=BR_CHARGER_STATE_ALERTS_REG
    )
    CHARGE_STATUS_ALERTS_REG: RegisterREG = RegisterREG(
        code=0x38, bit_rang=6, unpack='B',
        reg=BR_CHARGE_STATUS_ALERTS_REG
    )
    SYSTEM_STATUS_REG: RegisterREG = RegisterREG(
        code=0x39, bit_rang=9, unpack='H',
        reg=BR_SYSTEM_STATUS_REG
    )
    CHEM_CELLS_REG: RegisterREG = RegisterREG(
        code=0x43, bit_rang=12, unpack='H',
        reg=BR_CHEM_CELLS_REG
    )
    TELEMETRY_STATUS_REG: RegisterREG = RegisterREG(
        code=0x4A, bit_rang=2, unpack='B',
        reg=BR_TELEMETRY_STATUS_REG
    )

    def read_value(self, address: AddressI2C):
        for dc_field in fields(self):
            getattr(self, dc_field.name).read_value(address)


@dataclass
class LTC4162S:
    address: AddressI2C

    alert_limit: AlertLimit = AlertLimit()
    adc: ADCValues = ADCValues()
    dac: DACValues = DACValues()
    reg: REGValues = REGValues()
    settings: Settings = Settings()

    def __post_init__(self):
        self.read_value()

    def read_value(self):
        self.reg.read_value(self.address)

        cell_opt = int(self.reg.CHEM_CELLS_REG.reg.cell_count / 2)

        self.adc.read_value(self.address, cell_opt)
        self.dac.read_value(self.address, cell_opt)
        self.alert_limit.read_value(self.address, cell_opt)
        self.settings.read_value(self.address, cell_opt)
