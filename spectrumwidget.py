import pyqtgraph as pg
import numpy as np

class SpectrumWidget(pg.GraphicsWindow):
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'w')

    def __init__(self, parent=None, **kargs):
        super().__init__(**kargs)
        self.setParent(parent)

        # Create a new plot
        self.spectrumPlot = self.addPlot()

        # Set labels and units
        self.spectrumPlot.getAxis('bottom').setLabel("Frequency", units="Hz")
        self.spectrumPlot.getAxis('left').setLabel("Power", units="dBm")
        self.spectrumPlot.getAxis('bottom').enableAutoSIPrefix(True)

        self.graph = self.spectrumPlot.plot()

        # Setup signals for mouse movement
        self.crosshairUpdate = pg.SignalProxy(self.spectrumPlot.scene().sigMouseMoved, rateLimit=60, slot=self.drawCrosshair)
        self.crossVLine = pg.InfiniteLine()
        self.crossHLine = pg.InfiniteLine(angle=0)
        self.coords = pg.TextItem(anchor=(0, 1), fill='k')
        
        # Add the components of the crosshair
        self.spectrumPlot.addItem(self.coords, ignoreBounds=True)
        self.spectrumPlot.addItem(self.crossVLine, ignoreBounds=True)
        self.spectrumPlot.addItem(self.crossHLine, ignoreBounds=True)

        

        self.logXAxis = False
    

    def update(self, freq, mag):
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'w')

        self.graph.setData(freq, mag, fillLevel=min(mag), brush='w', stepMode="left")

    def drawCrosshair(self, event):
        coordinates = event[0]
        if self.spectrumPlot.sceneBoundingRect().contains(coordinates):
            # Find mouse coordinates and map them to view coordinates
            mousePos = self.spectrumPlot.vb.mapSceneToView(coordinates)
            
            # Draw the crosshair
            self.crossVLine.setPos(mousePos.x())
            self.crossHLine.setPos(mousePos.y())
            
            # Adjust the cursor if the x axis is in log mode
            if not self.logXAxis:
                cursorFreq = mousePos.x()
            else:
                cursorFreq = 10**mousePos.x()

            # Draw the crosshair label
            self.coords.setPlainText("{}, {:.2f} dBm".format(pg.siFormat(cursorFreq, precision=6, suffix="Hz"), mousePos.y()))
            self.coords.setPos(mousePos)

    def setCrosshairVisible(self, visible):
        if visible:
            self.crossVLine.show()
            self.crossHLine.show()
            self.coords.show()
        else:
            self.crossVLine.hide()
            self.crossHLine.hide()
            self.coords.hide()

    def setLogAxis(self, log):
        self.spectrumPlot.setLogMode(x=log)
        self.logXAxis = log


