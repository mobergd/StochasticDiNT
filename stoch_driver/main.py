"""
Executes the parallelization of Stochastic DiNT through MPI4Py
"""

import os
import os.path
import sys
import math
import numpy as np

#take the current main() function/subroutine and move that code 
#   into a main_run_DiNT() function/subroutine that main() now calls. 
#Then, one can create a libDiNT.a library that a new lightweight MPI code 
#   could link in where each MPI rank spawned would call main_run_DiNT() 
#   to launch its own instance of a DiNT calculation. 
#Making sure each instance of DiNT had unique input and output is the 
#   next step, and then it’s a matter of optimizing performance, 
#   which in this case is usually turning off all unnecessary writing of 
#   output and/or refactoring how output gets written so that it’s 
#   efficient when 100,000s of DiNTs are all running (e.g. could capture 
#   important output in memory and write single output file in parallel).

from mpi4py import MPI
#from libDiNT.a import dint
#or use f2py?
import stoch_driver.collisions as collisions
import stoch_driver.zonz as zonz
import stoch_driver.constants as constants


class Trajectory:
    """
    A representation of a stochastic trajectory.
    =========================== ================================================
    Attribute                   Description
    =========================== ================================================
    `rank`                      MPI process rank assigned to this trajectory
    `A`                         A list of the reactants present in the system
    `X`                         A list of the reactive collider species in the system
    `M`                         A list of the nonreactive collider species in the system
    `natoms`                    An array of the number of atoms in associated A species
    `temp`                      Temperature of the system in Kelvin
    `xA`                        Number of molar equivalents of each A species
    `xX`                        Number of molar equivalents of each X species
    `xM`                        Number of molar equivalents of each M species
    `steps`                     Maximum number of Monte Carlo steps the simulation should take
    `Ei_list`                   A list of the initial energies for each step in the trajectory
    `Ef_list`                   A list of the final energies for each step in the trajectory
    `Ji_list`                   A list of the initial J for each step in the trajectory
    `Jf_list`                   A list of the final J for each step in the trajectory
    --------------------------- ----------------------------------------------------
    `xAn`                       Normalized mole fraction of A species
    `xXn`                       Normalized mole fraction of A species
    `xMn`                       Normalized mole fraction of A species
    =========================== ================================================
    """
    def __init__(self, label, A, X, M, natomsA, natomsX, natomsM, 
                 xA, xX, xM, temperature, steps):
        self.label = label
        self.A = A
        self.X = X
        self.M = M
        self.natomsA = natomsA
        self.natomsX = natomsX
        self.natomsM = natomsM
        self.temperature = temperature
        self.xA = xA
        self.xX = xX
        self.xM = xM
        self.steps = steps

        self.outputDirectory = join(os.path.abspath(outputDirectory),"b",rank)

        self.Ei_list = []
        self.Ji_list = []
        self.Ef_list = []
        self.Jf_list = []

#    def species(self): 

        #for i in range(len(A)):
        #    self.A[i] = A[i]
        #for i in range(len(X)):
        #    self.X[i] = X[i]
        #for i in range(len(M)):
        #    self.M[i] = M[i]
        
#        return A, X, M

#    def moleFracs(self):

        #for i in range(len(xA)):
        #    self.xA[i] = xA[i]
        #for i in range(len(xA)):
        #    self.xX[i] = xX[i]
        #for i in range(len(xA)):
        #    self.xM[i] = xM[i]

#        return xA, xX, xM

    def initEJ(self, ei, ji):
        self.Ei_list.append(ei)
        self.Ji_list.append(ji)

    def updateEJ(self, ef, jf):
        self.Ef_list.append(ef)
        self.Jf_list.append(jf)

    def executeStochasticDynamics(self, rates):
        # Set path
        DRIVE_PATH = os.getcwd()

        xA = self.xA
        xX = self.xX
        xM = self.xM
        zhsA = rates.zhsA
        zhsX = rates.zhsX
        zhsM = rates.zhsM
        zljA = rates.zljA
        zljX = rates.zljX
        zljM = rates.zljM
        bmaxA = rates.bmaxA
        bmaxX = rates.bmaxX
        bmaxM = rates.bmaxM

        # Initialize trajectory objects
        collisions.normMoleFracs(xA, xX, xM, zhsA, zhsX, zhsM, 
                                 zljA, zljX, zljM, bmaxA, bmaxX, bmaxM)

        # Initialize E, J values 
        zonz.pEJ(temp)

        ef = ee*constants.cmtokcalmol + 4.5*constants.evtokcalmol
        self.initEJ(ei = ef, ji = jf)
        self.Ei_list.append(ei)
        self.Ji_list.append(ji)

        # Continue stochastic dynamics until reaction occurs or max steps reached:
        while nn[0] < maxsteps:
            x = random.randrange(0,1)
            it = 0
            test = pp/ps
            while (x > test):
                it += 1
                test += pp[it]/ps
            nn[it] += 1

            if (it == 0): # Counter
                # print to specific traj file
                print(nn[0],ji,ei,jf,ef)
            elif (it == 1): # A + M
                collisions.prepAMTraj(ef,jf,temp)    # creates new input file for A+M
                print("Run dint-alkT here")
#                dint.dint-alkT ### call appropriate dint exe
            elif (it == 2): # A + X
                collisions.prepAXTraj(nmodes,ef,jf,temp,bmax)   # creates new input file for A+X
                print("Run dint-ch4hALL here")
#                dint.dint-ch4hALL ### call appropriate dint exe
            else:
                print("Error: Iteration not found")
                break

            with open('fort.31') as f:
                for line in f:
                    pass    # grab last line from fort.31
                f31 = split(line)

            ji = f31[12]
            ei = (f31[13]+f31[14]+f31[15])*constants.eVtokcalmol
            jf = f31[24]
            ef = (f31[25]+f31[26]+f31[27])*constants.eVtokcalmol

            self.updateEJ(ef = ef, jf = jf)
            self.Ef_list.append(ef)
            self.Jf_list.append(jf)

#            print("Traj b",i,": Timestep ",nn[0]," , M collision ",nn[it]," ( ",ji," , ",ei," ) --> ( ",jf," , ",ef" )")

class Reactants:
    def __init__(self, A, natomsA, xA, B):
        self.A = A
        self.natomsA = natomsA
        self.xA = xA
        self.B = B

class xColliders:
    def __init__(self, X, natomsX, xX):
        self.X = X
        self.natomsX = natomsX
        self.xX = xX

class mColliders:
    def __init__(self, M, natomsM, xM):
        self.M = M
        self.natomsM = natomsM
        self.xM = xM