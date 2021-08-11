from pywinusb import hid
import time
from collections import deque

class SEIInspector():

    def __init__(self):
        self.val = 0
        self.initialized = False
        self.lastRead = 0
        self.times = deque([0])
        self.i = 0
        self.avgTime = 30
        self.count = 0

    def begin(self):
        try:
            if self.initialized:
                if self.device.is_plugged():
                    return True
                else:
                    self.end()
            
            # Find the device based on VID and PID
            filter = hid.HidDeviceFilter(vendor_id = 0x1781, product_id = 0x08E9)
            self.device = filter.get_devices()[0]

            # Open the device and set our own data handler
            self.device.open()
            self.device.set_raw_data_handler(self.dataHandler)

            self.initialized = True
            return True
        
        except Exception as e:
            # Return False if the device fails to connect
            return False

    def dataHandler(self, data):
        MODE_CPM = 0
        MODE_MRH = 2
        MODE_TOT = 20

        # Pick out the relevant portions from the usb data
        val = data[6]
        mode = data[10]
        
        # Set the mode
        if mode == MODE_MRH:
            self.val = val/1e3
        elif mode == MODE_CPM:
            self.val = val
        elif mode == MODE_TOT:
            self.val = val

        if data[1] != self.lastRead or self.i > 130: # Record a count every time the reading changes, or the current one is active for 130 calls
            self.i = 0
            for i in range(data[1]):
                self.times.append(time.time())
                self.count += 1
        else:
            self.i += 1

        try: # Remove old counts from the deque
            if (time.time() - self.times[0] > self.avgTime):
                self.times.popleft()
        except:
            None
        
        self.lastRead = data[1]
       

    
    def getReading(self):
        # Return the value of counts per minute, 0 if the device is disconnected
        if (not self.isConnected()):
            return 0

        return len(self.times)*60/self.avgTime

    def getCounts(self):
        if (not self.isConnected()):
            return 0
        
        c = self.count
        self.count = 0
        return c

    def isConnected(self):
        if self.initialized:
            return self.device.is_plugged()
        return False

    def end(self):
        # Release the usb interface
        self.device.close()
        self.initialized = False

    def setAvgTime(self, t):
        self.avgTime = t

if (__name__ == "__main__"):
    se = SEIInspector()
    se.begin()
    se.avgTime = 10

    for i in range(10000):
        read = se.getReading()
        print(read)
        if read == 0 and se.isConnected():
            se.begin()
        time.sleep(1)
    
    se.end()