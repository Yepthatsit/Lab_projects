import numpy as np
import serial
import time
def unitseparation(raw:str):
    '''
    Function separates unit from measurement value
    :param raw: is a data containing unit
    :return: Touple containing (Value,unit)
    '''
    unit = ""
    val = ""
    for i in raw:
        if i.isalpha():
            unit += i
        else:
            val += i
    if val =="":
        return "OVER",unit
    else:
        return float(val), unit
class LCRcom(serial.Serial):
    Gmode = ""
    delayvalue = 1
    def getvalues(self):
        '''
        :return:
        returns a python dictionary {first measured param: value , Second measured param : value , firtparam+ "unit" : str }
        '''
        self.write(b"MAIN:STAR\n\r")
        time.sleep(self.delayvalue)
        list = self.read_all().decode().split()
        if len(list) >= 4:
            if "SECO:OVER" in list and "PRIM:OVER" in list:
                return {self.Gmode[0]: float(list[1]), self.Gmode[1]: np.NaN, self.Gmode[0] + "unit": "I dont know what happend"}
            elif "SECO:OVER" in list:
                return {self.Gmode[0]: float(list[1]), self.Gmode[1]: np.NaN, self.Gmode[0] + "unit": list[3]}
            elif "PRIM:OVER" in list:
                v, u = unitseparation(list[3])
                return {self.Gmode[0]: np.NaN, self.Gmode[1]: v, self.Gmode[0] + "unit": u}
            else:
                secval, firstunit = unitseparation(list[3])
                if len(list) ==5 and firstunit == "":
                    return {self.Gmode[0]: float(list[1]), self.Gmode[1]: secval, self.Gmode[0] + "unit": list[4]}
                else:
                    return {self.Gmode[0]: float(list[1]), self.Gmode[1]: secval, self.Gmode[0] + "unit": firstunit}


        elif len(list) == 3 and "PRIM:OVER" in list:
            v,u = unitseparation(list[2])
            return {self.Gmode[0]: np.NaN, self.Gmode[1]: v, self.Gmode[0] + "unit": u}
        elif len(list) ==1 and list[0] == "PRIM:OVER":
            return {self.Gmode[0]: np.NaN, self.Gmode[1]: np.NaN, self.Gmode[0] + "unit": "both overloaded"}
        elif len(list) ==1 and list[0] == "PRIM:OV01":
            return {self.Gmode[0]: np.NaN, self.Gmode[1]: np.NaN, self.Gmode[0] + "unit": "first overload second no info"}
        elif len(list) ==2 and list[0] == "MAIN:SECO":
            v,u = unitseparation(list[1])
            return {self.Gmode[0]: np.NaN, self.Gmode[1]: v, self.Gmode[0] + "unit": u}
        elif len(list) == 2 and "SECO:OVER" in list[0]:
            return {self.Gmode[0]: np.NaN, self.Gmode[1]: np.NaN, self.Gmode[0] + "unit": list[0].replace("SECO:OVER","")}
        elif len(list) == 2 and list[0] == "MAIN:SECO":
            v,u = unitseparation(list[1])
            return {self.Gmode[0]: np.NaN, self.Gmode[1]: v, self.Gmode[0] + "unit": u}

        else:
            return {self.Gmode[0]:np.NaN, self.Gmode[1]: np.NaN, self.Gmode[0] + "unit": "No response from LCR"}
    def setmode(self,mode = "ZQ",freq = np.NaN,Voltage= np.NaN,delay =1):
        '''
        Function is responsible for setting user values on the LCR.
        Default value of the delay between sending a command and reading buffer(.getvalues() method) is 1 sec.
        :param mode: measurment mode
        :param freq: Frequency in kHz
        :param Voltage: Voltage in V
        :param delay: delay between sending a gueryy and reading buffer in getvalues() method
        :return: python touple (Frequency,Voltage) if a param is not set returns np.NaN
        '''
        self.delayvalue = delay
        time.sleep(1)
        time.sleep(1)
        if not np.isnan(float(Voltage)) and (Voltage>=0.005 and Voltage<=1.275):
            strnum = str("{:8.8f}".format(Voltage))[0:5]
            cmd = f"MAIN:VOLT {strnum}\n\r"
            self.write(bytes(cmd,"ascii"))
            self.write(b"COMU:OFF.\n\r")
            time.sleep(1)
            self.write(b"COMU?\n\r")
            time.sleep(1)
            self.readline().decode()
            self.write(b"COMU:OVER\n\r")
            self.readline().decode()
            time.sleep(1)
            self.read_all()
        elif not np.isnan(float(Voltage)):
            print("Voltage out of bounds")
            print("_______________________________________")
        cmd = f'MAIN:MODE:{mode}\n\r'
        self.Gmode += mode
        self.write(bytes(cmd, "utf-8"))
        print("_______________________________________")
        print(self.readline().decode())
        print("_______________________________________")
        print("_______________________________________")
        self.write(b"MAIN:TRIG:MANU\n\r")
        time.sleep(1)
        print(self.readline().decode())
        print("_______________________________________")
        if not np.isnan(float(freq)) and (freq>=0.012 and freq<=100):
            strnum = str("{:8.8f}".format(freq))[0:7]
            cmd = f"MAIN:FREQ {strnum}\n\r"
            self.write(bytes(cmd,"ascii"))
            time.sleep(1)
            self.read_all()
        elif not np.isnan(float(freq)):
            print("frequency out of bounds")
            print("_______________________________________")
        self.read_all().decode().split()
        self.write(b"MAIN:FREQ?\n\r")
        time.sleep(1)
        self.write(b"MAIN:VOLT?\n\r")
        time.sleep(1)
        resp = self.read_all().decode().split()
        print("_______________________________________")
        for i in resp:
            print(i + " ")
        time.sleep(1)
        ###########################################################
        ############################################################
        if len(resp)>3:
            return resp[1],resp[3]
        else:
            return np.NaN,np.NaN

    def claiminterface(self):
        """
        Function claims the interface
        :return:
        """
        print("_______________________________________")
        self.write(b"COMU?\n\r")
        time.sleep(1)
        print(self.readline().decode())
        self.write(b"COMU:OVER\n\r")
        print(self.readline().decode())
        print("_______________________________________")
    def free(self):
        '''
            Function closes communication
        :return:
        '''
        self.write(b"COMU:OFF.\n\r")
        time.sleep(1)
        self.close()