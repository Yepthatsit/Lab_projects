import serial
from time import sleep,time
class Arduino(serial.Serial):
    def query(self,cmd: bytes):
        self.write(cmd)
        sleep(0.1)
        return (float(self.read_all()))
if __name__ == '__main__':
    pressure  = 0
    filename = 'test_17_04_v4.csv'
    arduino = Arduino('COM3', 9600)
    sleep(2)
    const = arduino.query(b'READ?')
    file = open(filename,'a')
    file.write(f'Pod,Pzad,V_zad,V_odcz,t\n')
    file.close()
    start = time()
    while pressure < 10000:
        arduino.write(bytes(f'{pressure}','utf-8'))
        sleep(5)
        file = open(filename,'a')
        raw_voltage = arduino.query(b'READ?') - const
        a = f'{raw_voltage*0.9/0.4},{9*pressure*10**-3/10},{pressure},{raw_voltage},{time()-start}'
        file.write(f'{a}\n')
        print(a)
        file.close()
        pressure += 50
    while pressure > 0:
        arduino.write(bytes(f'{pressure}','utf-8'))
        sleep(5)
        file = open(filename,'a')
        raw_voltage = arduino.query(b'READ?') - const
        a = f'{raw_voltage*0.9/0.4},{9*pressure*10**-3/10},{pressure},{raw_voltage},{time()-start}'
        file.write(f'{a}\n')
        print(a)
        file.close()
        pressure -= 50
    arduino.write(b'0')    
    arduino.close()