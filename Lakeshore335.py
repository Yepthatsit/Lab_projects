import serial
import serial.tools.list_ports
import time
from lakeshore import Model335
p = serial.tools.list_ports.comports()
for i in p:
    print(i)
Lakeshore335 = serial.Serial(port='COM13',baudrate=57600,bytesize=serial.SEVENBITS,stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_ODD,timeout=10)
Lakeshore335.write(b'KRDG?\r\n')
print(Lakeshore335.readline().decode())
Lakeshore335.close()
Lakeshore335 = Model335(baud_rate=57600,com_port='COM13',timeout=10)
print(Lakeshore335.query('*IDN?'))