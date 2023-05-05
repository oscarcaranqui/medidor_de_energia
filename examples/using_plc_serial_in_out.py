###############################################################
# how to use library:
#   PLC_serial_in_out(ext_boards=1)
#   se especifica que la tarjeta rpi_plc tendra una tarjeta
#   de expansion adicional como cape
#
#   plc.pin_output(pin, level)
#   si se usa expansion se puede tener 16 salidas
#   8 salidas de abajo, y 8 salidas de arriba
#   las salidas comienzan desde 0 -> pin[0 - 15]
#   level es 1 para encendio, 0 para apagado
#
#   plc.pin_input(pin)
#   pin [0 - 15] si se usa expansion
#   retorna 1 si la entrada esta encendida
#   retorna 0 si la salida esta apagada
###############################################################

import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import time
from bsp.v3.PLC_serial_in_out import PLC_serial_in_out

plc = PLC_serial_in_out(ext_boards=0)

for i in range(8):
    plc.pin_output(i, 1)
    time.sleep(0.5)

plc.port_output(0xaa)

loops = 5
while loops > 0:
    for i in range(8):
        if plc.pin_input(i) == 1:
            print("pin %d, encendido" % i)

    time.sleep(0.5)
    loops -= 1

port_in = plc.port_input()
print("puerto de entrada = %d" % port_in)