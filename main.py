# workaraund tyo work with external folders modules
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from bsp.common import util
import datetime, pprint, time

import paho.mqtt.client as mqtt
from bsp.v3.modbus_generic import AddressSerial, AddressSerialPort
from dispositivos_modbus.PM5100 import MedidorDeEnergia
from dataclasses import dataclass, field
from typing import List
import json

sampling_time_s = 2
general_port= AddressSerialPort.rs485_isolated_4
general_baudrate = 9600
modbus_mode = "rtu"

THINGSBOARD_HOST    = 'demo.thingsboard.io'
ACCESS_TOKEN        = 'ypfO0yYZ5xeuv5bMtHT5'
PORT                = 1883
KEEPLIVE            = 60
TOPIC               = 'v1/devices/me/telemetry'
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, PORT, KEEPLIVE)
client.loop_start()

medidores_energia_address_lst = [
    AddressSerial(aplicacion="Medidor_1", method=modbus_mode, port=general_port, baudrate=general_baudrate, slave=1)
]

@dataclass
class Mediciones:
    date: datetime = field(init=False)
    tipo_de_red: str = field(init=False)
    status: str = field(init=False)
    control: str = field(init=False)

    medidores_de_energia: List[MedidorDeEnergia] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.date = datetime.datetime.now(tz=datetime.timezone.utc).astimezone()
        self.status = "OK"
        self.tipo_de_red = ""

        for address in medidores_energia_address_lst:
            medidor_de_energia = MedidorDeEnergia(address=address)
            self.medidores_de_energia.append(medidor_de_energia)

            if medidor_de_energia.status != "OK":
                self.status = "Error"


###########################
# Aqui comienza el programa principal
while True:
    init = datetime.datetime.now()

    result = Mediciones()
    result_dict = util.asdict_without_datetostr(result)
    payload = json.dumps(util.asdict(result))
    # pprint.pprint(util.asdict(result), compact=True)
    status = result_dict["status"]
    if status == "OK":
        medidor1 = result_dict["medidores_de_energia"][0]
        del medidor1['address']
        del medidor1['status']
        print(medidor1)
        client.publish(TOPIC, json.dumps(medidor1))
        print()

    print("Elapsed time: %d s" % (datetime.datetime.now() - init).total_seconds())

    while (datetime.datetime.now() - init).total_seconds() < sampling_time_s:
        time.sleep(1)






















