from datadef import RampDef
import subprocess
import numpy as np

def get_optics( ramp, stone ) :
    # stone = RampDef.testRamp.stoneList[stone_num]
    input_parm = ['./opticscalc']
    input_parm.extend( (str(stone.momentum), ramp.particle) )
    input_parm.extend( [str(i) for i in stone.quads] )
    
    output = subprocess.check_output( input_parm ).split("\n")

    N_elements = int(output[len(output)-2])
    if output[len(output)-1-2].strip() == 'failed' :
        stone.stable = False
        return
    else :
        stone.stable = True


    stone.gammaTR =  float(output[len(output)-1-2-N_elements-3])
    dumm, stone.Qpx, stone.Qpy = np.fromstring(output[len(output)-1-2-N_elements-2], sep=' ')
    stone.Qx, stone.Qy = np.fromstring(output[len(output)-1-2-N_elements-1], sep=' ')


    stone.optics = np.array(  [np.fromstring(row, sep=' ') for row in np.array (output[len(output)-3-N_elements : len(output)-2])  ] )
    print stone.timing*1e3, ' ms  done'
    # print  type(test), test.shape
    # print np.fromstring(test[1], sep=' ' )
    
    
    # for i in range(N_elements) :
        

    # a = np.array([[float(j) for j in i.split('\t')] for i in b.splitlines()])


    # print np.array( [[ float(j) for j in i.split   (output[len(output)-3-N_elements : len(output)-2], sep=' ')
    # print output[len(output)-3-N_elements : len(output)-2]
    # print output[len(output)-2-N_elements]
    # print output[len(output)-2]
