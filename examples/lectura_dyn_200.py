# workaraund tyo work with external folders modules
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from bsp.common import util
import datetime, pprint, time

from bsp.v3.modbus_generic import AddressSerial, AddressSerialPort
from dispositivos_modbus.DYN200 import MedidorDeEnergia
from dataclasses import dataclass, field
from typing import List
import datetime as dt
import time


sampling_time_s = 1

general_port = AddressSerialPort.rs485_isolated_4
general_baudrate = 9600
modbus_mode = "rtu"


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




try:
    with open('data.txt', 'w') as f:
        f.write("FECHA" + "," + "TORQUE" + "," + "RPM" + "," + "POTENCIA" + '\n')
        print("FECHA" + " " + "TORQUE" + " " + "RPM" + " " + "POTENCIA" + '\n')
        while True:
            result = Mediciones()
            result_dict = util.asdict_without_datetostr(result)
            current_time = dt.datetime.now().strftime('%H:%M:%S')

            torque = result_dict["medidores_de_energia"][0]["registers_torque"]
            rpm = result_dict["medidores_de_energia"][0]["registers_rpm"]
            potencia = result_dict["medidores_de_energia"][0]["registers_potencia"]

            data = str(current_time) + "---->     " + str(torque) + "     " + str(rpm) + "     " + str(potencia)
            print(data)
            f.write(data + '\n')


            time.sleep(1)

except KeyboardInterrupt:
    print('Interrupted')
    f.close()

