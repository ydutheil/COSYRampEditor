#!/home/yann/VirtualENVs/Python3.5.2_main/bin/python

        

if __name__ == '__main__':
    import sys
    from PyQt5 import QtGui, QtWidgets
    from core import MainWindow
    
    # RampDef.setExampleRamp()
    
    
    app = QtWidgets.QApplication(sys.argv)

    MainWindow.doIT()
    # global main
    # main = Main()
    # RampDef.liveRamp.printInfos()

    # # for i in range(len(RampDef.liveRamp.stoneList)):
    # #     BmadCalc.get_optics( RampDef.liveRamp, RampDef.liveRamp.stoneList[i] )
    # # Plotter.plot_test(main)
    
    # # sys.exit()
    # main.show()

    # RampDef.Compute_and_set_all (RampDef.liveRamp, main)


    sys.exit(app.exec_())



    
