################################################################ DZIAŁA #####################################################################
### UWAGA NA EOL \r\n zły EOL i w ogóle nie widzi komend
##### KOMENDY STANDARD SCPI
import signal
import sys
import pandas as pd
import serial.tools.list_ports as p
import serial
import time
#####################################################################
'''funkcja określa, co stanie się po wyłapaniu przerwania ctrl ^c'''
def signal_handler(sig,frame):
    print("Caugth ctrl ^c!")
    Fluke8846A.write(b'SYST:LOC\r\n')#zwolnić interfejs multimetru, tak żeby mógł być znowu używany manualnie z panelu głównego
    Fluke8846A.close() #zamknięcie komunikacji
    sys.exit(0) #przerwanie programu
######################################################################
'''wypisanie dostępnych portów'''
list1 = p.comports()
for i in list1:
    print(i)
######################################################################
Fluke8846A = serial.Serial('COM11',9600,timeout=1,parity=serial.PARITY_NONE)# nawiązanie połączenia z multimetrem
signal.signal(signal.SIGINT,signal_handler)# zaczyna wyłapywanie ctrl ^c
Fluke8846A.write(b'SYST:REM\r\n')# wysyła multimetrowi komendę zmieniającą działanie interfejsu na tryb zdalny
time.sleep(1)#czekaj 1s dla pewności że intrerfejs zmienił tryb
while True:
    Fluke8846A.write(bytes('MEAS:volt:dc?\r\n','utf-8'))# wysyła zapytanie o aktualnie zmierzoną wartość
    print(Fluke8846A.read_until(b'\r\n'))# odczytuje pomiar
