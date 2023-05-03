import paho.mqtt.client as mqtt
import json
import time
import random

THINGSBOARD_HOST    = 'XXX'
ACCESS_TOKEN        = 'XXX'
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

        client.publish(TOPIC, json.dumps(data))

        print("Message: ", data)
        time.sleep(5)

except ValueError:
    print("Problem Connection ")
    pass

client.loop_stop()
client.disconnect()
