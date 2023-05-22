import numpy as np, pandas as pd
from tc_python import *
from mpi4py.futures import MPIPoolExecutor
import time
def Batch_equilib(DB,Elements,NTP):
    '''
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Description
    ===========
    This function calculates a batch equilibrium based on given conditions. The function is written based on the single point calculation.


    Revisions
    =========

     Date            Programmer      Description of change
     ----            ----------      ---------------------
     05/16/2023      S. KWON         Original code


    Variables
    =========

    Arguments
    DB:       (string)            A database name of ThermoCalc e.g., TCFE11
    Elements: (list of strings)   A list of system elements e.g., ['Fe','C']
    NTP:      (array of floats)   An array of condition with the sequence of compositions (wt.), Temperature (Celsius), Pressure (bar), e.g., [0.8,0.2,1500,1]

    Returns
    output_all: (list)            A list of dictionary that contains equilibrium information i.e., stable phases and volume fractions
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    '''
    # Allocate variables
    comp = NTP[:,:-2]
    T = NTP[:,-2]
    P = NTP[:,-1]
    l = len(NTP[:,0])
    
    # TC-Python calculation
    with TCPython() as sess:
        # Init TC python: load database, set system elements
        TCcalc = (
            sess
            .select_database_and_elements(DB, Elements)     #Define databases and the system of interest
            .select_phase('FCC_L12')                        #Specify phases that must be included
            .select_phase('BCC_B2')
            .get_system()
            .with_single_equilibrium_calculation()
            .enable_global_minimization()                   #We enable globla minimization
        )

        # Loop through conditions
        output_all=[]   #Initialize the output variable
        for j in range(l):
            output=dict({})
            try:            
                TCcalc.set_condition(ThermodynamicQuantity.temperature(), T[j])
                TCcalc.set_condition(ThermodynamicQuantity.pressure(), P[j])
                
                #When the composition is given in wt fraction
                wf = ThermodynamicQuantity.mass_fraction_of_a_component
                
                # Loop Thorugh compositions
                for i in range(1,len(Elements)):
                    TCcalc.set_condition(wf(Elements[i]), comp[j,i])
                
                result = TCcalc.calculate()
                Phases=result.get_stable_phases()
                

                for phase in Phases:
                    output[phase]=result.get_value_of("VPV({})".format(phase))
            
            #Error handling
            except CalculationException as e:
                # Sometime TC-Python fails to reach global equilibrium, which will abort the whole calculations.
                # We create an exception that handles this error
                output['Error']=0
            output_all.append(output)
    return output_all

def determine_subranges(Database,elements,NTP,nPerBatch):
    """ 
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Description
    ===========
    Break a full range into smaller sets of ranges.
    
    Revisions
    =========

     Date            Programmer      Description of change
     ----            ----------      ---------------------
     05/18/2023      S. KWON         Original code


    Variables
    =========

    Arguments
    DB:       (string)            A database name of ThermoCalc e.g., TCFE11
    elements: (list of strings)   A list of system elements e.g., ['Fe','C']
    NTP:      (array of floats)   An array of condition with the sequence of compositions (wt.), Temperature (Celsius), Pressure (bar), e.g., [0.8,0.2,1500,1]
    nPerBatch: (integer)          The size of a subrange

    Returns
    res: (list)                   A list of arguments for Batch_equilibrium function
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """
    res = [] #Allocate output
    n,m=NTP.shape
    fullrange=[0,n]

    for i in range(fullrange[0], fullrange[1], nPerBatch):
        res.append( [Database,elements,NTP[i:min(i+nPerBatch, fullrange[1]),:]] ) 
    return res

if __name__ == '__main__': #Make sure the script is executed only once
    # First define the number of cores and the subrange for each batch
    start=time.time()
    nCores=5
    nPerBatch=40
    
    # Get whole dataset for calculations
    database='TCFE11'                   #Define database
    df=pd.read_csv('BatchEquilib.csv')  # Read csv file into a dataframe
    elements=df.keys().to_list()[:-2]   #Define system   
    NTP=df.to_numpy()                   #Read NTP data from the dataframe
    
    # Prepare arguments for each subrange
    subsets=determine_subranges(database,elements,NTP,nPerBatch)
    
    # Conduct multiprocess calculation
    with MPIPoolExecutor() as executor:
        res = executor.starmap(Batch_equilib, subsets)
    end=time.time()
    print('Total execution time: {} s'.format(end-start))
    
    # Combine all results
    output_all=[] 
    for r in res:
        output_all=output_all+r
    
    # Data Processing
    # Get all phases in the results
    Phases=[]
    for output in output_all:
        Phases=Phases+list(output.keys())
        
    # Remove the duplicate
    Phases=[*set(Phases)]

    # Create a numpy database
    res=np.zeros((len(output_all),len(Phases)))

    # Allocate data
    for i,output in enumerate(output_all):
        for j,Phase in enumerate(Phases):
            try: res[i,j]=output[Phase]
            except: KeyError

    df_out=pd.DataFrame(res,columns=Phases)

    # We can also save the dataframe into csv file via
    df_out.to_csv('BatchEquilibMpi_results.csv')