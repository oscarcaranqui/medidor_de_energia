########################
# Ejemplo de lectura de muestras oxigenometro RDO_BLUE
#  * El sensor necesita ser configurado previamente con winsitu para cambiar su configuracion modbus
#   "parity bit" de "even" a "None", de lo contrario no podra ser leido
#
# Conexion:
# Pin B - cable VERDE
# Pin A - cable AZUL
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

import pprint, time, json

from dispositivos_modbus.RDOBLUEsensor import SensorOxigenometro as SO
from bsp.v3.modbus_generic import AddressSerial, AddressSerialPort
from bsp.common.util import asdict_without_datetostr as asdict

enable_storage = False

address = AddressSerial(
    aplicacion="Sensor oxigenometro insitu",
    method="rtu",
    port=AddressSerialPort.rs485_2,
    baudrate=19200,
    slave=1
)

while True:
    a = SO(address=address)
    pprint.pprint(asdict(a))

    if enable_storage:
        with open("muestras_oxigenometro.txt", "a") as f:
            f.write("" + json.dumps(asdict(a)) + ",")

    time.sleep(30)