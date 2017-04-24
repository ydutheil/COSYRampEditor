from PyQt5 import QtCore
import copy

# global particle_dict
# global particle_dict_inv
particle_dict = {
    'proton'   : 0 ,
    'deuteron' : 1
}
particle_dict_inv = {v: k for k, v in particle_dict.items()}

class Ramp:
    def __init__(self, name, cycleLength, particle):
        self.name = name
        self.cycleLength = cycleLength
        self.particle = particle_dict[particle]
        self.stoneList = []
        self.selected_stone_ID=0
        self.selected_magnet=0
        
    def add_stone(self, stone):
        self.stoneList.append(stone)

    def moove_stone_up(self):
        stone_ID = self.selected_stone_ID
        if stone_ID <= 0 or stone_ID > len(self.stoneList)-1 :
            return
        self.stoneList.insert( stone_ID-1, self.stoneList[stone_ID] )
        self.stoneList.pop( stone_ID+1 )
        Compute_and_set_all ( self, compute=False )

    def moove_stone_down(self):
        stone_ID = self.selected_stone_ID
        if stone_ID >= len(self.stoneList)-1 :
            return
        self.stoneList.insert(stone_ID+2, self.stoneList[stone_ID] )
        self.stoneList.pop( stone_ID )
        Compute_and_set_all ( self, compute=False )
        
    def remove_stone(self):
        stone_ID = self.selected_stone_ID
        if stone_ID > len(self.stoneList)-1 :
            return
        self.stoneList.pop( stone_ID )
        Compute_and_set_all ( self, compute=False )
        
    def copy_stone(self):
        stone_ID = self.selected_stone_ID
        if stone_ID > len(self.stoneList)-1 :
            return
        self.stoneList.insert(stone_ID, copy.deepcopy(self.stoneList[stone_ID]) )
        Compute_and_set_all ( self, compute=False )
        self.stoneList[self.selected_stone_ID+1].comment = "*** copy *** \r\n" + self.stoneList[self.selected_stone_ID+1].comment
        
    def printInfos(self):
        print ("Ramp name is {}".format( self.name) )
        print ("duration is {}".format( self.cycleLength) )
        print ("particle is {}".format( self.particle) )
        print ("number of stones is {}".format( len(self.stoneList)) )
        for i in range(len(self.stoneList)):
            print ("stone {}".format( i) )
            self.stoneList[i].printInfos()

    def change_comment(self) :
        from core import MainWindow
        self.stoneList[self.selected_stone_ID].comment = MainWindow.main.CommentStone.toPlainText()

    def change_particle(self, ID) :
        self.particle = ID

    def change_name( self, new_name) :
        self.name = new_name

    def get_M0( self ) : #return particle rest mass in MeV
        if self.particle == 0 : #proton
            return 938.2720813
        elif self.particle == 1 : #deuteron
            return 1875.612928
        

class Stone:
    def __init__(self, momentum, timing,  ListQuadrupolesValues, ListSextupolesValues=0, name="", Qx=0, Qy=0, Qpx=0, Qpy=0, gammaTR=0, optics=0, stable=False):
        self.momentum = momentum #in MeV/c
        self.timing = timing  #in s
        self.quads = ListQuadrupolesValues # in values of k
        self.sexts = ListSextupolesValues  # in normalized
        self.name = name
        self.Qx = Qx
        self.Qy = Qy
        self.Qpx = Qpx
        self.Qpy = Qpy
        self.gammaTR = gammaTR
        self.optics = optics
        self.stable = stable
        self.comment = "none"
        self.quad_link = 0

# optics is
# i, s,  X_beta, Y_beta, X_alpha, Y_alpha, X_phi, Y_phi, X_eta, X_etap
# 0  1    2        3        4       5        6     7      8       9
        
    def printInfos(self):
        print ("    name is {} ".format( self.name) )
        print ("    momentum is {}".format( self.momentum) )
        print ("    quadrupoles are {}".format( self.quads) )

def change_energy_stone() :
    from core import MainWindow
    liveRamp.stoneList[liveRamp.selected_stone_ID].momentum = float(MainWindow.main.StoneParm_energy.text())
    Compute_and_set_all ( liveRamp, compute=False )

def change_timing_stone() :
    from core import MainWindow
    liveRamp.stoneList[liveRamp.selected_stone_ID].timing = float(MainWindow.main.StoneParm_timing.text())/1000
    Compute_and_set_all ( liveRamp, compute=False )

    
def setRamp(loadedRamp):
    from datadef import RampDef
    global liveRamp
    liveRamp = loadedRamp

    
def Compute_and_set_all (ramp, compute=True) :
    from opticsCALC import BmadCalc
    from PyQt5.QtWidgets import QListWidgetItem
    from core import MainWindow
    
    MainWindow.main.RampParm_name.setText( "%s" %ramp.name )
    MainWindow.main.RampParm_particle.setCurrentIndex( ramp.particle )
    MainWindow.main.RampParm_Nstones.setText( "%i"  %len(ramp.stoneList) )
    MainWindow.main.RampParm_length.setText( "%g"  %ramp.cycleLength)
    

    MainWindow.main.Qlist_StoneManipulator.clear()
    for i in range(len(ramp.stoneList)):
        if compute :
            BmadCalc.get_optics( ramp.stoneList[i] )
        txt = 'Stable' if ramp.stoneList[i].stable else 'Unstable'
        item = QListWidgetItem( "%i    " %i +"%g MeV/c    " %(ramp.stoneList[i].momentum)  + " at %g ms" %(ramp.stoneList[i].timing*1000) +"%8s" %txt )
        MainWindow.main.Qlist_StoneManipulator.addItem( item )

    MainWindow.main.update_plot_ramp()
        
def Compute_stone_and_update (stone) :
    from opticsCALC import BmadCalc
    from datadef import StoneEditor
    from core import MainWindow
    BmadCalc.get_optics( stone )
    StoneEditor.update_stone_infos_box()
    MainWindow.main.update_plot_stone()

def select_stone( selected_stone_ID ) :
    from core import MainWindow
    from datadef import StoneEditor

    liveRamp.selected_stone_ID = selected_stone_ID
    MainWindow.main.CommentStone.setPlainText( liveRamp.stoneList[liveRamp.selected_stone_ID].comment )
    StoneEditor.update_stone_infos_box()

    MainWindow.main.StoneParm_energy.setText( "%g" %liveRamp.stoneList[liveRamp.selected_stone_ID].momentum )
    MainWindow.main.StoneParm_timing.setText( "%g" %(liveRamp.stoneList[liveRamp.selected_stone_ID].timing*1000) )
    
    StoneEditor.set_list_quads()
    MainWindow.main.update_plot_stone()

    MainWindow.main.Qcombo_quads_link.blockSignals( True )
    MainWindow.main.Qcombo_quads_link.setCurrentIndex(liveRamp.stoneList[liveRamp.selected_stone_ID].quad_link)
    StoneEditor.changeQuadsHooks( liveRamp.stoneList[liveRamp.selected_stone_ID].quad_link, recompute=False )
    MainWindow.main.Qcombo_quads_link.blockSignals( False )
    
