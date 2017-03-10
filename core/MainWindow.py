from PyQt4.uic import loadUiType

import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from plots import Plotter
from datadef import RampDef
from opticsCALC import BmadCalc
from datadef import StoneEditor
Ui_MainWindow, QMainWindow = loadUiType('RampEditor.ui')

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

        self.fig_dict_Ramp = {}
        self.Qlist_PlotSelectorRamp.itemClicked.connect(self.change_plot_ramp)
        self.Qlist_PlotSelectorStone.itemClicked.connect(self.change_plot_stone)

        self.live_plot_stone = 'Beta'
      
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
        Plotter.make_plot_ramp(item.text(), 'RampEditor')
    def change_plot_stone(self, item):
        self.remove_plot('StoneEditor')
        self.live_plot_stone = item.text()
        Plotter.make_plot_stone(item.text(), 'StoneEditor')

    def update_plot_stone(self):
        self.remove_plot('StoneEditor')
        Plotter.make_plot_stone(self.live_plot_stone, 'StoneEditor')
        
        
    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.axs[target].grid(True)
        self.canvas[target].draw_idle()

    def remove_plot(self, target):
        self.axs[target].cla()


def doIT():
    from PyQt4 import QtCore
    import pickle
    global main
    main = Main()
    main.show()

    RampDef.setExampleRamp()

    main.Up.clicked.connect( RampDef.testRamp.moove_stone_up)
    main.Down.clicked.connect( RampDef.testRamp.moove_stone_down)
    main.Remove.clicked.connect( RampDef.testRamp.remove_stone)
    main.Copy.clicked.connect( RampDef.testRamp.copy_stone)
    main.Qlist_StoneManipulator.itemClicked.connect(RampDef.selec_stone)

    main.CommentStone.textChanged.connect(RampDef.testRamp.change_comment)
    main.Qlist_Quadrupoles.itemClicked.connect(StoneEditor.select_magnet)

    step = 0.001
    main.magnet_strength_changer.setSingleStep(step)
    main.Magnet_stepper.setText( str(step) )
    main.Magnet_stepper.editingFinished.connect( StoneEditor.change_step )
    main.magnet_strength_changer.valueChanged.connect( StoneEditor.change_value_magnet )

    
    RampDef.testRamp.printInfos()
    RampDef.Compute_and_set_all (RampDef.testRamp)
    StoneEditor.set_list_quads()

    main.Save_Ramp.triggered.connect( save_ramp )
    

def save_ramp():
    from PyQt4 import QtGui
    from datadef import RampDef
    name = QtGui.QFileDialog.getSaveFileName()
    file_ramp = open( name , 'w')
    pickle.dump(RampDef.testRamp, file_ramp)

    file.close()
    


    
    


    
