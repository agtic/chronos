from pymodbus.server.sync import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer

import logging
import sys

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# initialize the server information
#---------------------------------------------------------------------------# 
# If you don't set this or any fields, they are defaulted to empty strings.
#---------------------------------------------------------------------------# 
identity = ModbusDeviceIdentification()
identity.VendorName  = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName   = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'


def setup_server():
    datablock = ModbusSequentialDataBlock(address=6, values=[1]*16)
    inpblock = ModbusSequentialDataBlock(address=3, values=[1]*16)
    slave_1 = ModbusSlaveContext(
        di = datablock,
        co = datablock,
        hr = datablock,
        ir = inpblock,
    )

    store = slave_1
    context = ModbusServerContext(slaves=store, single=True)

    #---------------------------------------------------------------------------#
    # run the server you want
    #---------------------------------------------------------------------------# 
    # RTU:
    print(("address: 0x00, value=" + str(context[1].getValues(3, 0))))
    print(("address: 0x01, value=" + str(context[1].getValues(3, 1))))
    return context

if __name__ == "__main__":
    ctx = setup_server()
    server = StartSerialServer(context=ctx, framer=ModbusRtuFramer, identity=identity, port=sys.argv[1], timeout=2, baudrate=9600, startbit=1, databits=1, stopbit=2, bytesize=8, parity='N')
