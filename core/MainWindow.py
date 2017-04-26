from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import pickle

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
        self.live_plot_ramp = 'Momentum'
      
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
        self.live_plot_ramp = item.text()
        Plotter.make_plot_ramp(item.text(), 'RampEditor')
    def change_plot_stone(self, item):
        self.remove_plot('StoneEditor')
        self.live_plot_stone = item.text()
        Plotter.make_plot_stone(item.text(), 'StoneEditor')

    def update_plot_stone(self):
        self.remove_plot('StoneEditor')
        Plotter.make_plot_stone(self.live_plot_stone, 'StoneEditor')
    def update_plot_ramp(self):
        self.remove_plot('RampEditor')
        Plotter.make_plot_ramp(self.live_plot_ramp, 'RampEditor')

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.axs[target].grid(True)
        self.canvas[target].draw_idle()

    def remove_plot(self, target):
        self.axs[target].cla()


def doIT():
    """ 
    First function called
    Set some objects and connecst signal to general functions
    """
    import numpy as np

    global main
    main = Main()
    main.show()

    main.Qlist_StoneManipulator.itemClicked.connect( lambda item : RampDef.select_stone( int(np.fromstring( item.text(), sep=' ' )[0]) ) )
    main.Qlist_Quadrupoles.itemClicked.connect(StoneEditor.select_magnet)

    main.magnet_strength_changer = MyDoubleSpinBox(main.stepper)
    main.magnet_strength_changer.setDecimals(5)
    main.magnet_strength_changer.setMinimum(-10.0)
    main.magnet_strength_changer.setMaximum(10.0)
    main.magnet_strength_changer.setObjectName("magnet_strength_changer")
    main.stepper_layout.addWidget(main.magnet_strength_changer)

    main.spinBox_stone = MySpinBox( main.stoneStepper )
    main.spinBox_stone.setObjectName("spinBox_stone")
    main.stoneStepper_layout.addWidget(main.spinBox_stone)

    step = 0.001
    main.magnet_strength_changer.setSingleStep(step)
    main.Magnet_stepper.setText( str(step) )
    main.Magnet_stepper.editingFinished.connect( StoneEditor.change_step )
    main.magnet_strength_changer.valueChanged.connect( StoneEditor.trigger_changed_magnet_value)

    main.spinBox_stone.valueChanged.connect( RampDef.select_stone  )

    main.Save_Ramp.triggered.connect( save_ramp )
    main.Load_Ramp.triggered.connect( load_ramp )
    main.Create_new_ramp.triggered.connect( NewRamp )

    

def save_ramp():
    """ Connected to Menu save ramp """
    from datadef import RampDef
    name = QtWidgets.QFileDialog.getSaveFileName()
    file_ramp = open( name[0] , 'wb')
    pickle.dump(RampDef.liveRamp, file_ramp)

    file_ramp.close()


def load_ramp():
    """ Connected to Menu load ramp """
    name = QtWidgets.QFileDialog.getOpenFileName()
    file_ramp = open( name[0] , 'rb')
    RampDef.setRamp(pickle.load( file_ramp))
    file_ramp.close()

    RampDef.Compute_and_set_all (RampDef.liveRamp)
    connect_ramp_buttons()
    



def NewRamp():
    """ Connected to Menu new ramp, generates a single stable stone """
    newramp = RampDef.Ramp("tesons", 120, "deuteron")
    testStone = RampDef.Stone(100, 150e-3, [-0.553299,  0.514285,  0.730639,  -0.67389,  -0.629671156,  0.579184782,  -0.622108141,  0.579169937,  -0.25,  0.322,  -0.25,  0.43,  -0.25,  0.322])
    newramp.add_stone(testStone)
    RampDef.setRamp( newramp )
    RampDef.Compute_and_set_all (RampDef.liveRamp)
    connect_ramp_buttons()


def connect_ramp_buttons() :
    """
    Function called after the ramp is initialized
    links signals to the Ramp methods once it is created
    """
    main.Up.clicked.connect( RampDef.liveRamp.moove_stone_up)
    main.Down.clicked.connect( RampDef.liveRamp.moove_stone_down)
    main.Remove.clicked.connect( RampDef.liveRamp.remove_stone)
    main.Copy.clicked.connect( RampDef.liveRamp.copy_stone)

    main.CommentStone.textChanged.connect(RampDef.liveRamp.change_comment)
    RampDef.liveRamp.printInfos()
    # RampDef.Compute_and_set_all (RampDef.liveRamp)
    StoneEditor.set_list_quads()

    main.RampParm_particle.currentIndexChanged.connect( RampDef.liveRamp.change_particle )
    main.RampParm_name.textChanged.connect( RampDef.liveRamp.change_name )

    main.StoneParm_energy.returnPressed.connect( RampDef.change_energy_stone )
    main.StoneParm_timing.returnPressed.connect( RampDef.change_timing_stone )

    main.Qcombo_quads_link.currentIndexChanged.connect( StoneEditor.changeQuadsHooks )

    main.RecomputeRampNow.clicked.connect( lambda signal : RampDef.Compute_and_set_all( RampDef.liveRamp ) )
    main.RecomputeStoneNow.clicked.connect( lambda signal : RampDef.Compute_stone_and_update( RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ] ) )

    

# redifined a personal QDoubleSpinBox due to double event trigger when the computation (here caomputation of the optics by Bmad) takes too long
# http://www.qtcentre.org/archive/index.php/t-43078.html
# It behaves exactly like QDoubleSpinBox but I redifine the timerEvent and do nothing with it
# consequence : event only triggered once when click stays pushed
class MyDoubleSpinBox (QtWidgets.QDoubleSpinBox):

    def timerEvent( self, dummy ):
        pass


class MySpinBox (    QtWidgets.QSpinBox ) :

    def timerEvent( self, dummy ):
        pass

    
