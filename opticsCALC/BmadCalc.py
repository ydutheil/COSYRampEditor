import subprocess
import numpy as np

from datadef import RampDef

def get_optics(  stone ) :
    print ("computing")
    # stone = RampDef.liveRamp.stoneList[stone_num]
    input_parm = ['./opticscalc']
    input_parm.extend( (str(stone.momentum), RampDef.particle_dict_inv[RampDef.liveRamp.particle]) )
    input_parm.extend( [str(i) for i in stone.quads] )

    # start_time = timeit.default_timer()
    output = str(subprocess.check_output( input_parm )).split("\\n") 
    # print timeit.default_timer()-start_time
    N_elements = int(output[len(output)-2])
    if output[len(output)-1-2].strip() == 'failed' :
        stone.stable = False
        stone.gammaTR, stone.Qpx, stone.Qpy, stone.optics = 0, 0, 0, [0]
        return
    else :
        stone.stable = True
        stone.gammaTR =  float(output[len(output)-1-2-N_elements-3])
        dumm, stone.Qpx, stone.Qpy = np.fromstring(output[len(output)-1-2-N_elements-2], sep=' ')
        stone.Qx, stone.Qy = np.fromstring(output[len(output)-1-2-N_elements-1], sep=' ')


        stone.optics = np.array(  [np.fromstring(row, sep=' ') for row in np.array (output[len(output)-3-N_elements : len(output)-2])  ] )

 
