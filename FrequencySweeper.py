from PyQt5 import QtCore, QtGui, QtWidgets 
import RFExplorer as rf
from freqsweepui import Ui_MainWindow
import serial.tools.list_ports
import time
import numpy as np
from datetime import datetime
import os

class SpectrumWindowWrapper(Ui_MainWindow): # The GUI thread for the spectrum analyzer
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.spectrumData = None
        self.inProgress = False

        # Attach inputs to handlers
        self.startFreqInput.valueChanged.connect(self.configHandler)
        self.endFreqInput.valueChanged.connect(self.configHandler)
        self.freqStepSelector.activated.connect(self.configHandler)
        self.freqStepSelectorExp.activated.connect(self.configHandler)
        self.scanTimeInput.valueChanged.connect(self.configHandler)
        self.moduleSelector.activated.connect(self.configHandler)
        self.freqStepGroup.buttonClicked.connect(self.configHandler)
        self.freqStepGroup.buttonClicked.connect(self.lockoutStepSelector)

        self.configHandler()
        self.lockoutStepSelector()
        self.freqLimitHandler()

        self.startButton.pressed.connect(self.startHandler)
        self.saveButton.pressed.connect(self.saveHandler)
        self.loadButton.pressed.connect(self.loadHandler)
        self.crossCheckBox.stateChanged.connect(self.crosshairHandler)
        self.logFreqBox.stateChanged.connect(self.logBoxHandler)
        self.freqStepGroup.buttonClicked.connect(self.configHandler)
        self.moduleSelector.activated.connect(self.freqLimitHandler)


    # Event handler functions
    def configHandler(self):
        modules = ["main", "ext"]
        isLinear = {self.linearFreq : True, self.expFreq : False}

        start = self.startFreqInput.value()
        end = self.endFreqInput.value()
        time = self.scanTimeInput.value()
        module = modules[self.moduleSelector.currentIndex()]
        linear = isLinear[self.freqStepGroup.checkedButton()]

        if linear:
            step = float(self.freqStepSelector.currentText())
        else:
            step = float(self.freqStepSelectorExp.currentText())/100
        
        if (start >= end):
            return

        self.config = ScanConfig(start, end, step, time, module, linear)

        self.estimatorText.setText(self.config.estimator())

        self.freq = self.config.freq

    def startHandler(self):
        if (self.inProgress):
            return
        
        self.configControls.setDisabled(True)
        self.loadButton.setDisabled(True)
        self.startButton.setDisabled(True)
        self.cancelButton.setDisabled(False)

        self.thread = QtCore.QThread()
        self.worker = SpectrumWorker(self.config)          

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.values.connect(self.updateWindow)
        self.worker.error.connect(self.errorHandler)
        self.worker.progress.connect(self.progressHandler)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.endScan)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.cancelButton.pressed.connect(self.worker.end)


        self.thread.start()
        self.inProgress = True
    
    def endScan(self):
        self.inProgress = False
        self.configControls.setEnabled(True)
        self.loadButton.setEnabled(True)
        self.startButton.setEnabled(True)
        self.cancelButton.setEnabled(False)

    def saveHandler(self):
        if self.spectrumData is not None:
            filename = self.getNewFilename()
            np.savetxt(filename, np.transpose([self.freq, self.spectrumData]),delimiter=",", header="Frequency [Hz], Power [dBm]", fmt='%f')
        else:
            self.errorHandler("No data found")

    def loadHandler(self):
        try:
            filename, filetype = QtWidgets.QFileDialog.getOpenFileName()
            print(filename)
            self.loadCSV(filename)
        except:
            self.errorHandler("Invalid data file")

    def errorHandler(self, msg):
        self.errorMessage.setText(msg)
        self.errorTimer = QtCore.QTimer()
        self.errorTimer.setInterval(10000)
        self.errorTimer.timeout.connect(lambda : self.errorMessage.setText(""))
        self.errorTimer.start()

    def progressHandler(self, p):
        self.progressBar.setValue(int(p*100))

    def crosshairHandler(self, state):
        self.spectrumGraph.setCrosshairVisible(state == 2)
    
    def logBoxHandler(self, state):
        self.spectrumGraph.setLogAxis(state)

    def freqLimitHandler(self):
        modules = ["main", "ext"]
        module = modules[self.moduleSelector.currentIndex()]

        if module == "main":
            self.setFrequencyLimits(4850, 6100)
        elif module == "ext":
            self.setFrequencyLimits(15, 2700)

    # Graph update function 
    def updateWindow(self, data):
        self.spectrumGraph.update(self.freq[:data.size], data)
        self.spectrumData = data

    def setFrequencyLimits(self, minFreq, maxFreq):
        self.startFreqInput.setMinimum(minFreq)
        self.startFreqInput.setMaximum(maxFreq)
        self.startFreqInput.setValue(minFreq)

        self.endFreqInput.setMinimum(minFreq)
        self.endFreqInput.setMaximum(maxFreq)
        self.endFreqInput.setValue(maxFreq)

    def lockoutStepSelector(self):
        isLinear = {self.linearFreq : True, self.expFreq : False}
        linear = isLinear[self.freqStepGroup.checkedButton()]

        self.freqStepSelector.setEnabled(linear)
        self.freqStepSelectorExp.setEnabled(not linear)

    # File IO functions
    def getNewFilename(self):
        timeString = datetime.now().strftime("%Y-%m-%dT%H%M")
        filename = "logs/SWEEP-{}.csv".format(timeString)

         # If logs folder does not exist, make one
        dir = "logs"
        if not os.path.exists(dir):
            os.makedirs(dir)

        i = 1 # If that filename already exists, add a number on the end
        while os.path.isfile(filename):
            filename = "logs/SWEEP-{}-{}.csv".format(timeString, i)
            i += 1
            print(i)

        return filename

    def loadCSV(self, filename):
        data = np.loadtxt(filename, delimiter=',', skiprows=1)
        self.freq = data[:, 0]
        self.updateWindow(data[:, 1])

    
class ScanConfig(): # A data structure to store the parameters of a scan
    start = 0
    end = 0
    step = 0
    time = 0

    def __init__(self, start, end, step, time, module="main", linear=True):
        self.start = start   # Starting frequency, in Hz
        self.end = end       # End frequency, in Hz
        self.step = step     # Maximum Frequency step, in Hz
        self.time = time     # Scan time per interval, in s
        self.module = module # Module to use for the scan, "main" or "ext"
        self.linear = linear # True if the intervals are linearly spaced, false if exponential

        if linear:
            self.freqRanges = self.genLinearFreq()
        else:
            self.freqRanges = self.genLogFreq()

        self.genFrequencies(self.freqRanges)

    def estimator(self):
        totalTime = self.intervals*(self.time + 1)
        minutes, seconds = divmod(totalTime, 60)

        return "{} minutes, {} seconds: {} data points".format(int(minutes), int(seconds), self.points)

    def genLinearFreq(self):
        self.span = min(self.step*112, 600)                             # Span of each individual frequency range
        self.intervals = int(np.ceil((self.end-self.start)/self.span))  # Number of frequency ranges needed to span from start to end
        self.points = self.intervals*112                                # Number of data points to be collected

        allFreq  = np.linspace(self.start, self.end, self.intervals+1)
        ranges = np.zeros((self.intervals, 2))
        ranges[:, 0] = allFreq[:-1]
        ranges[:, 1] = allFreq[1:]
        return ranges

    def genLogFreq(self):
        self.intervals = int(np.ceil(np.log(self.end/self.start)/np.log(1+self.step)/112))
        self.points = self.intervals*112
        allFreq = np.logspace(np.log10(self.start), np.log10(self.end), self.intervals+1)

        ranges = np.zeros((self.intervals, 2))
        ranges[:, 0] = allFreq[:-1]
        ranges[:, 1] = allFreq[1:]

        return ranges

    def genFrequencies(self, ranges):
        self.freq = np.zeros(112*self.intervals)
        for i, r in enumerate(ranges):
            start, end = r
            self.freq[i*112:(i+1)*112] = np.linspace(start, end, 112)*1e6



    

class SpectrumWorker(QtCore.QObject): # The worker thread for collecting data from the RF Explorer
    values = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(float)
    error = QtCore.pyqtSignal(object)
    finished = QtCore.pyqtSignal()

    BAUDRATE = 500000

    def __init__(self, config):
        super().__init__()

        self.config = config
        self.data = np.zeros(self.config.points)

        self.i = -1
        self.startTime = -10000

    def connect(self):
        explorer = rf.RFECommunicator()
        explorer.GetConnectedPorts()
        if not explorer.ConnectPort(self.searchPorts(), self.BAUDRATE):
            raise Exception()

        return explorer

    def searchPorts(self):
        # Search all serial ports based on Vendor ID and Product ID for the RF Explorer
        for p in serial.tools.list_ports.comports():
            if p.vid == 0x10C4 and p.pid == 0xEA60:
                return p.name
        return None
    
    def setActiveModule(self, module):
        # Send the command to set which module is in use, then wait for it to take effect
        if module == "main":
            self.explorer.SendCommand('CM\x00')
        elif module == "ext":
            self.explorer.SendCommand('CM\x01')
        time.sleep(5)


    def run(self):

        try:
            self.explorer = self.connect()
        except:
            self.error.emit("Device not found")
            self.end()
            return

        self.setActiveModule(self.config.module)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.scanRange)
        self.timer.start()
            

    def scanRange(self):
        try:
            # Allow waiting time between scans
            if time.time() - self.startTime >= (self.config.time + 1):
                self.i += 1
                if self.i >= self.config.freqRanges.shape[0]:
                    self.end()
                    return 
                
                # Set the progrss bar
                self.progress.emit((self.i + 1)/self.config.freqRanges.shape[0])

                # Set the frequency range on the device
                minFreq, maxFreq = self.config.freqRanges[self.i]
                self.explorer.UpdateDeviceConfig(minFreq, maxFreq)
                self.startTime = time.time()
                self.explorer.SweepData.CleanAll()

            self.explorer.ProcessReceivedString(True)
            if (self.explorer.SweepData.Count > 0):
                # Collect the scan data from the device and emit it
                self.data[self.i*112:(self.i+1)*112] = self.explorer.SweepData.MaxHoldData.m_arrAmplitude
                self.values.emit(self.data[:(self.i+1)*112])

        except Exception as e:
            # Disconnect the device properly if communication is interrupted
            print(e)
            self.end()

    @QtCore.pyqtSlot()
    def end(self):
        try:
            self.timer.stop()
            self.explorer.Close()
        except:
            pass
        self.progress.emit(0)
        self.finished.emit()

                

if __name__ == "__main__":
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SpectrumWindowWrapper()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())