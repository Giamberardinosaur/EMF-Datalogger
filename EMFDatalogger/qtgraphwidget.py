import pyqtgraph as pg
import numpy as np
import time
import datetime

class TimeAxisItem(pg.AxisItem):
    def __init__(self, orientation, **kwargs):
        super().__init__(orientation, **kwargs)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [self.get_tick(v, spacing) for v in values]

    def get_tick(self, ts, spacing):
        dt = datetime.datetime.fromtimestamp(ts)
        # Here you can decide on the accuracy of the time data
        # displayed depending on the spacing.
        if spacing > 60:
            return "%02d:%02d" % (dt.hour, dt.minute)
        else:
            return "%02d:%02d:%02d" % (dt.hour, dt.minute, dt.second)


class GraphWidget(pg.GraphicsWindow):

    def __init__(self, parent=None, **kargs):
        super().__init__(**kargs)
        self.setParent(parent)

        self.units = ["CPM", "mG", "μW/m²"] # Default units
        
        # Create three stacked plots, one for each meter
        self.geigerPlot = self.addPlot(labels={'left': "Geiger Counter [CPM]"}, axisItems={'bottom': TimeAxisItem(orientation='bottom', pen='k', textPen='k')})
        self.gaussPlot = self.addPlot(labels={'left': "Gauss Meter [mG]"}, axisItems={'bottom': TimeAxisItem(orientation='bottom', pen='k', textPen='k')}, row=1, col=0)
        self.rfPlot = self.addPlot(labels={'left': "RF Meter [μW/m²]", 'bottom' : "Time"}, axisItems={'bottom': TimeAxisItem(orientation='bottom', pen='k', textPen='k')}, row=2, col=0)

        # Set the coloring and style for the graphs, to match the window
        self.geigerPlot.getAxis("bottom").setStyle(showValues=False)
        self.gaussPlot.getAxis("bottom").setStyle(showValues=False)

        self.geigerPlot.getAxis("left").setPen('k')
        self.gaussPlot.getAxis("left").setPen('k')
        self.rfPlot.getAxis("left").setPen('k')

        self.geigerPlot.getAxis("left").setTextPen('k')
        self.gaussPlot.getAxis("left").setTextPen('k')
        self.rfPlot.getAxis("left").setTextPen('k')
        
        self.geigerPlot.showGrid(x=True, alpha=0.2)
        self.gaussPlot.showGrid(x=True, alpha=0.2)
        self.rfPlot.showGrid(x=True, alpha=0.2)

        self.setBackground((0xF0, 0xF0, 0xF0))

        self.geigerGraph = self.geigerPlot.plot(pen='k')
        self.gaussGraph = self.gaussPlot.plot(pen='k')
        self.rfGraph = self.rfPlot.plot(pen='k')

        self.geigerMode = 'average'

    def update(self, time, values, units):

        t = [t.timestamp() for t in time]
        geigerVals = [y[0] for y in values]
        geigerCounts = [y[1] for y in values]
        gaussVals = [y[2] for y in values]
        rfVals = [y[3] for y in values]
        
        if (self.geigerMode == 'average'): # Check whether to graph the time average or raw counts
            self.geigerGraph.setData(t, geigerVals, fillLevel=None, fillBrush=(0, 0, 0, 0), stepMode=False)
        elif (self.geigerMode == 'raw'):
            self.geigerGraph.setData(t, geigerCounts, fillLevel=0, fillBrush='k', stepMode="left")

        # Set the data for the other two graphs
        self.gaussGraph.setData(t, gaussVals)
        self.rfGraph.setData(t, rfVals)

    def changeUnits(self, units):
        # Change unit labels
        self.geigerPlot.setLabel('left', "Geiger Counter [{}]".format(units[0]))
        self.gaussPlot.setLabel('left', "Gauss Meter [{}]".format(units[1]))
        self.rfPlot.setLabel('left', "RF Meter [{}]".format(units[2]))
        self.units = units

    def changePlotMode(self, geiger=None, gauss=None):
        # Change the geiger plot mode from time averaged to raw counts
        if geiger == 'average':
            self.geigerMode = 'average'
            self.geigerPlot.setLabel('left', "Geiger Counter [{}]".format(self.units[0]))
        elif geiger == 'raw':
            self.geigerMode = 'raw'
            self.geigerPlot.setLabel('left', "Raw Counts")




        