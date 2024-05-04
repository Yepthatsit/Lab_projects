
from Mylibrarry import qSerial
import time
import signal
import sys
from datetime import datetime
import numpy as np
################################################
'''dodatkowe definicje'''
################################################
def signal_handler(sig,frame):
    print("Caugth ctrl ^c!")
    #Fluke8846A.write(b'SYST:LOC\r\n')#zwolnić interfejs multimetru, tak żeby mógł być znowu używany manualnie z panelu głównego
    #Fluke8846A.close() #zamknięcie komunikacji
    HP.write(b'SYST:LOC\r\n')
    HP.close()
    Lakeshore335.write(b'SETP 1, 300\r\n')
    time.sleep(1)
    Lakeshore335.write(b'RANGE 1,0\r\n')
    Lakeshore335.close()
    datafile.close()
    sys.exit(0) #przerwanie programu
###################################################
'''setup'''
###################################################
signal.signal(signal.SIGINT,signal_handler)
print(qSerial.available())
Lakeshore335 = qSerial.qSerial(port='COM3',baudrate=57600,bytesize=qSerial.SEVENBITS,stopbits=qSerial.STOPBITS_ONE,parity=qSerial.PARITY_ODD,timeout=10)
#Fluke8846A = qSerial.qSerial(port='COM6',baudrate=9600,timeout=1)
HP = qSerial.qSerial('COM4',9600,timeout=1,parity=qSerial.PARITY_NONE)
time.sleep(1)
#Fluke8846A.write(b'SYST:REM\r\n')# wysyła multimetrowi komendę zmieniającą działanie interfejsu na tryb zdalny
HP.write(b'SYST:REM\r\n')# wysyła multimetrowi komendę zmieniającą działanie interfejsu na tryb zdalny
time.sleep(1)
Lakeshore335.write(b"RAMP 1,1,1\r\n")
time.sleep(1)
Lakeshore335.write(b'RANGE 1,3\r\n')
####################################################
filename = "./bateriaNiCd/BatNiCd_no_added_res001.dat"
Setpoint = 200
CoolingEnd = 200
HeatingEnd = 315
Stabtime = 20
####################################################
mnumber =0
datafile = open(filename , "a")
datafile.write("Temperatue B,Temperature A,Setpoint,pwr,Voltage,Current,mnumber,Time\n")
start_time = time.time()
datafile.close()
while Setpoint <= HeatingEnd:
    Lakeshore335.write(bytes("SETP 1,{}\r\n".format(Setpoint),'ascii'))
    time.sleep(1)
    helptime = time.time()
    while time.time() - helptime <= Stabtime*60:
        pwr = Lakeshore335.query("HTR? 1\r\n").replace("\r\n","")
        Current = np.NaN#Fluke8846A.query('MEAS:curr:dc?\r\n').replace("\r\n","")
        Voltage = HP.query('MEAS:volt:dc?\r\n').replace("\r\n","")
        TemperatureA = float(Lakeshore335.query('KRDG? A\r\n').replace("\r\n", ""))
        TemperatureB = Lakeshore335.query('KRDG? B\r\n').replace("\r\n","")
        Time = round(time.time() - start_time,2)
        mnumber+=1
        dataline = f"{TemperatureB},{TemperatureA},{Setpoint},{pwr},{Voltage},{Current},{mnumber},{Time}\n"
        print(dataline)
        datafile = open(filename,'a')
        datafile.write(dataline)
        datafile.close()
        time.sleep(5)
    Setpoint+=2
while Setpoint >= CoolingEnd:
    Lakeshore335.write(bytes("SETP 1,{}\r\n".format(Setpoint),'ascii'))
    helptime = time.time()
    while time.time() - helptime <= Stabtime*60:
        pwr = Lakeshore335.query("HTR? 1\r\n").replace("\r\n","")
        Current = np.NaN#Fluke8846A.query('MEAS:curr:dc?\r\n').replace("\r\n","")
        Voltage = HP.query('MEAS:volt:dc?\r\n').replace("\r\n","")
        TemperatureA = float(Lakeshore335.query('KRDG? A\r\n').replace("\r\n", ""))
        TemperatureB = Lakeshore335.query('KRDG? B\r\n').replace("\r\n","")
        Time = round(time.time() - start_time,2)
        mnumber+=1
        dataline = f"{TemperatureB},{TemperatureA},{Setpoint},{pwr},{Voltage},{Current},{mnumber},{Time}\n"
        print(dataline)
        datafile = open(filename,'a')
        datafile.write(dataline)
        datafile.close()
        time.sleep(5)
    Setpoint-=2
Lakeshore335.write(b'SETP 1, 300\r\n')
time.sleep(1)
Lakeshore335.write(b'RANGE 1,0\r\n')
#Fluke8846A.write(b'SYST:LOC\r\n')# wysyła multimetrowi komendę zmieniającą działanie interfejsu na tryb zdalny
HP.write(b'SYST:LOC\r\n')
#Fluke8846A.close()
HP.close()
Lakeshore335.close()