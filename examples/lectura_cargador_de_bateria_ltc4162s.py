#####################################
# I2C communication with bitbangio
# testing ltc4162s battery charger ic
# in gpio 1 for scl and gpio 0 for sda
# it should work in any rpi gpio
#####################################

import datetime
import pprint

from bsp.v3.i2c_generic import AddressI2Cbb
from dispositivos_i2c import LTC4162S
from bsp.common.util import asdict

address = AddressI2Cbb(
    aplicacion='charger_1',
    scl_pin=28,   # gpio 1
    sda_pin=27,   # gpio 0
    address=0x68
)

dt = datetime.datetime.now()
ltc = LTC4162S.LTC4162S(address=address)
dt2 = datetime.datetime.now()

pprint.pprint(asdict(ltc))

print("elapsed: %d s" % (dt2 - dt).microseconds)
