import pymodbus
import sys
from pymodbus.client import ModbusSerialClient
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def c_to_f(t):
    return round(((9.0 / 5.0) * t + 32.0), 1)

client = ModbusSerialClient( 
    method = 'rtu', 
    port = sys.argv[1], 
    startbit=1, 
    databits=1, 
    bytesize=8, 
    baudrate=9600 , 
    parity= 'N', 
    stopbits=2, 
    timeout=2)

client.connect()
hregs = client.read_holding_registers(6, count=1, unit=1)
print((c_to_f(hregs.getRegister(0) / 10.0)))

iregs = client.read_input_registers(3, count=9, unit=1)
for i in range (1, 9):
    print((c_to_f(iregs.getRegister(i) / 10.0)))
    print((float(iregs.getRegister(i))))
