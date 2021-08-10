import serial
import serial.tools.list_ports
import time
import struct
import numpy as np
import codecs

class TM192D():

    def __init__(self):
        self.baud = 38400
        self.initialized = False

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
        # Return the field strength, 0 if the device is disconnected
        if (not self.isConnected()):
            return 0
        try:
            readBytes = [0]*14 # Empty list with length 14

            while (self.serial.in_waiting > 14): # Empty the buffer until 14 bytes are left
                self.serial.read()

            while readBytes[0:2] != b'\x01D': 
                # Only stop reading if the received bytes begin with the correct start byte - 0x0144
                readBytes = self.serial.read(14)
                print(codecs.encode(readBytes, 'hex'))
                self.serial.reset_input_buffer()

                # Data format, 14 bytes: 0x0144XXXXYYYYZZZZDDDDTTTTSS??
                # XX/YY/ZZ = 16-bit ints, field strength on each axis
                # DD/TT Datetime, unknown format
                # SS Scale byte, more info below
            scale = readBytes[12]
        except:
            return 0

        # Scale Byte: 0bXXYYZZUU

        # For XX/YY/ZZ
        # 00 = 1e-2
        # 01 = 1e-1
        # 10 = 1e0
        # 11 = 1e1

        # UU = Units
        # 00 = mG
        # 10 = uT

        # This info used to scale the 16-bit int used for the xyz field strengths

        xScale = 10**(float((scale & 0b11000000) >> 6) - 2)
        yScale = 10**(float((scale & 0b00110000) >> 4) - 2)
        zScale = 10**(float((scale & 0b00001100) >> 2) - 2)

        # Unpack each component as a 16-bit int, and then apply scale
        x = struct.unpack('h', readBytes[2:4])[0]*xScale
        y = struct.unpack('h', readBytes[4:6])[0]*yScale
        z = struct.unpack('h', readBytes[6:8])[0]*zScale

        return x, y, z

    def isConnected(self):
        if self.initialized:
            return self.port in [p.name for p in serial.tools.list_ports.comports()]
        return False

    def end(self):
        # Release the usb interface
        self.serial.close()
        self.initialized = False

    def searchPorts(self):
        # Search all serial ports based on Vendor ID and Product ID for the gauss meter
        for p in serial.tools.list_ports.comports():
            if p.vid == 0x067B and p.pid == 0x2303:
                self.port = p.name
                return True
        return False

if (__name__ == "__main__"):
    gauss = TM192D()
    gauss.begin()

    for i in range(100):
        read = gauss.getReading()
        print(read, gauss.isConnected())
        if read == 0 and gauss.isConnected():
            gauss.end()
            gauss.begin()
        time.sleep(1)
    
    gauss.end()