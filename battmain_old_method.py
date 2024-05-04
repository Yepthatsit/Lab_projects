from Mylibrarry import qSerial
import time
import sys
import signal
################################ User parameters #############################################
filename = "./bateriaNiCd/BatNiCd001_old_method_no_res.dat"
Setpoint = 180
Heatsetp = 300
Ramp = 0.1
################################ Function definitions ########################################
def signal_handler(sig,frame):
    print("Caugth ctrl ^c!")
    Fluke8846A.write(b'SYST:LOC\r\n')#zwolnić interfejs multimetru, tak żeby mógł być znowu używany manualnie z panelu głównego
    Fluke8846A.close() #zamknięcie komunikacji
    HP.write(b'SYST:LOC\r\n')
    HP.close()
    #Lakeshore335.write(b'SETP 1, 300\r\n')
    time.sleep(1)
    #Lakeshore335.write(b'RANGE 1,0\r\n')
    Lakeshore335.close()
    sys.exit(0) #przerwanie programu
#############################################################################################
if __name__ == "__main__":
    datafile = open(filename , "a")
    datafile.write("Temperatue A,Temperature B,Setpoint,pwr,Voltage,Current,mnumber,Time\n")
    datafile.close()
    signal.signal(signal.SIGINT,signal_handler)
    Lakeshore335 = qSerial.qSerial(port='COM3',baudrate=57600,bytesize=qSerial.SEVENBITS,stopbits=qSerial.STOPBITS_ONE,parity=qSerial.PARITY_ODD,timeout=10)
    Fluke8846A = qSerial.qSerial(port='COM6',baudrate=9600,timeout=1)
    HP = qSerial.qSerial('COM4',9600,timeout=1,parity=qSerial.PARITY_NONE)
    Fluke8846A.write(b'SYST:REM\r\n')# wysyła multimetrowi komendę zmieniającą działanie interfejsu na tryb zdalny
    HP.write(b'SYST:REM\r\n')
    Lakeshore335.write(b'RANGE 1,3\r\n')
    while (float(Lakeshore335.query("KRDG? A\r\n")) <300 or float(Lakeshore335.query("KRDG? B\r\n")) <300):
        print(Lakeshore335.query("KRDG? A\r\n"),Lakeshore335.query("KRDG? A\r\n"),Lakeshore335.query("KRDG?  B\r\n"),Lakeshore335.query("HTR? 1\r\n"))
        time.sleep(60)
    print("temp reached")
    #time.sleep(30*60)
    Lakeshore335.write(bytes("RAMP 1,1,{}\r\n".format(Ramp),'ascii'))
    time.sleep(1)
    Lakeshore335.write(bytes("SETP 1,{}\r\n".format(Setpoint),'ascii'))
    time.sleep(1)
    TemperatureB = float(Lakeshore335.query("KRDG? B\r\n").replace("\r\n",""))
    start_time = time.time()
    mnumber = 0
    while TemperatureB > Setpoint:
        pwr = Lakeshore335.query("HTR? 1\r\n").replace("\r\n","")
        Current = Fluke8846A.query('MEAS:curr:dc?\r\n').replace("\r\n","")
        Voltage = HP.query('MEAS:volt:dc?\r\n').replace("\r\n","")
        TemperatureA = float(Lakeshore335.query('KRDG? A\r\n').replace("\r\n", ""))
        TemperatureB = float(Lakeshore335.query('KRDG? B\r\n').replace("\r\n",""))
        msetp = Lakeshore335.query("SETP?\r\n").replace("\r\n","")
        Time = round(time.time() - start_time,2)
        mnumber+=1
        dataline = f"{TemperatureA},{TemperatureB},{msetp},{pwr},{Voltage},{Current},{mnumber},{Time}\n"
        print(dataline)
        datafile = open(filename,'a')
        datafile.write(dataline)
        datafile.close()
        time.sleep(5)
    Lakeshore335.write(bytes("SETP 1,{}\r\n".format(Heatsetp),'ascii'))
    while TemperatureB < Heatsetp:
        pwr = Lakeshore335.query("HTR? 1\r\n").replace("\r\n","")
        Current = Fluke8846A.query('MEAS:curr:dc?\r\n').replace("\r\n","")
        Voltage = HP.query('MEAS:volt:dc?\r\n').replace("\r\n","")
        TemperatureA = float(Lakeshore335.query('KRDG? A\r\n').replace("\r\n", ""))
        TemperatureB = float(Lakeshore335.query('KRDG? B\r\n').replace("\r\n",""))
        Time = round(time.time() - start_time,2)
        msetp = Lakeshore335.query("SETP?\r\n").replace("\r\n","")
        mnumber+=1
        dataline = f"{TemperatureA},{TemperatureB},{msetp},{pwr},{Voltage},{Current},{mnumber},{Time}\n"
        print(dataline)
        datafile = open(filename,'a')
        datafile.write(dataline)
        datafile.close()
        time.sleep(5)
    Lakeshore335.write(b'SETP 1, 300\r\n')
    time.sleep(1)
    Lakeshore335.write(b'RANGE 1,0\r\n')
    Fluke8846A.write(b'SYST:LOC\r\n')# wysyła multimetrowi komendę zmieniającą działanie interfejsu na tryb zdalny
    HP.write(b'SYST:LOC\r\n')
    Fluke8846A.close()
    HP.close()
    Lakeshore335.close()