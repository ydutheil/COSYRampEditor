# dictionary of elements

quadsDIC = {
    'QTov1' : 0,
    'QTov2' : 1,
    'QTov3' : 2,
    'QTov4' : 3,
    'QTov5' : 4,
    'QTov6' : 5,
    'QTov7' : 6,
    'QTov8' : 7,
    'QUov1' : 8,
    'QUov2' : 9,
    'QUov3' : 10,
    'QUov4' : 11,
    'QUov5' : 12,
    'QUov6' : 13
}
inv_quadsDIC =  {v: k for k, v in quadsDIC.iteritems()}

def set_list_quads():
    from core import MainWindow
    from datadef import RampDef
    from PyQt4.QtGui import QListWidgetItem
    MainWindow.main.Qlist_Quadrupoles.clear()
    stoneID = RampDef.testRamp.selected_stone_ID 
    
    for i in inv_quadsDIC :
        # text = inv_quads[i] + '  ' + r' %+6.4f m-2' %(RampDef.testRamp.stoneList[stoneID].quads[i])
        text = get_text_magnet(inv_quadsDIC[i],  RampDef.testRamp.stoneList[stoneID].quads[i])
        # text = r"%6s   %+6.4f m-2" %(inv_quadsDIC[i] , RampDef.testRamp.stoneList[stoneID].quads[i])
        MainWindow.main.Qlist_Quadrupoles.addItem(  QListWidgetItem( text ) )

def get_text_magnet( magnet_text, value ):
    text = r"%6s   %+6.4f m-2" %(magnet_text, value)
    return text

        
def select_magnet(item) :
    from core import MainWindow
    from datadef import RampDef
    global selected_magnet_item
    selected_magnet_item = item
    RampDef.testRamp.selected_magnet = str(item.text()).split()[0]
    MainWindow.main.magnet_strength_changer.setValue( RampDef.testRamp.stoneList[ RampDef.testRamp.selected_stone_ID ].quads[ quadsDIC[RampDef.testRamp.selected_magnet]] )
                                                      
def change_step():
    from core import MainWindow
    step = float(MainWindow.main.Magnet_stepper.text())
    MainWindow.main.magnet_strength_changer.setSingleStep(step)


def change_value_magnet():
    from core import MainWindow
    from datadef import RampDef
    new_value = MainWindow.main.magnet_strength_changer.value()
    RampDef.testRamp.stoneList[ RampDef.testRamp.selected_stone_ID ].quads[ quadsDIC[RampDef.testRamp.selected_magnet]] = new_value

    text = get_text_magnet( RampDef.testRamp.selected_magnet, new_value )
    selected_magnet_item.setText( text )

    if ( MainWindow.main.Recompute_always.checkState() == 2 ) :
        RampDef.Compute_stone_and_update( RampDef.testRamp, RampDef.testRamp.stoneList[ RampDef.testRamp.selected_stone_ID ] )
        MainWindow.main.update_plot_stone()
        
