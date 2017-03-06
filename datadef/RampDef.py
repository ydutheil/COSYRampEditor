
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



# from PyQt4.uic import loadUiType
    
# test, qwidget = loadUiType('stoneWidget.ui')


import sys
from PyQt4 import QtGui, QtCore

class stoneWidget(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(stoneWidget, self).__init__(parent)

        
        self.allQHBoxLayout  = QtGui.QHBoxLayout()
        
        self.textcell    = QtGui.QLabel()
        self.allQHBoxLayout.addWidget(self.textcell)

        self.comment = QtGui.QLineEdit()
        self.allQHBoxLayout.addWidget(self.comment)

        # self.up = QtGui.QPushButton('up')
        # self.down = QtGui.QPushButton('down')         
        # self.allQHBoxLayout.addWidget(self.up)
        # self.allQHBoxLayout.addWidget(self.down)
        
        # self.copy = QtGui.QPushButton('copy')
        # self.allQHBoxLayout.addWidget(self.copy)
        
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet

  

        

def Compute_and_set_all (ramp, main) :
    from opticsCALC import BmadCalc
    from  PyQt4.QtGui import QListWidgetItem
    from PyQt4 import QtGui

    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( "%s" %ramp.name ))
    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( "Ramp uses %s" %ramp.particle))
    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( " contains %i stones" %len(ramp.stoneList)))
    main.Qlist_GeneralRampParm.addItem(  QListWidgetItem( " is %g s long" %ramp.cycleLength))


    
    for i in range(len(ramp.stoneList)):
        BmadCalc.get_optics( ramp, ramp.stoneList[i] )
        txt = 'Stable' if ramp.stoneList[i].stable else 'Unstable'
        stone = stoneWidget()
        stone.textcell.setText( "%i    " %i +"%g MeV/c    " %(ramp.stoneList[i].momentum) +"%8s" %txt )

        ListItem = QListWidgetItem(main.Qlist_StoneManipulator)
        ListItem.setSizeHint(stone.sizeHint())
        main.Qlist_StoneManipulator.addItem(ListItem)
        main.Qlist_StoneManipulator.setItemWidget( ListItem, stone )
        
        # item = QListWidgetItem( "%i    " %i +"%g MeV/c    " %(ramp.stoneList[i].momentum) +"%8s" %txt)
        # main.Qlist_StoneManipulator.addItem( item )


    def selec_stone( ) :
        selected_stone_ID = main.Qlist_StoneManipulator.currentRow() #int(np.fromstring( item.text(), sep=' ' )[0])
        testRamp.selected_stone_ID = selected_stone_ID
        print 'now selected ', testRamp.selected_stone_ID

    def copy_stone ( ) :
        print 'laa'
        
        
    main.Qlist_StoneManipulator.itemClicked.connect(selec_stone)


# from PyQt4 import QtGui
# import sys

# filenames = []

# class TestGui(QtGui.QWidget):
#     """ A Fast test gui show how to create buttons in a ScrollArea"""
#     def __init__(self):
#         super(TestGui, self).__init__()
#         self.lay = QtGui.QHBoxLayout()
#         self.sA = QtGui.QScrollArea()
#         self.sA_lay = QtGui.QVBoxLayout()
#         self.sA.setLayout(self.sA_lay)
#         self.closeGui = QtGui.QPushButton("Close")
#         self.add_file_button = QtGui.QPushButton("Add File")
#         self.lay.addWidget(self.closeGui)
#         self.lay.addWidget(self.add_file_button)
#         self.lay.addWidget(self.sA)
#         self.setLayout(self.lay)
#         self.connect_()
#         self.show()

#     def connect_(self):
#         self.add_file_button.clicked.connect(self.__add_file_to_list)
#         self.closeGui.clicked.connect(self.close)
#         return

#     def __add_file_to_list(self):
#         fname = QtGui.QFileDialog.getOpenFileName()
#         global filenames
#         filenames.append(fname)
#         button = QtGui.QPushButton(fname)
#         self.sA_lay.addWidget(button)
#         return

    # # Create QCustomQWidget
    # myQCustomQWidget = QCustomQWidget()
    # myQCustomQWidget.text.setText('lala')
    # # Create QListWidgetItem
    # myQListWidgetItem = QtGui.QListWidgetItem(main.Qlist_StoneManipulator)
    # # Set size hint
    # myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
    # # Add QListWidgetItem into QListWidget
    # main.Qlist_StoneManipulator.addItem(myQListWidgetItem)
    # main.Qlist_StoneManipulator.setItemWidget(myQListWidgetItem, myQCustomQWidget)
    

# from PyQt4.QtCore import *
# from PyQt4.QtGui import *

    # list_data = [1,2,3,4]
    # lm = MyListModel(list_data)
    # de = MyDelegate()
    # main.Qlist_StoneManipulator.setModel(lm)
    # main.Qlist_StoneManipulator.setItemDelegate(de)


# class MyDelegate(QItemDelegate):
#     def __init__(self, parent=None, *args):
#         QItemDelegate.__init__(self, parent, *args)

#     # def paint(self, painter, option, index):
#     #     painter.save()

#     #     # set background color
#     #     painter.setPen(QPen(Qt.NoPen))
#     #     if option.state & QStyle.State_Selected:
#     #         painter.setBrush(QBrush(Qt.red))
#     #     else:
#     #         painter.setBrush(QBrush(Qt.white))
#     #     painter.drawRect(option.rect)

#     #     # set text color
#     #     painter.setPen(QPen(Qt.black))
#     #     value = index.data(Qt.DisplayRole)
#     #     if value.isValid():
#     #         text = value.toString()
#     #         painter.drawText(option.rect, Qt.AlignLeft, text)

#     #     painter.restore()

# ####################################################################
# class MyListModel(QAbstractListModel):
#     def __init__(self, datain, parent=None, *args):
#         """ datain: a list where each item is a row
#         """
#         QAbstractTableModel.__init__(self, parent, *args)
#         self.listdata = datain

#     def rowCount(self, parent=QModelIndex()):
#         return len(self.listdata)

#     def data(self, index, role):
#         if index.isValid() and role == Qt.DisplayRole:
#             return QVariant(self.listdata[index.row()])
#         else:
#             return QVariant()
