import numpy as np
from seiinspector import SEIInspector
from TM192D import TM192D
from rfmeter import RFMeter
from collections import deque
from datetime import datetime
import pandas as pd
import time
import os

class DataLogger():
    
    def __init__(self):
        self.DEQUESIZE = 128
        self.ARRSIZE = 3600
        self.RECORDSIZE = 18000

        self.idx = 0 # Current write index in the pandas dataframe
        self.recordIdx = 0 # Current write index in the CSV file
        self.recording = False

        # Set up buffers and larger data storage
        self.valBuffer = deque([], maxlen=self.DEQUESIZE)
        self.timeBuffer = deque([], maxlen=self.DEQUESIZE)
        self.newBuffer()
        self.lastVal = (0, 0)

        # Create instances of all 3 devices
        self.geiger = SEIInspector()
        self.gauss = TM192D()
        self.rf = RFMeter()

        # Set up units and conversions
        self.units = ["CPM", "mG", "μW/m²"] # Default units
        self.geigerConv = {"CPM" : 1, "CPS" : 1/60, "mR/hr" : 1/3340, "μSv/hr" : 1/334} # Conversions from CPM "sensitivity" = 3340 obtained from the device calibration
        self.gaussConv = {"mG" : 1, "μT" : 0.1} # Conversions from mG
        self.rfConv = {"μW/m²" : 1, "mW/m²" : 1/1000}

        self.filename = ""
        self.prefix = "LOG"

    def newBuffer(self):
        # Create the storage buffer
        self.data = pd.DataFrame(np.zeros((self.ARRSIZE, 10)), columns=["Datetime", "CPM", "Counts", "Gauss Total [mG]", "Gauss X", "Gauss Y", "Gauss Z", "RF [μW/m²]", "Latitude", "Longitude"])
        self.data["Datetime"] = pd.to_datetime(self.data["Datetime"], unit='s')
        self.data["Latitude"] = np.nan
        self.data["Longitude"] = np.nan

    def connectDevices(self):
        # Attempt to connect all three devices
        self.geiger.begin()
        self.gauss.begin()
        self.rf.begin()

    def closeDevices(self):
        # Close all three devices
        self.geiger.end()
        self.gauss.end()
        self.rf.end()
        
    def log(self, saveData=True):
        # Get reading from each of the meters
        geigerRead = self.geiger.getReading()
        geigerCount = self.geiger.getCounts()
        gaussRead = self.gauss.getReading()
        rfRead, lat, lon = self.rf.getReading()
        
        # Get unit conversion factors from the current units
        geigerConv = self.geigerConv[self.units[0]]
        gaussConv = self.gaussConv[self.units[1]]
        rfConv = self.rfConv[self.units[2]]

        value = geigerRead*geigerConv, geigerCount, np.linalg.norm(gaussRead)*gaussConv, rfRead*rfConv # Modify the readings based on units
        timeNow = datetime.now() # Get the current datetime

        # Store the readings and time in a buffer for graphing
        self.valBuffer.append(value)
        self.timeBuffer.append(timeNow)

        # Store the readings in a pandas dataframe for saving to disk
        if (saveData):
            self.data.iloc[self.idx, 0] = np.datetime64(timeNow)
            self.data.iloc[self.idx, 1] = geigerRead # Values recorded are unaffected by changing units
            self.data.iloc[self.idx, 2] = geigerCount
            self.data.iloc[self.idx, 3] = np.linalg.norm(gaussRead)
            self.data.iloc[self.idx, 4:7] = gaussRead
            self.data.iloc[self.idx, 7] = rfRead
            self.data.iloc[self.idx, 8] = lat
            self.data.iloc[self.idx, 9] = lon

            if (self.recording): # Handle saving to file if recording is active
                self.data.iloc[[self.idx]].to_csv(self.filename, index=False, header=False, mode='a')
                self.recordIdx += 1

                if (self.recordIdx >= self.RECORDSIZE):
                    # If creating a new file automatically, the current prefix should be kept
                    self.filename = self.getNewFilename(self.prefix)

            self.idx += 1

        if (self.idx >= self.ARRSIZE): # Reset the arrays if they're filled
            self.idx = 0
            self.newBuffer()
            self.filename = self.getNewFilename()

        self.lastVal = value
        return value

    def beginRecord(self, prefix="LOG"):
        self.filename = self.getNewFilename(copyBuffer=True, prefix=prefix)
        self.recording = True
        return self.filename

    def endRecord(self):
        self.recording = False

    def changeUnits(self, units):
        geigerUnits, gaussUnits, rfUnits = units

        geigerOld = self.geigerConv[self.units[0]]
        gaussOld = self.gaussConv[self.units[1]]
        rfOld = self.rfConv[self.units[2]]

        geigerNew = self.geigerConv[geigerUnits]
        gaussNew = self.gaussConv[gaussUnits]
        rfNew = self.rfConv[rfUnits]

        # Convert every value currently in the buffer
        for i, v in enumerate(self.valBuffer):
            self.valBuffer[i] = v[0]/geigerOld*geigerNew, v[1], v[2]/gaussOld*gaussNew, v[3]/rfOld*rfNew

        self.units = units

    def config(self, avgTime=30):
        # Set the geiger counter config
        self.geiger.setAvgTime(avgTime)

    def setRFConfig(self, rfScale, rfRange):
        # Set the rf meter config
        self.rf.setConfig(rfScale, rfRange)

    def getData(self):
        # Return the current data array, but only up to the point recorded
        return self.data[:self.idx]

    def getNewFilename(self, copyBuffer=False, prefix="LOG"):
        self.prefix = prefix
        timeString= datetime.now().strftime("%Y-%m-%dT%H%M")
        filename = "logs/{}-{}.csv".format(prefix, timeString)

        # If logs folder does not exist, make one
        dir = "logs"
        if not os.path.exists(dir):
            os.makedirs(dir)

        i = 1 # If that filename already exists, add a number on the end
        while os.path.isfile(filename):
            filename = "logs/LOG-{}-{}.csv".format(timeString, i)
            i += 1
            print(i)

        # Create the header, decide whether or not to copy existing data into the file
        if copyBuffer:
            self.data.iloc[:self.idx].to_csv(filename, index=False)
            self.recordIdx = self.idx
        else:
            self.data.iloc[:0].to_csv(filename, index=False)
            self.recordIdx = 0

        return filename

    def setMaxFileLength(self, length):
        self.RECORDSIZE = length
        return 0
        




if (__name__ == "__main__"):
    d = DataLogger()
    d.connectDevices()
    d.beginRecord()
    for i in range(100):
        d.connectDevices()
        print(d.log())