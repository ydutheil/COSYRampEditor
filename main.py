#!/home/yann//VirtualENVs/Main/bin/python2.7 

from PyQt4.uic import loadUiType

import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from plots import Plotter

Ui_MainWindow, QMainWindow = loadUiType('RampEditor.ui')

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

        self.fig_dict_Ramp = {}
        self.Qlist_PlotSelectorRamp.itemClicked.connect(self.change_plot_ramp)
        self.Qlist_PlotSelectorStone.itemClicked.connect(self.change_plot_stone)
        
        self.figs = {}
        self.canvas = {}
        self.window = {}
        self.toolbar = {}
        self.axs = {}
        plot_names = ['RampEditor', 'StoneEditor']
        self.window['RampEditor'] = self.RampEditor_mpl
        self.window['StoneEditor'] = self.StoneEditor_mpl
        for pn in plot_names:
            fig = Figure(tight_layout=True ) #, facecolor="white", edgecolor="red")
            self.canvas[pn] = FigureCanvas(fig)
            self.toolbar[pn] = NavigationToolbar(self.canvas[pn], self.window[pn], coordinates=True)


            ax = fig.add_subplot(1, 1, 1)
            ax.grid(True)
            self.figs[pn] = fig
            self.axs[pn] = ax

        # -------------------------------------------------------------
        self.RampEditor_mpl_vl.addWidget(self.canvas['RampEditor'])
        self.RampEditor_mpl_vl.addWidget(self.toolbar['RampEditor'])
        self.StoneEditor_mpl_vl.addWidget(self.canvas['StoneEditor'])
        self.StoneEditor_mpl_vl.addWidget(self.toolbar['StoneEditor'])

    def change_plot_ramp(self, item):
        self.remove_plot('RampEditor')
        Plotter.make_plot_ramp(self, item.text(), 'RampEditor')
    def change_plot_stone(self, item):
        self.remove_plot('StoneEditor')
        Plotter.make_plot_stone(self, item.text(), 'StoneEditor')

        
    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.axs[target].grid(True)
        self.canvas[target].draw_idle()

    def remove_plot(self, target):
        self.axs[target].cla()

        

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    from datadef import RampDef
    from opticsCALC import BmadCalc


    RampDef.setExampleRamp()
    
    
    app = QtGui.QApplication(sys.argv)
    main = Main()
    RampDef.testRamp.printInfos()

    # for i in range(len(RampDef.testRamp.stoneList)):
    #     BmadCalc.get_optics( RampDef.testRamp, RampDef.testRamp.stoneList[i] )
    # Plotter.plot_test(main)
    
    # sys.exit()
    main.show()

    RampDef.Compute_and_set_all (RampDef.testRamp, main)


    sys.exit(app.exec_())



    
