#!/home/yann//VirtualENVs/Main/bin/python2.7 


        

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    from core import MainWindow
    
    # RampDef.setExampleRamp()
    
    
    app = QtGui.QApplication(sys.argv)

    MainWindow.doIT()
    # global main
    # main = Main()
    # RampDef.testRamp.printInfos()

    # # for i in range(len(RampDef.testRamp.stoneList)):
    # #     BmadCalc.get_optics( RampDef.testRamp, RampDef.testRamp.stoneList[i] )
    # # Plotter.plot_test(main)
    
    # # sys.exit()
    # main.show()

    # RampDef.Compute_and_set_all (RampDef.testRamp, main)


    sys.exit(app.exec_())



    
