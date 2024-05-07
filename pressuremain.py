from pymeasure.instruments.srs import SR860
import serial
import os
import subprocess
import sys
from time import sleep,time
class Arduino(serial.Serial):
    def query(self,cmd: bytes):
        self.write(cmd)
        sleep(0.1)
        return (float(self.read_all()))
if __name__ == '__main__':
    arduino = Arduino('COM3', 9600)
    sleep(2)
    pressure = 0
    filename = 'Test_sonda_v3.csv'
    Lockin = SR860('GPIB0::4::INSTR')
    if os.path.isfile(filename):
        pass
    else:
        file = open(filename,'a')
        file.write('Pressure,Voltage,Time\n')
        file.close()
    subprocess.Popen(f'python liveplot.py {filename}')
    const = arduino.query(b'READ?')
    start = time()
    try:
        while True:
            while pressure < 10000:
                arduino.write(bytes(f'{pressure}','utf-8'))
                sleep(5)
                file = open(filename,'a')
                raw_voltage = arduino.query(b'READ?') - const
                a = f'{raw_voltage*0.9/0.4},{Lockin.x},{time()-start}'
                file.write(f'{a}\n')
                print(a)
                file.close()
                pressure += 500
            while pressure > 0:
                arduino.write(bytes(f'{pressure}','utf-8'))
                sleep(5)
                file = open(filename,'a')
                raw_voltage = arduino.query(b'READ?') - const
                a = f'{raw_voltage*0.9/0.4},{Lockin.x},{time()-start}'
                file.write(f'{a}\n')
                print(a)
                file.close()
                pressure -= 500
    except KeyboardInterrupt:
        print('user ended program')
        arduino.write(b'0')    
        arduino.close()
        sys.exit(0)