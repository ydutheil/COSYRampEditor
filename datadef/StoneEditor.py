# dictionary of elements

quadsDIC = {
    'QT1' : 0,
    'QT2' : 1,
    'QT3' : 2,
    'QT4' : 3,
    'QT5' : 4,
    'QT6' : 5,
    'QT7' : 6,
    'QT8' : 7,
    'QU1' : 8,
    'QU2' : 9,
    'QU3' : 10,
    'QU4' : 11,
    'QU5' : 12,
    'QU6' : 13
}
inv_quadsDIC =  {v: k for k, v in quadsDIC.items()}


def set_list_quads():
    from core import MainWindow
    from datadef import RampDef
    from PyQt5.QtWidgets import QListWidgetItem
    MainWindow.main.Qlist_Quadrupoles.clear()
    stoneID = RampDef.liveRamp.selected_stone_ID 
    
    for i in inv_quadsDIC :
        # text = inv_quads[i] + '  ' + r' %+6.4f m-2' %(RampDef.liveRamp.stoneList[stoneID].quads[i])
        text = get_text_magnet(inv_quadsDIC[i],  RampDef.liveRamp.stoneList[stoneID].quads[i])
        # text = r"%6s   %+6.4f m-2" %(inv_quadsDIC[i] , RampDef.liveRamp.stoneList[stoneID].quads[i])
        MainWindow.main.Qlist_Quadrupoles.addItem(  QListWidgetItem( text ) )

def get_text_magnet( magnet_text, value ):
    text = r"%6s   %+6.4f m-2" %(magnet_text, value)
    return text

        
def select_magnet(item) :
    from core import MainWindow
    from datadef import RampDef
    global selected_magnet_item
    selected_magnet_item = item
    RampDef.liveRamp.selected_magnet = str(item.text()).split()[0]
    MainWindow.main.magnet_strength_changer.setValue( RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ].quads[ quadsDIC[RampDef.liveRamp.selected_magnet]] )
                                                      
def change_step():
    from core import MainWindow
    step = float(MainWindow.main.Magnet_stepper.text())
    MainWindow.main.magnet_strength_changer.setSingleStep(step)


def trigger_changed_magnet_value():
    from core import MainWindow
    from datadef import RampDef

    quadHookID = MainWindow.main.Qcombo_quads_link.currentIndex()
    magnet = RampDef.liveRamp.selected_magnet
    if quadHookID == 1 or quadHookID == 2:
        if magnet=='QU1' :
            set_magnet_value( 'QU1', MainWindow.main.magnet_strength_changer.value(), force_norecompute=True )
            if quadHookID == 1 :
                set_magnet_value( 'QU3', MainWindow.main.magnet_strength_changer.value(), force_norecompute=True  )
            set_magnet_value( 'QU5', MainWindow.main.magnet_strength_changer.value() )
        elif magnet=='QU2' :
            set_magnet_value( 'QU2', MainWindow.main.magnet_strength_changer.value(), force_norecompute=True  )
            if quadHookID == 1 :
                set_magnet_value( 'QU4', MainWindow.main.magnet_strength_changer.value(), force_norecompute=True  )
            set_magnet_value( 'QU6', MainWindow.main.magnet_strength_changer.value() )
        elif magnet=='QU5' or magnet=='QU6' :
            pass
        elif (magnet=='QU3' or magnet=='QU4') and quadHookID==2 :
            set_magnet_value( magnet, MainWindow.main.magnet_strength_changer.value())
    else :
        set_magnet_value( magnet, MainWindow.main.magnet_strength_changer.value())
            
        
def set_magnet_value(magnetNAME, value, force_recompute=False, force_norecompute=False) :
    from datadef import RampDef
    from core import MainWindow
    RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ].quads[ quadsDIC[magnetNAME]] = value
    text = get_text_magnet( magnetNAME, value)
    MainWindow.main.Qlist_Quadrupoles.item(quadsDIC[magnetNAME]).setText( text )
    if ( (MainWindow.main.Recompute_always.checkState() == 2 or force_recompute) and not force_norecompute ) :
        RampDef.Compute_stone_and_update( RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ] )
        MainWindow.main.update_plot_stone()

    

        
def update_stone_infos_box():
    from core import MainWindow
    from PyQt5 import QtGui, QtCore
    from datadef import RampDef

    if RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].stable is True :
        MainWindow.main.Stone_Qx.setText( "%6.4f"  %RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].Qx)
        MainWindow.main.Stone_Qx.setStyleSheet("QLineEdit { background-color : white; }")
        MainWindow.main.Stone_Qy.setText( "%6.4f"  %RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].Qy)
        MainWindow.main.Stone_Qy.setStyleSheet("QLineEdit { background-color : white; }")
    else :
        MainWindow.main.Stone_Qx.setText( "Unstable")
        MainWindow.main.Stone_Qx.setStyleSheet("QLineEdit { background-color : red; }")
        MainWindow.main.Stone_Qy.setText( "Unstable")
        MainWindow.main.Stone_Qy.setStyleSheet("QLineEdit { background-color : red; }")

    MainWindow.main.Stone_Qpx.setText( "%6.4f"  %RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].Qpx)
    MainWindow.main.Stone_Qpy.setText( "%6.4f"  %RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].Qpy)
    MainWindow.main.Stone_pc.setText( "%g MeV/c" %RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].momentum )
    MainWindow.main.Stone_time.setText( "%g ms" %(RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].timing*1000) )

    MainWindow.main.spinBox_stone.blockSignals( True )
    MainWindow.main.spinBox_stone.setValue( RampDef.liveRamp.selected_stone_ID )
    MainWindow.main.spinBox_stone.blockSignals( False )
    

# hooks ID are
# 0 for no hooks
# 1 for 1-3-5 and 2-4-6 hooked
# 2 for 1-5 and 2-6 hooked
def changeQuadsHooks(hookID, recompute=True):
    from PyQt5 import QtGui, QtCore
    from core import MainWindow
    from datadef import RampDef

    RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID].quad_link = hookID
    
    if hookID == 0 :
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU1']).setBackground( QtGui.QColor( 'white' ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU2']).setBackground( QtGui.QColor( 'white' ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU3']).setBackground( QtGui.QColor( 'white' ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU4']).setBackground( QtGui.QColor( 'white' ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU5']).setBackground( QtGui.QColor( 'white' ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU6']).setBackground( QtGui.QColor( 'white' ) )
    elif hookID == 1 :
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU1']).setBackground( QtGui.QColor( 255, 0, 0, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU3']).setBackground( QtGui.QColor( 255, 0, 0, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU5']).setBackground( QtGui.QColor( 255, 0, 0, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU2']).setBackground( QtGui.QColor( 0, 0, 255, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU4']).setBackground( QtGui.QColor( 0, 0, 255, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU6']).setBackground( QtGui.QColor( 0, 0, 255, 100 ) )
        QU1_k = RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ].quads[ quadsDIC['QU1'] ]
        set_magnet_value( 'QU3', QU1_k, force_norecompute=True)
        set_magnet_value( 'QU5', QU1_k, force_norecompute=True)
        QU2_k = RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ].quads[ quadsDIC['QU2'] ]
        set_magnet_value( 'QU4', QU2_k, force_norecompute=True)
        set_magnet_value( 'QU6', QU2_k, force_recompute= recompute ) 
    elif hookID == 2 : 
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU1']).setBackground( QtGui.QColor( 255, 0, 0, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU3']).setBackground( QtGui.QColor('white') )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU5']).setBackground( QtGui.QColor( 255, 0, 0, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU2']).setBackground( QtGui.QColor( 0, 0, 255, 100 ) )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU4']).setBackground( QtGui.QColor('white') )
        MainWindow.main.Qlist_Quadrupoles.item(quadsDIC['QU6']).setBackground( QtGui.QColor( 0, 0, 255, 100 ) )
        QU1_k = RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ].quads[ quadsDIC['QU1'] ]
        set_magnet_value( 'QU5', QU1_k, force_norecompute=True)
        QU2_k = RampDef.liveRamp.stoneList[ RampDef.liveRamp.selected_stone_ID ].quads[ quadsDIC['QU2'] ]
        set_magnet_value( 'QU6', QU2_k, force_recompute= recompute ) 
    
