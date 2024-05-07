import pyvisa as visa
import time
import LCR821lib
import subprocess
import os
###############################################

filename = 'test.txt'
delay = 2 # <---------time between mesurements in seconds
Plot_on_start = True

##################################################
if __name__ == '__main__':
    ############################LCR SETUP###################################
    LCR821 = LCR821lib.LCRcom(port="COM2", baudrate=38400, stopbits=1, timeout=5)
    LCR821.claiminterface()
    mode = "ZQ"  # <---------please modify mode here
    voltage = 1  # [V]
    frequency = 10.0  # [kHz]
    delay = 1  # [s]
    Frequency, Voltage = LCR821.setmode(mode=mode, Voltage=voltage, freq=frequency, delay=delay)
    """
        During setup of the LCR you may notice a communication reboot.
        It is made deliberately as the change of voltage seems to require such action.
    """
    ########################################################################
    rm = visa.ResourceManager()
    kithley700 = rm.open_resource('GPIB0::26::INSTR')
    try:
        kithley700.write("*REN")
        kithley700.write('*O0X')
        kithley700.write('*N12X')
        kithley700.write('*GET')
        mnum = 1
        file = open(filename,'a')
        if os.stat(filename).st_size==0:
            file.write(f"Temperature\tResistance\ttheta\tMnum\ttime\tFrequency\tVoltage\n")
        file.close()
        if Plot_on_start:
            subprocess.Popen(f"python Furnaceplot.py {filename}")
        while True:
            rawtemp = kithley700.read('*BOX').split(sep = ',')
            temperature = float(rawtemp[0].replace('DEGC',''))
            resp = LCR821.getvalues()
            resistance = resp[f"{mode[0]}"]
            resunit = resp[f"{mode[0]}unit"]
            if resunit.lower() == "k":
                resistance *= 1000
            theta = resp[f"{mode[1]}"]
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Measurement #{mnum}: Temperature: {temperature} °C\tResistance: {resistance} Ohms angle {theta} Frequency {Frequency} Voltage {Voltage} \t{timestamp} info for programers {resunit}")
            file = open(filename,mode='a')
            file.write(f"{temperature}\t{resistance}\t{theta}\t{mnum}\t{timestamp}\t{Frequency}\t{Voltage}\n")
            file.close()
            time.sleep(delay)
            mnum += 1
    except visa.VisaIOError as e:
        print(f"Error communicating with the instrument: {e}")
    except KeyboardInterrupt:
        print("Measurement stopped by user.")
    finally:
        print('Closing instruments.')
        kithley700.close()
        time.sleep(0.5)
        LCR821.free()
        rm.close()