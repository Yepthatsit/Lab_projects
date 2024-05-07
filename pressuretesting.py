import serial
from time import sleep
class Arduino(serial.Serial):
    def query(self,cmd: bytes):
        self.write(cmd)
        sleep(0.1)
        return self.read_all()
if __name__ == "__main__":
    arduino = Arduino('COM3',9600)
    '''sleep(2)
    arduino.write(b'0')
    sleep(0.1)
    arduino.write(b'READ?')
    sleep(0.1)
    const = float(arduino.read_all())
    sleep(0.1)
    const = 0.93'''
    print(arduino.query(b"READ?"))