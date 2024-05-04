
##### DZIAŁA DOKŁADNIE TAK SAMO JAK FLUKE TYLKO UWAŻAĆ NA TO , ŻEBY BYŁ USTAWIONY NA KOMUNIKACJE RS-232
##### KOMENDY STANDARD SCPI
import serial.tools.list_ports as p
import serial
import signal
import sys
import time
list1 = p.comports()
def signal_handler(sig,frame):
    print("Caugth ctrl ^c!")
    HP.write(b'SYST:LOC\r\n')
    HP.close()
    sys.exit(0)
for i in list1:
    print(i)
HP = serial.Serial('COM14',9600,timeout=1,parity=serial.PARITY_NONE)
signal.signal(signal.SIGINT,signal_handler)
HP.write(b'SYST:REM\r\n')
time.sleep(1)
while True:
    HP.write(bytes('MEAS:curr:dc?\r\n','utf-8'))
    print(HP.read_until(b'\r\n'))