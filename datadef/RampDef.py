class Ramp:
    def __init__(self, name, cycleLength, particle):
        self.name = name
        self.cycleLength = cycleLength
        self.particle = particle
        self.stoneList = []
        self.selected_stone_ID=0
        
    def add_stone(self, stone):
        self.stoneList.append(stone)

    def printInfos(self):
        print "Ramp name is ", self.name
        print "duration is ", self.cycleLength
        print "particle is ", self.particle
        print "number of stones is ", len(self.stoneList)
        for i in range(len(self.stoneList)):
            print "stone ", i
            self.stoneList[i].printInfos()
        

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

# optics is
# i, s,  X_beta, Y_beta, X_alpha, Y_alpha, X_phi, Y_phi, X_eta, X_etap
# 0  1    2        3        4       5        6     7      8       9
        
    def printInfos(self):
        print "    name is ", self.name
        print "    momentum is", self.momentum
        print "    quadrupoles are", self.quads


def setExampleRamp():
    from datadef import RampDef
    
    global testRamp
    testRamp = RampDef.Ramp("tesons", 120, "deuteron")
    testStone = RampDef.Stone(100, 150e-3, [-0.553299,  0.514285,  0.730639,  -0.67389,  -0.629671156,  0.579184782,  -0.622108141,  0.579169937,  -0.25,  0.322,  -0.25,  0.43,  -0.25,  0.322])
    testRamp.add_stone(testStone)
    testStone = RampDef.Stone(110, 200e-3, [-0.553299,  0.514285,  50.730639,  -0.67389,  -0.629671156,  0.579184782,  -0.622108141,  0.579169937,  -0.25,  0.322,  -0.25,  0.43,  -0.25,  0.322])
    testRamp.add_stone(testStone)
    testStone = RampDef.Stone(120, 250e-3, [-0.553299,  0.514285,  0.730639,  -0.67389,  -0.629671156,  0.579184782,  -0.622108141,  0.579169937,  -0.25,  0.322,  -0.25,  0.43,  -0.25,  0.322])
    testRamp.add_stone(testStone)
    # testRamp.printInfos()

    
def Compute_and_set_all (ramp, main) :
    from opticsCALC import BmadCalc
    from PyQt4.QtGui import *

    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( "%s" %ramp.name ))
    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( "Ramp uses %s" %ramp.particle))
    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( " contains %i stones" %len(ramp.stoneList)))
    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( " is %g s long" %ramp.cycleLength))

    for i in range(len(ramp.stoneList)):
        BmadCalc.get_optics( ramp, ramp.stoneList[i] )
        txt = 'Stable' if ramp.stoneList[i].stable else 'Unstable'
        item = QListWidgetItem( "%i    " %i +"%g MeV/c    " %(ramp.stoneList[i].momentum) +"%8s" %txt)
        main.Qlist_StoneManipulator.addItem( item )

    main.Qlist_StoneManipulator.itemClicked.connect(selec_stone)

def selec_stone( item ) :
    import numpy as np
    selected_stone_ID = int(np.fromstring( item.text(), sep=' ' )[0])
    testRamp.selected_stone_ID = selected_stone_ID
    print 'now selected ', testRamp.selected_stone_ID