from PyQt5 import QtCore, QtGui, QtWidgets
from DataLogger import DataLogger
from autogenui import Ui_MainWindow
from FreqSweepUI import SpectrumWindowWrapper
from pandasmodel import PandasModel
import time
import os

class MainWindowWrapper(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.units = ("CPM", "mG", "μW/m²")

        # Set up data logging
        self.logger = DataLogger()
        self.logger.connectDevices()

        # Attach button events to their handlers
        self.recButton.clicked.connect(self.recordHandler)
        self.geigerUnits.activated.connect(self.changeUnits)
        self.gaussUnits.activated.connect(self.changeUnits)
        self.rfUnits.activated.connect(self.changeUnits)

        self.geigerModeButtonGroup.buttonClicked.connect(self.changePlotMode)
        self.rfAdapterButtonGroup.buttonClicked.connect(self.setRFConfig)
        self.rfRange.buttonClicked.connect(self.setRFConfig)
        self.maxSampleSelector.currentTextChanged.connect(self.setMaxFileLength)

        # Attach menu options
        self.avgTimeMenu.triggered.connect(self.changeAvg)

        # Setup the table view
        self.logTable.horizontalHeader().setDefaultSectionSize(60)
        self.logTable.setShowGrid(False)

        # Start the worker thread to collect data without interrupting the GUI thread
        self.thread = QtCore.QThread()
        self.worker = Worker(self.logger)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.values.connect(self.updateWindow)
        self.intervalSelector.activated.connect(self.worker.setInterval)
        self.thread.start()

        # Start the second window, but keep it hidden for now
        self.spectrumWindow = QtWidgets.QMainWindow()
        self.spectrumUI = SpectrumWindowWrapper()
        self.spectrumUI.setupUi(self.spectrumWindow)

        self.spectrumButton.clicked.connect(self.spectrumWindow.show)

    def updateWindow(self, val):
        # Update LCDs
        self.geigerLCD.setProperty("value", val[0])
        self.gaussLCD.setProperty("value",  float(round(val[2], 2)))
        self.rfLCD.setProperty("value",  val[3])

        # Update Indicators
        self.setIndicator(self.logger.geiger.isConnected(), self.geigerIndicator)
        self.setIndicator(self.logger.gauss.isConnected(), self.gaussIndicator)
        self.setIndicator(self.logger.rf.isConnected(), self.rfIndicator)

        # Update graphs
        self.graph.update(self.logger.timeBuffer, self.logger.valBuffer, self.units)

        # Update log view
        autoscroll = self.logTable.verticalScrollBar().value() == self.logTable.verticalScrollBar().maximum()
        self.tableModel = PandasModel(self.logger.getData())
        self.logTable.setModel(self.tableModel)
        #self.logTable.setColumnWidth(0, 90)
        #self.logTable.setColumnWidth(3, 90)
        self.logTable.show()

        if autoscroll:
            self.logTable.scrollToBottom()
        

    def setIndicator(self, val, indicator):
        if val:
            indicator.setStyleSheet("\nborder: 0px solid #555;\nborder-radius: 8px;\nborder-style: outset;\nbackground-color: rgb(0, 255, 0);\npadding: 5px;")
        else:
            indicator.setStyleSheet("\nborder: 0px solid #555;\nborder-radius: 8px;\nborder-style: outset;\nbackground-color: rgb(255, 0, 0);\npadding: 5px;")

    def recordHandler(self):
        if self.recButton.isChecked():
            prefix = self.filenameEdit.text()
            filename = self.logger.beginRecord(prefix=prefix)
            self.filenameLabel.setText("Recording to {}".format(filename))
            self.filenameEdit.setText("")
        else:
            self.logger.endRecord()
            self.filenameLabel.setText("Not currently logging to file.") 

    def changeUnits(self):
        # Get the current values from each of the combo boxes
        geigerUnits = str(self.geigerUnits.currentText())
        gaussUnits = str(self.gaussUnits.currentText())
        rfUnits = str(self.rfUnits.currentText())
        self.units = geigerUnits, gaussUnits, rfUnits

        # Change the units the logger is using
        self.logger.changeUnits(self.units)

        # Change the graph units
        self.graph.changeUnits(self.units)

    def changeAvg(self):
        action = self.avgTimeMenu.checkedAction()
        times = {self.avg10s : 10, self.avg30s : 30, self.avg60s : 60}
        self.logger.config(avgTime=times[action])

    def changePlotMode(self, button):
        geigerMode = {self.timeAvgMode : 'average', self.rawCountMode : 'raw'}

        self.graph.changePlotMode(geiger=geigerMode[button])

    def setRFConfig(self):
        scaleDict = {self.rf0db : 1,  self.rfMinus20db : 100, self.rfPlus20dB : 1/100}
        rangeDict = {self.rfRangeMax : 10, self.rfRangeMin: 1}
        
        rfScale = scaleDict[self.rfAdapterButtonGroup.checkedButton()]
        rfRange = rangeDict[self.rfRange.checkedButton()]
        self.logger.setRFConfig(rfScale, rfRange)

    def setMaxFileLength(self, option):
        value = int(option)
        print(value)

        self.logger.setMaxFileLength(value)



        


class Worker(QtCore.QObject):
    values = QtCore.pyqtSignal(object)

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.interval = 1
        self.count = 0

    @QtCore.pyqtSlot(int)
    def setInterval(self, idx):
        intList = [1, 2, 5, 10, 15, 30]
        self.interval = intList[idx]

    def run(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.start()
        self.timer.timeout.connect(self.update)


    def update(self):
        self.logger.connectDevices()
        values = self.logger.log(saveData=(self.count%self.interval == 0))
        self.values.emit(values)
        self.count += 1





if __name__ == "__main__":
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowWrapper()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())