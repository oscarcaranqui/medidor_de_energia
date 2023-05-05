# todo rewrite and test example with new lib

########################
# Ejemplo de comunicacion modbus a bajo nivel con sensor oxigenometro RDO_BLUE
# se procede a leer el registro 0x25 el cual contiene la muestra tomada del sensor
# la muestra tiene tamaño 0x20
# se lee dos veces porque la primera lectura inicia el muestreo
# el sensor necesita ser configurado previamente con winsitu para cambiar su configuracion modbus parity bit a None
#
# Conexion:
# Pin B - cable azul
# Pin A - cable verde
#
# jumpers config:
# JP1 - close
# JP2 - open
# JP3 - open
# JP4 - close
#
########################

# workaraund tyo work with external folders modules
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from bsp.common.my_pymodbus.sync import ModbusSerialClient as ModbusClient

mb = ModbusClient(method="rtu", port="/dev/serial0", baudrate=19200)

a = mb.read_holding_registers(address=0x25, count=0x20, unit=0x01)
a = mb.read_holding_registers(address=0x25, count=0x20, unit=0x01)

print('[{}]'.format(', '.join(hex(x) for x in a.registers)))
