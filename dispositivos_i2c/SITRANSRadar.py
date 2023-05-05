import traceback
import time

from bsp.common.Config import Config
from dispositivos_i2c.MCP3424 import MCP3424

from dataclasses import dataclass, field, InitVar
from typing import Union


class SITRANS:
    RES: int = 75
    VOLT_MAX = 0.02 * RES
    VOLT_MIN = 0.004 * RES

    def get_distance(self, adc: MCP3424, cal_inf: float, cal_sup: float) -> float:
        pendiente1 = (self.VOLT_MAX - self.VOLT_MIN)
        pendiente2 = (cal_inf - cal_sup)

        adc.read_value()

        return round(cal_inf - (((pendiente2 / pendiente1) * (adc.value_v - self.VOLT_MIN)) + 0), 3)


@dataclass
class Identificacion:
    aplicacion: str
    code: str


@dataclass
class RadarCombustible:
    adc: MCP3424
    id: Union[Identificacion, None]

    cal_inf: InitVar[float]
    cal_sup: InitVar[float]

    distancia_radar: float = field(init=False)
    nivel_combustible: float = field(init=False)

    def __post_init__(self, cal_inf: float, cal_sup: float):
        retry = Config.RETRY
        while retry > 0:
            try:

               self.distancia_radar = SITRANS().get_distance(self.adc, cal_inf, cal_sup)
               self.nivel_combustible = cal_inf - self.distancia_radar
               self.status = "OK"
               return

            except Exception as e:
                retry -= 1
                time.sleep(Config.TIME_WAIT_EXCEPTION)

                self.status = traceback.format_exc()
