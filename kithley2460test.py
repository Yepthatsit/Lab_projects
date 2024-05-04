import pyvisa
from time import sleep
if __name__ == '__main__':
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    kithley = rm.open_resource('USB0::0x05E6::0x2460::04452187::INSTR')
    print(bytes(kithley.query('*IDN?'),'utf-8'))
    kithley.write('OUTP:STAT OFF')
    kithley.write('SOUR1:FUNC CURR')
    kithley.write('OUTP:STAT ON')
    print(kithley.query(':MEAS?'))
    sleep(5)
    kithley.write('OUTP:STAT OFF')
    kithley.write('SOUR1:FUNC VOLT')
    kithley.write('OUTP:STAT ON')
    print(kithley.query(':MEAS?'))
    '''kithley.write('OUTP:STAT OFF')
    kithley.write('SOUR:FUNC RES')
    kithley.write('OUTP:STAT ON')
    print(kithley.query(':MEAS?'))'''
    kithley.close()