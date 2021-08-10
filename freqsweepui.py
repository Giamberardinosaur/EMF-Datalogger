# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FreqSweepV2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 705)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.configControls = QtWidgets.QFrame(self.groupBox)
        self.configControls.setEnabled(True)
        self.configControls.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.configControls.setFrameShadow(QtWidgets.QFrame.Raised)
        self.configControls.setObjectName("configControls")
        self.formLayout = QtWidgets.QFormLayout(self.configControls)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.configControls)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.moduleSelector = QtWidgets.QComboBox(self.configControls)
        self.moduleSelector.setObjectName("moduleSelector")
        self.moduleSelector.addItem("")
        self.moduleSelector.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.moduleSelector)
        self.linearFreq = QtWidgets.QRadioButton(self.configControls)
        self.linearFreq.setChecked(True)
        self.linearFreq.setObjectName("linearFreq")
        self.freqStepGroup = QtWidgets.QButtonGroup(MainWindow)
        self.freqStepGroup.setObjectName("freqStepGroup")
        self.freqStepGroup.addButton(self.linearFreq)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.linearFreq)
        self.expFreq = QtWidgets.QRadioButton(self.configControls)
        self.expFreq.setObjectName("expFreq")
        self.freqStepGroup.addButton(self.expFreq)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.SpanningRole, self.expFreq)
        self.label_2 = QtWidgets.QLabel(self.configControls)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label = QtWidgets.QLabel(self.configControls)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.startFreqInput = QtWidgets.QDoubleSpinBox(self.configControls)
        self.startFreqInput.setMinimum(15.0)
        self.startFreqInput.setMaximum(6100.0)
        self.startFreqInput.setSingleStep(100.0)
        self.startFreqInput.setProperty("value", 4800.0)
        self.startFreqInput.setObjectName("startFreqInput")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.startFreqInput)
        self.endFreqInput = QtWidgets.QDoubleSpinBox(self.configControls)
        self.endFreqInput.setMinimum(15.0)
        self.endFreqInput.setMaximum(6100.0)
        self.endFreqInput.setSingleStep(100.0)
        self.endFreqInput.setProperty("value", 6100.0)
        self.endFreqInput.setObjectName("endFreqInput")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.endFreqInput)
        self.label_4 = QtWidgets.QLabel(self.configControls)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.scanTimeInput = QtWidgets.QSpinBox(self.configControls)
        self.scanTimeInput.setMinimum(1)
        self.scanTimeInput.setMaximum(10000)
        self.scanTimeInput.setSingleStep(5)
        self.scanTimeInput.setProperty("value", 10)
        self.scanTimeInput.setObjectName("scanTimeInput")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.scanTimeInput)
        self.freqStepSelectorExp = QtWidgets.QComboBox(self.configControls)
        self.freqStepSelectorExp.setObjectName("freqStepSelectorExp")
        self.freqStepSelectorExp.addItem("")
        self.freqStepSelectorExp.addItem("")
        self.freqStepSelectorExp.addItem("")
        self.freqStepSelectorExp.addItem("")
        self.freqStepSelectorExp.addItem("")
        self.freqStepSelectorExp.addItem("")
        self.freqStepSelectorExp.addItem("")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.freqStepSelectorExp)
        self.freqStepSelector = QtWidgets.QComboBox(self.configControls)
        self.freqStepSelector.setObjectName("freqStepSelector")
        self.freqStepSelector.addItem("")
        self.freqStepSelector.addItem("")
        self.freqStepSelector.addItem("")
        self.freqStepSelector.addItem("")
        self.freqStepSelector.addItem("")
        self.freqStepSelector.addItem("")
        self.freqStepSelector.addItem("")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.freqStepSelector)
        self.verticalLayout_2.addWidget(self.configControls)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.estimatorText = QtWidgets.QLabel(self.frame)
        self.estimatorText.setObjectName("estimatorText")
        self.verticalLayout.addWidget(self.estimatorText)
        self.crossCheckBox = QtWidgets.QCheckBox(self.frame)
        self.crossCheckBox.setChecked(True)
        self.crossCheckBox.setObjectName("crossCheckBox")
        self.verticalLayout.addWidget(self.crossCheckBox)
        self.logFreqBox = QtWidgets.QCheckBox(self.frame)
        self.logFreqBox.setObjectName("logFreqBox")
        self.verticalLayout.addWidget(self.logFreqBox)
        self.startButton = QtWidgets.QPushButton(self.frame)
        self.startButton.setObjectName("startButton")
        self.verticalLayout.addWidget(self.startButton)
        self.cancelButton = QtWidgets.QPushButton(self.frame)
        self.cancelButton.setEnabled(False)
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout.addWidget(self.cancelButton)
        self.errorMessage = QtWidgets.QLabel(self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.errorMessage.setPalette(palette)
        self.errorMessage.setText("")
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.errorMessage.setObjectName("errorMessage")
        self.verticalLayout.addWidget(self.errorMessage)
        self.saveButton = QtWidgets.QPushButton(self.frame)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout.addWidget(self.saveButton)
        self.loadButton = QtWidgets.QPushButton(self.frame)
        self.loadButton.setObjectName("loadButton")
        self.verticalLayout.addWidget(self.loadButton)
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame.raise_()
        self.configControls.raise_()
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.spectrumGraph = SpectrumWidget(self.groupBox_2)
        self.spectrumGraph.setObjectName("spectrumGraph")
        self.horizontalLayout_2.addWidget(self.spectrumGraph)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1360, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spectrum Analyzer"))
        self.groupBox.setTitle(_translate("MainWindow", "Options"))
        self.label_5.setText(_translate("MainWindow", "Radio Module:"))
        self.moduleSelector.setItemText(0, _translate("MainWindow", "Main: 4.8-6.1 GHz"))
        self.moduleSelector.setItemText(1, _translate("MainWindow", "Ext: 15-2700 MHz"))
        self.linearFreq.setText(_translate("MainWindow", "Linear Frequency Step [Mhz]"))
        self.expFreq.setText(_translate("MainWindow", "Exponential Frequency Step [%]"))
        self.label_2.setText(_translate("MainWindow", "End Frequency [MHz]:"))
        self.label.setText(_translate("MainWindow", "Start Frequency [MHz]:"))
        self.label_4.setText(_translate("MainWindow", "Scan Time Per Step [s]:"))
        self.freqStepSelectorExp.setItemText(0, _translate("MainWindow", "5.00"))
        self.freqStepSelectorExp.setItemText(1, _translate("MainWindow", "2.00"))
        self.freqStepSelectorExp.setItemText(2, _translate("MainWindow", "1.00"))
        self.freqStepSelectorExp.setItemText(3, _translate("MainWindow", "0.50"))
        self.freqStepSelectorExp.setItemText(4, _translate("MainWindow", "0.20"))
        self.freqStepSelectorExp.setItemText(5, _translate("MainWindow", "0.05"))
        self.freqStepSelectorExp.setItemText(6, _translate("MainWindow", "0.02"))
        self.freqStepSelector.setItemText(0, _translate("MainWindow", "6.000"))
        self.freqStepSelector.setItemText(1, _translate("MainWindow", "3.000"))
        self.freqStepSelector.setItemText(2, _translate("MainWindow", "1.000"))
        self.freqStepSelector.setItemText(3, _translate("MainWindow", "0.500"))
        self.freqStepSelector.setItemText(4, _translate("MainWindow", "0.100"))
        self.freqStepSelector.setItemText(5, _translate("MainWindow", "0.050"))
        self.freqStepSelector.setItemText(6, _translate("MainWindow", "0.020"))
        self.estimatorText.setText(_translate("MainWindow", "0 minutes, 0 seconds: 0000 data  points"))
        self.crossCheckBox.setText(_translate("MainWindow", "Show crosshair"))
        self.logFreqBox.setText(_translate("MainWindow", "Log Frequency Axis"))
        self.startButton.setText(_translate("MainWindow", "Start Scan"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel Scan"))
        self.saveButton.setText(_translate("MainWindow", "Save Scan as CSV"))
        self.loadButton.setText(_translate("MainWindow", "Load Scan from CSV..."))
        self.groupBox_2.setTitle(_translate("MainWindow", "Plots"))
from spectrumwidget import SpectrumWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
