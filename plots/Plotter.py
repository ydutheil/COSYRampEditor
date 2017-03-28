from datadef import RampDef

import random
import numpy as np


def plot_test():

    RampDef.liveRamp.printInfos()

    
    MainWindow.main.draw_plot('RampEditor',  [random.random() for i in range(10)])
    MainWindow.main.draw_plot('StoneEditor', [random.random() for i in range(100)])

    MainWindow.main.remove_plot('RampEditor')
    MainWindow.main.draw_plot('RampEditor',  [random.random() for i in range(150)])

    
def make_plot_ramp(plot_name, window):
    from core import MainWindow
    ax = MainWindow.main.axs[window] 
    can  = MainWindow.main.canvas[window]

    Ramp =  RampDef.liveRamp
    timings, y1, y2  = [], [], []
    for i in range(len(Ramp.stoneList)) :
        timings.append(Ramp.stoneList[i].timing)

    
    if plot_name == 'Momentum'  :
        for i in range(len(Ramp.stoneList)) :
            y1.append(Ramp.stoneList[i].momentum)
        
        ax.plot(timings, y1, '--x', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Timing (ms)')
        ax.set_ylabel('Momentum (MeV/c)')
        can.draw_idle()
        
    elif plot_name == 'Tune' :
        for i in range(len(Ramp.stoneList)) :
            y1.append(Ramp.stoneList[i].Qx)
            y2.append(Ramp.stoneList[i].Qy)
        
        ax.plot(timings, y1, '--x', label='Qx', markersize=12)
        ax.plot(timings, y2, '--+', label='Qy', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Timing (ms)')
        ax.set_ylabel('Tunes')
        ax.legend()
        can.draw_idle()

    elif plot_name == 'Chromaticity' :
        for i in range(len(Ramp.stoneList)) :
            y1.append(Ramp.stoneList[i].Qpx)
            y2.append(Ramp.stoneList[i].Qpy)
        
        ax.plot(timings, y1, '--x', label='Qpx', markersize=12)
        ax.plot(timings, y2, '--+', label='Qpy', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Timing (ms)')
        ax.set_ylabel('Chromaticities')
        ax.legend()
        can.draw_idle()

    elif plot_name == 'Gamma transition' :
        gamma = lambda p : np.sqrt( 1 + (p/Ramp.get_M0())**2)
        for i in range(len(Ramp.stoneList)) :
            y1.append( gamma(Ramp.stoneList[i].momentum))
            y2.append(Ramp.stoneList[i].gammaTR)
        print y1
        ax.plot(timings, y1, '--x', label='gamma', markersize=12)
        ax.plot(timings, y2, '--+', label='gamma transition', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Timing (ms)')
        ax.set_ylabel('Gamma')
        ax.legend()
        can.draw_idle()
        

def make_plot_stone(plot_name, window) :
    from core import MainWindow
    ax = MainWindow.main.axs[window] 
    can  = MainWindow.main.canvas[window]
    
    Ramp =  RampDef.liveRamp
    Stone = RampDef.liveRamp.stoneList[RampDef.liveRamp.selected_stone_ID]
    s, y1, y2 = [], [], []

    for i in range(len(Stone.optics)) :
        s.append(Stone.optics[i,1])

    if plot_name == 'Beta' :
        for i in range(len(Stone.optics)) :
            y1.append(Stone.optics[i,2])
            y2.append(Stone.optics[i,3])
        
        ax.plot(s, y1, '--x', label='Beta x', markersize=12)
        ax.plot(s, y2, '--+', label='Beta y', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Longitudinal position (m)')
        ax.set_ylabel('Beta function (m)')
        ax.legend()
        can.draw_idle()

    if plot_name == 'Dispersion' :
        for i in range(len(Stone.optics)) :
            y1.append(Stone.optics[i,8])
            # y2.append(Stone.optics[i,3])
        
        ax.plot(s, y1, '--x', label='Dispersion x', markersize=12)
        # ax.plot(s, y2, '--+', label='Dispersion y', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Longitudinal position (m)')
        ax.set_ylabel('Dispersion function (m)')
        ax.legend()
        can.draw_idle()

    if plot_name == 'Phi' :
        for i in range(len(Stone.optics)) :
            y1.append(Stone.optics[i,6])
            y2.append(Stone.optics[i,7])
        
        ax.plot(s, y1, '--x', label='Phi x', markersize=12)
        ax.plot(s, y2, '--+', label='Phi y', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Longitudinal position (m)')
        ax.set_ylabel('Phase advance (rad)')
        ax.legend()
        can.draw_idle()

    if plot_name == 'Alpha' :
        for i in range(len(Stone.optics)) :
            y1.append(Stone.optics[i,2])
            y2.append(Stone.optics[i,3])
        
        ax.plot(s, y1, '--x', label='Alpha x', markersize=12)
        ax.plot(s, y2, '--+', label='Alpha y', markersize=12)
        ax.grid(True)
        ax.set_xlabel('Longitudinal position (m)')
        ax.set_ylabel('Alpha function')
        ax.legend()
        can.draw_idle()
        
        
    

    
    # for i in range(len(
    
    # if plot_name == 'Beta'  :
            
    
    # for i in range(len(stone.optics
    
    # if plot_name == 'Rigidity'  :
        
    #     name1 = 'Rigidity'
    #     main.axs[window].plot(np.random.rand(5), '-*')
    #     main.axs[window].grid(True)
    #     main.axs[window].set_title('Ridity')
    #     main.canvas[window].draw_idle()
        

    # elif plot_name == 'Tune' :
        

    #     # make plot of tune
    #     name1 = 'Rigidity'
    #     fig1 = Figure()
    #     ax1f1 = fig1.add_subplot(111)
    #     ax1f1.plot(np.random.rand(10))
        

    
