# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

# runs = [48742,48743,48744,48745,48746]
runs = range(48742,48747)


for run in runs: 
    
    LoadNexus(Filename=f'/SNS/SNAP/IPTS-24179/shared/Malcolm/reduced/small/SNAP{run}.nxs', 
    OutputWorkspace=f'SNAP{run}', 
    SpectrumMax=1)

    CropWorkspace(InputWorkspace=f'SNAP{run}', 
    OutputWorkspace=f'SNAP{run}', 
    XMin=1.4550000000000001, 
    XMax=2.1360000000000001)
    
    #create handle to workspace
    ws = mtd[f'SNAP{run}']
    
    #get x, y data from workspace
    x = ws.extractX()
    y = ws.extractY()
    i = np.argmax(y)

    FitPeaks(InputWorkspace=f'SNAP{run}', 
    OutputWorkspace=f'SNAP{run}_fit', 
    PeakCenters=x[0,i], 
    PeakWidthPercent=0.03, 
    FitFromRight=False, 
    HighBackground=False, 
    ConstrainPeakPositions=False, 
    FittedPeaksWorkspace=f'SNAP{run}_fittedPeaks', 
    OutputPeakParametersWorkspace=f'SNAP{run}_outputPars', 
    OutputParameterFitErrorsWorkspace=f'SNAP{run}_fitErrors')

    #get output fit parameters and convert to dictionaries
    ws_res = mtd[f'SNAP{run}_outputPars']
    ws_err = mtd[f'SNAP{run}_fitErrors']
    res = ws_res.toDict()
    err = ws_err.toDict()
    
    print(f'peak pos: {res["PeakCentre"][0]:.4f} ({err["PeakCentre"][0]:.4f})')
    
    #get log information from metadata
    
    
    
    CreateWorkspace(DataX=
    
    

    