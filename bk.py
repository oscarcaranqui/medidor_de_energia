import paho.mqtt.client as mqtt
import json
import time
import random

THINGSBOARD_HOST    = 'demo.thingsboard.io'
ACCESS_TOKEN        = 'cWCf2JS1QDybTJtvhg4r'
PORT                = 1883
KEEPLIVE            = 60
TOPIC               = 'v1/devices/me/telemetry'

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, PORT, KEEPLIVE)
client.loop_start()


# data = {'VAB': 0, 'VBC': 0, 'VCA': 0,
#         'VAN': 0, 'VBN': 0, 'VCN': 0,
#
#         'IAB': 0, 'IBC': 0, 'ICA': 0,
#         'IAN': 0, 'IBN': 0, 'ICN': 0
#         }

try:
    while True:
        # VAB = round(random.uniform(235,240), 2)
        # VBC = round(random.uniform(235,240), 2)
        # VCA = round(random.uniform(235,240), 2)
        #
        # VAN = round(random.uniform(115, 120), 2)
        # VBN = round(random.uniform(115, 120), 2)
        # VCN = round(random.uniform(115, 120), 2)
        #
        # IAB = round(random.uniform(0, 10), 2)
        # IBC = round(random.uniform(0, 10), 2)
        # ICA = round(random.uniform(0, 10), 2)
        #
        # IAN = round(random.uniform(0, 10), 2)
        # IBN = round(random.uniform(0, 10), 2)
        # ICN = round(random.uniform(0, 10), 2)
        #
        # data['VAB'] = VAB
        # data['VBC'] = VBC
        # data['VCA'] = VCA
        #
        # data['VAN'] = VAN
        # data['VBN'] = VBN
        # data['VCN'] = VCN
        #
        # data['IAB'] = IAB
        # data['IBC'] = IBC
        # data['ICA'] = ICA
        #
        # data['IAN'] = IAN
        # data['IBN'] = IBN
        # data['ICN'] = IAB
        #
        # a = {'VAB': VAB, 'VBC': VBC, 'VCA': VCA, 'VAN': VAN, 'VBN': VBN, 'VCN': VCN, 'IAB': IAB,
        #  'IBC': IBC, 'ICA': ICA, 'IAN': IAN, 'IBN': IBN, 'ICN': ICN}
        #
        #
        Vavg1 = round(random.uniform(7000,7100),2)
        Iavg1 = round(random.uniform(1,2),2)
        Ptot1 = round(random.uniform(30000,38000),2)
        Edel1 = round(random.uniform(18,20),2)

        Vavg2 = round(random.uniform(7000, 7100), 2)
        Iavg2 = round(random.uniform(1, 2), 2)
        Ptot2 = round(random.uniform(30000, 38000), 2)
        Edel2 = round(random.uniform(18, 20), 2)

        Vavg3 = round(random.uniform(7000, 7100), 2)
        Iavg3 = round(random.uniform(1, 2), 2)
        Ptot3 = round(random.uniform(30000, 38000), 2)
        Edel3 = round(random.uniform(18, 20), 2)

        Vavg4 = round(random.uniform(7000, 7100), 2)
        Iavg4 = round(random.uniform(1, 2), 2)
        Ptot4 = round(random.uniform(30000, 38000), 2)
        Edel4 = round(random.uniform(18, 20), 2)


        A = round(random.uniform(18, 20), 2)
        B = round(random.uniform(18, 20), 2)
        C = round(random.uniform(18, 20), 2)
        D = round(random.uniform(18, 20), 2)

        b = {'Vavg1': Vavg1, 'Iavg1': Iavg1, 'Ptot1': Ptot1, 'Edel1': Edel1 }
        c = {'Vavg2': Vavg2, 'Iavg2': Iavg2, 'Ptot2': Ptot2, 'Edel2': Edel2 }
        d = {'Vavg3': Vavg3, 'Iavg3': Iavg3, 'Ptot3': Ptot3, 'Edel3': Edel3 }
        e = {'Vavg4': Vavg4, 'Iavg4': Iavg4, 'Ptot4': Ptot4, 'Edel4': Edel4 }
        f = {'A': A, 'B': B, 'C': C, 'D': D }
        x = {"exio_relay_1": 1}
        data = {**b, **c, **d, **e, **f, **x}
        print(data)
        print(type(data))
        client.publish(TOPIC, json.dumps(data))

        print("Message: ", data)
        time.sleep(5)

except ValueError:
    print("Problem Connection ")
    pass

client.loop_stop()
client.disconnect()



#
# ########################
# # settings
# ########################
# rpi_plc_library_name = 'rpi_plc_v1'
# sampling_time_s = 60
# max_holding_time_msg_mqtt = 48 * 60 * 60 # 2 dia de retencion de mensaje
#
#
# # workaraund tyo work with external folders modules
# import sys
# from os.path import dirname, join, abspath
# sys.path.insert(0, abspath(join(dirname(__file__), '../' + rpi_plc_library_name)))
#
# import pprint, time, json
#
# import paho.mqtt.client as paho_mqtt
#
# from paho.mqtt.properties import Properties
# from paho.mqtt.packettypes import PacketTypes
#
# from dispositivos_modbus.INTELIdrive import ControlBomba as ID_ControlBomba
# from dispositivos_modbus.INTELIdrive import ReglasAlarmas as ID_ReglasAlarmasBomba
# from dispositivos_modbus.INTELIdrive import Identificacion as ID_IdentificacionBomba
#
# from bsp.v3.modbus_generic import AddressSerial, AddressSerialPort
#
# from bsp.common.util import asdict, get_now_date
#
# from datetime import datetime
# from dataclasses import dataclass, field
# from uuid import getnode as get_mac
#
#
# mac = get_mac()
#
#
# ##--------------------------------------------------
# ## CONFIGURACIONES Alarmas para bombas
# id_reglas_alarmas = ID_ReglasAlarmasBomba(
#     low_eng_temp=80,
#     high_eng_temp=95,
#     low_oil_press=30,
#     low_rpm=1700,
#     high_rpm=1900,
#     low_ubat_6C=11,
#     high_ubat_6C=14,
#     low_ubat_NT_KT=23,
#     high_ubat_NT_KT=26,
#     slow_rpm_value=500,
#     slow_rpm_minutes=15
# )
#
#
#
# ##--------------------------------------------------
# ## CONFIGURACIONES MODBUS INTELIDRIVE
# general_port= AddressSerialPort.rs485_isolated_4
# general_baudrate = 9600
# modbus_mode = "rtu"
#
# address_bombas_lst = [
#     (
#         ID_ControlBomba,
#         AddressSerial(method=modbus_mode, port=general_port, baudrate=general_baudrate, slave=1, aplicacion="Bomba_9"),
#         ID_IdentificacionBomba(id_equipo="MOT-0881", tipo_motor="", serie_equipo="41322902"),
#         None #id_reglas_alarmas
#     ),
#     (
#         ID_ControlBomba,
#         AddressSerial(method=modbus_mode, port=general_port, baudrate=general_baudrate, slave=2, aplicacion="Bomba_10"),
#         ID_IdentificacionBomba(id_equipo="MOT-0882", tipo_motor="", serie_equipo="41322903"),
#         None #id_reglas_alarmas
#     ),
# ]
#
#
# ##--------------------------------------------------
# ##
# @dataclass
# class EstacionDeBombas:
#     status: str = field(init=False)
#
#     control_de_bombas: list = field(init=False, default_factory=list)
#
#     def __post_init__(self):
#         self.status = "OK"
#
#         for ctrl_bomba, address, id_bomba, reglas_alarmas in address_bombas_lst:
#             control_bomba = ctrl_bomba(address=address, id=id_bomba, reglas_alarma=reglas_alarmas)
#             self.control_de_bombas.append(control_bomba)
#
#             if control_bomba.status != "OK":
#                 self.status = "Error"
#
#
# def on_connect(client, userdata, flags, reasonCode, properties):
#     if reasonCode == 0:
#         client.publish(
#             topic=TOPIC_STATUS,
#             payload='1',
#             qos=1,
#             retain=True
#         )
#
#
# ###########################
# # Aqui comienza el programa principal
#
# TOPIC_STATUS = 'status'
# TOPIC_MUESTRAS = 'muestras'
# TOPIC_ULTIMA_MUESTRA = 'ultima_muestra'
#
# device = paho_mqtt.Client(
#     client_id=str(mac),
#     protocol=paho_mqtt.MQTTv5
# )
#
# device.on_connect = on_connect
#
# device.will_set(
#     topic=TOPIC_STATUS,
#     payload='0',
#     qos=1,
#     retain=True
# )
#
# device.connect('localhost', 1885)
# device.loop_start()
#
# print("\t - connecting")
# while not device.is_connected():
#     time.sleep(1)
# print("\t - connected")
#
# while True:
#     init = get_now_date()
#     result = EstacionDeBombas()
#
#     result_dict = asdict(result)
#     pprint.pprint(result_dict, compact=True)
#
#     topic = TOPIC_MUESTRAS + '/%s' % init.isoformat(timespec='milliseconds')
#
#     payload = json.dumps(result_dict)
#
#     properties = Properties(PacketTypes.PUBLISH)
#     properties.MessageExpiryInterval = max_holding_time_msg_mqtt
#
#     device.publish(
#         topic=topic,
#         payload=payload,
#         qos=1,
#         retain=True,
#         properties=properties
#     )
#
#     result_dict.update({'date': init.isoformat(timespec='milliseconds')})
#
#     payload = json.dumps(result_dict)
#
#     device.publish(
#         topic=TOPIC_ULTIMA_MUESTRA,
#         payload=payload,
#         qos=1,
#         retain=True,
#         properties=None
#     )
#
#     print("Elapsed time: %d s" % (get_now_date() - init).total_seconds())
#
#     while (get_now_date() - init).total_seconds() < sampling_time_s:
#         time.sleep(1)
#
#
#
#
