from PyQt4 import QtCore
import copy
class Ramp:
    def __init__(self, name, cycleLength, particle):
        self.name = name
        self.cycleLength = cycleLength
        self.particle = particle
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
        print "Ramp name is ", self.name
        print "duration is ", self.cycleLength
        print "particle is ", self.particle
        print "number of stones is ", len(self.stoneList)
        for i in range(len(self.stoneList)):
            print "stone ", i
            self.stoneList[i].printInfos()

    def change_comment(self) :
        from core import MainWindow
        self.stoneList[self.selected_stone_ID].comment = MainWindow.main.CommentStone.toPlainText()
    
        

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

# optics is
# i, s,  X_beta, Y_beta, X_alpha, Y_alpha, X_phi, Y_phi, X_eta, X_etap
# 0  1    2        3        4       5        6     7      8       9
        
    def printInfos(self):
        print "    name is ", self.name
        print "    momentum is", self.momentum
        print "    quadrupoles are", self.quads



def setRamp(loadedRamp):
    from datadef import RampDef
    global liveRamp
    liveRamp = loadedRamp

    
def Compute_and_set_all (ramp, compute=True) :
    from opticsCALC import BmadCalc
    from PyQt4.QtGui import QListWidgetItem
    from core import MainWindow

    MainWindow.main.Qlist_GeneralRampParm.clear()
    MainWindow.main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( "%s" %ramp.name ))
    MainWindow.main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( "Ramp uses %s" %ramp.particle))
    MainWindow.main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( " contains %i stones" %len(ramp.stoneList)))
    MainWindow.main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( " is %g s long" %ramp.cycleLength))

    MainWindow.main.Qlist_StoneManipulator.clear()
    for i in range(len(ramp.stoneList)):
        if compute :
            BmadCalc.get_optics( ramp.stoneList[i] )
        txt = 'Stable' if ramp.stoneList[i].stable else 'Unstable'
        item = QListWidgetItem( "%i    " %i +"%g MeV/c    " %(ramp.stoneList[i].momentum) +"%8s" %txt)
        MainWindow.main.Qlist_StoneManipulator.addItem( item )

def Compute_stone_and_update (stone) :
    from opticsCALC import BmadCalc
    from datadef import StoneEditor
    BmadCalc.get_optics( stone )
    StoneEditor.update_stone_infos_box()
    

def selec_stone( item ) :
    from core import MainWindow
    from datadef import StoneEditor
    import numpy as np
    selected_stone_ID = int(np.fromstring( item.text(), sep=' ' )[0])
    liveRamp.selected_stone_ID = selected_stone_ID
    MainWindow.main.CommentStone.setPlainText( liveRamp.stoneList[liveRamp.selected_stone_ID].comment )
    StoneEditor.update_stone_infos_box()
    
    

    
