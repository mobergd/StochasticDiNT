import os
import sys
import numpy as np

import stoch_driver.main as main
import parser

################################################################################

reactants = None
x_Colliders = None
m_Colliders = None
temp = None
steps = None

#def setReactants(A, natoms, xA, B):
#    global reactants
#    reactants = Reactants(A, natoms, xA, B)

#def setXColliders(X, natoms, xX):
#    global x_Colliders
#    x_Colliders = xColliders(X, natoms, xX)

#def setMColliders(M, natoms, xM):
#    global m_Colliders
#    m_Colliders = mColliders(M, natoms, xM)

#def setTrajectory(temp, steps):
#    global temp, steps
#    temp = temp
#    steps = steps

#def setDirSetup(procs, ntrajs):
#    global dirSetup
#    dirSetup = DirSetup(procs, ntrajs)

################################################################################

def loadInputFile(input_path):
    """
    Load the MC input file located at `path`.
    """
    # Set paths
    DRIVE_PATH = os.getcwd()

    # Read the input file into a string
    with open(os.path.join(DRIVE_PATH, 'input.dat'), 'r') as infile:
        INPUT_STRING = infile.read()
    
    # Check system info parameters
    parser.check_system_info_keywords(INPUT_STRING)

    # Read system info
    JOBTYPE = parser.read_jobtype(INPUT_STRING)
    LABEL = parser.read_label(INPUT_STRING)
    NA, NX, NM = parser.read_num_axm(INPUT_STRING)
    REACTANTS = parser.read_reactants(INPUT_STRING, NA)
    XCOLLIDERS = parser.read_xcolliders(INPUT_STRING, NX)
    MCOLLIDERS = parser.read_mcolliders(INPUT_STRING, NM)
    NATOMSA = parser.read_natoms_a(INPUT_STRING, NA)
    NATOMSX = parser.read_natoms_x(INPUT_STRING, NX)
    NATOMSM = parser.read_natoms_m(INPUT_STRING, NM)
    XA = parser.read_xa(INPUT_STRING, NA)
    XX = parser.read_xx(INPUT_STRING, NX)
    XM = parser.read_xm(INPUT_STRING, NM)
    BLIST = parser.read_blist(INPUT_STRING, NA)
    TEMPERATURE = parser.read_temperature(INPUT_STRING)
    STEPS = parser.read_steps(INPUT_STRING)

    # Check directory info parameters
    parser.check_directory_info_keywords(INPUT_STRING)
    
    # Read directory info
    NTRAJS = parser.read_ntrajs(INPUT_STRING)
    NPROCS = parser.read_nprocs(INPUT_STRING)
    POTENTIALS = parser.read_potentials(INPUT_STRING)

    stochTraj = Trajectory(
        label = LABEL,
        A = REACTANTS,
        X = XCOLLIDERS,
        M = MCOLLIDERS,
        natomsA = NATOMSA,
        natomsX = NATOMSX,
        natomsM = NATOMSM,
        xA = XA,
        xX = XX,
        xM = XM,
        temperature = TEMPERATURE,
        steps = STEPS,
    )

    ntrajs = NTRAJS
    nprocs = NPROCS

    return stochTraj, ntrajs, nprocs
