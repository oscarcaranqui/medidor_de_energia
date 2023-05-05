########################
# Ejemplo de lectura de estacion de bombeo con intelidrive
#
# jumpers config:
# JP1 - close   (A <-> VCC)
# JP2 - open
# JP3 - open
# JP4 - close   (B <-> GND)
#
########################

# workaraund tyo work with external folders modules
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pprint, time, datetime, json

from dispositivos_modbus.DSEcontroler import ControlBomba as CtrlBomba
from bsp.v3.modbus_generic import AddressSerial, AddressSerialPort
from bsp.common.util import asdict_without_datetostr as asdict

from dataclasses import dataclass, field
from typing import List

enable_storage = True

general_port= AddressSerialPort.rs485_1
general_baudrate = 115200
modbus_mode = "rtu"

address_lst = [
    AddressSerial(aplicacion="Bomba_1", method=modbus_mode, port=general_port, baudrate=general_baudrate, slave=1)
]


@dataclass
class EstacionDeBombas:
    date: datetime = field(init=False)
    status: str = field(init=False)

    control_de_bombas: List[CtrlBomba] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.date = str(datetime.datetime.now(tz=datetime.timezone.utc).astimezone())
        self.status = "OK"

        for address in address_lst:
            control_bomba = CtrlBomba(address=address, id=None, reglas_alarma=None)
            self.control_de_bombas.append(control_bomba)

            if control_bomba.status != "OK":
                self.status = "Error"


###########################
# Aqui comienza el programa principal
while True:
    a = EstacionDeBombas()
    pprint.pprint(asdict(a))

    if enable_storage:
        with open("muestras_estacion_de_bombas.txt", "a") as f:
            f.write("" + json.dumps(asdict(a)) + ",")

    time.sleep(30)
