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
# macros
########################
SECTOR = "siemav"
ESTACION = "test"

collection_name = "logs_" + SECTOR + "_" + ESTACION

database_name = "estacion_de_bombas"
mongo_ip = "192.168.1.142"

mongo_user = "produccion"
mongo_pass = "Profremar202"


# workaraund tyo work with external folders modules
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pprint, time, datetime, pymongo

from dispositivos_modbus.INTELIdrive import ControlBomba as CtrlBombaID
from dispositivos_modbus.DSEcontroler import ControlBomba as CtrlBombaDSE
from bsp.v3.modbus_generic import AddressSerial, AddressSerialPort

from dispositivos_i2c.SITRANSRadar import RadarCombustible
from bsp.v3.i2c_generic import AddressI2Chw

from bsp.common.util import asdict_without_datetostr as asdict

from dataclasses import dataclass, field

enable_storage = True

##--------------------------------------------------
## CONFIGURACIONES MODBUS INTELIDRIVE
general_port= AddressSerialPort.rs485_isolated_4
general_baudrate = 9600
modbus_mode = "rtu"

address_bombas_lst = [
    (
        CtrlBombaID,
        AddressSerial(aplicacion="Bomba_1", method=modbus_mode, port=general_port, baudrate=general_baudrate, slave=1)
    ),
    (
        CtrlBombaDSE,
        AddressSerial(aplicacion="Bomba_2", method=modbus_mode, port=general_port, baudrate=general_baudrate, slave=2)
    ),
]

##--------------------------------------------------
## CONFIGURACIONES I2C SITRANS RADAR
# mcp3424
# ADD1 = High, ADD0 = float
# jp25 = [1-2], jp24 = empty
address_nivel_de_combustible = AddressI2Chw(aplicacion="Sonda_1", channel=0, address=0x6f)
cal_inf = 0
cal_sup = 2.4

##--------------------------------------------------
##
@dataclass
class EstacionDeBombas:
    date: datetime = field(init=False)
    status: str = field(init=False)

    control_de_bombas: list = field(init=False, default_factory=list)
    radar_combustible: RadarCombustible = field(init=False)

    def __post_init__(self):
        self.date = str(datetime.datetime.now(tz=datetime.timezone.utc).astimezone())
        self.status = "OK"

        for ctrl_bomba, address in address_bombas_lst:
            control_bomba = ctrl_bomba(address=address)
            self.control_de_bombas.append(control_bomba)

            if control_bomba.status != "OK":
                self.status = "Error"

        self.radar_combustible = RadarCombustible(address=address_nivel_de_combustible,
                                                  cal_inf=cal_inf, cal_sup=cal_sup)

        if self.radar_combustible.status != "OK":
            self.status = "Error"


###########################
# Aqui comienza el programa principal

c_lst = []
while True:
    init = datetime.datetime.now()

    result = EstacionDeBombas()
    result_dict = asdict(result)
    pprint.pprint(result_dict, compact=True)

    c_lst.append(result_dict)

    while len(c_lst) >= 10:
        try:
            client = pymongo.MongoClient(mongo_ip,
                                         username=mongo_user,
                                         password=mongo_pass,
                                         authMechanism="SCRAM-SHA-1")

            db = client[database_name]
            col = db[collection_name]
            col.insert_many(c_lst)
            client.close()
            c_lst = []
            break
        except Exception as oe:
            print(oe)

            if len(c_lst) < 1000000:
                break

            print("Buffer lleno, intentando insertar muestras nuevamente en 10 segundos...")
            time.sleep(10)


    while (datetime.datetime.now() - init).total_seconds() < 30:
        time.sleep(1)
