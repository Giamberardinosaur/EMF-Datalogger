import serial
import serial.tools.list_ports
import time

class RFMeter():

    def __init__(self):
        self.baud = 115200
        self.initialized = False
        self.scaleFactor = 1 # Factor to scale the readings by, units are uw/m2
        self.rangeFactor = 1 # Scaling the readings by range

    def begin(self):
        try:
            if not self.searchPorts(): # Return false if the device is not found
                if self.initialized:
                    self.end()
                return False
            
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
            self.serial.set_buffer_size(rx_size = 128)
            self.initialized = True
            return True
        except Exception as e:
            # Return False if the device fails to connect
            return False
    
    def getReading(self):
        # Return the RF strength, 0 if the device is disconnected
        if (not self.isConnected()):
            return (0, float('nan'), float('nan'))
        try:
            while (self.serial.in_waiting > 27):
                self.serial.read()
            reading = self.serial.read(27) # incoming reading is always 27 characters long
            reading = reading.decode("utf-8")[:-1]
            print(reading)
            read = reading.split(',')


            power = int(float(read[0])/1024*1.1*1999*self.scaleFactor*self.rangeFactor) # Reading transmitted is a 10-bit int, from 0V - 1.1V
            power = min(power, 2000*self.scaleFactor*self.rangeFactor) # Cap the received value at the max range of the device


            lat = float(read[1])
            lon = float(read[2])
        except Exception as e:
            print(e)
            return (0, float('nan'), float('nan'))

        return power, lat, lon

    def isConnected(self):
        if self.initialized:
            return self.port in [p.name for p in serial.tools.list_ports.comports()]
        return False

    def end(self):
        # Release the usb interface
        self.serial.close()
        self.initialized = False

    def searchPorts(self):
        # Search all serial ports based on Vendor ID and Product ID for the arduino uno
        for p in serial.tools.list_ports.comports():
            if p.vid == 0x2341 and p.pid == 0x0043:
                self.port = p.name
                return True
        return False

    def setConfig(self, scaleFactor=None, rangeFactor=None):
        if scaleFactor is not None:
            self.scaleFactor = scaleFactor
        if rangeFactor is not None:
            self.rangeFactor = rangeFactor

if (__name__ == "__main__"):
    rf = RFMeter()
    rf.begin()

    for i in range(100):
        read = rf.getReading()
        print(read, rf.isConnected())
        if read == 0 and rf.isConnected():
            rf.end()
            rf.begin()
        time.sleep(1)
    
    rf.end()