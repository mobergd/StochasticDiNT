################################################################################
#
#   Stochastic DiNT -
#
#   Copyright (c) 2020 by Daniel R. Moberg (mobergdr@anl.gov)
#                         Ahren W. Jasper (ajasper@anl.gov)
#
################################################################################

"""
This is the main execution script for Stochastic DiNT,
To use with 36 processes (one trajectory per process is recommended):

$ python3 stoch_dint.py examples/CH4+H_H2/input.py
$ mpiexec -n 36 python3 -m mpi4py.bench 
        stoch_dint.py examples/CH4+H_H2/input.py
"""

import os.path
import sys
import argparse

from mpi4py import MPI

import stoch_driver.main as main
import stoch_driver.collisions as collisions
import stoch_driver.zonz as zonz
from stoch_driver.input import loadInputFile

################################################################################

#System setup
def parseCommandLineArguments():

    parser = argparse.ArgumentParser(prog='Stoch DiNT',
                                     description='Stochastic Dynamcis setup for DiNT')

    parser.add_argument('T', metavar='TEMP', type=float, nargs=1,
                        help='System temperature (K)')
    parser.add_argument('A', type=str, action='append', nargs='+',
                        help='adds a reactive species to the system')
    parser.add_argument('M', type=str, action='append', nargs='+',
                        help='adds an inert species to the system')
    parser.add_argument('X', type=str, action='append', nargs='+',
                        help='adds a radical species to the system')
    parser.add_argument('xA', type=str, action='append', nargs='+',
                        help='relative mole fraction for reactive species')
    parser.add_argument('xM', type=str, action='append', nargs='+',
                        help='relative mole fraction for inert species')
    parser.add_argument('xX', type=str, action='append', nargs='+',
                        help='relative mole fraction for radical species')
    parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                        help='specify file to use for input')
    parser.add_argument('-p', '--processes', metavar='PROC', type=int, nargs=1, default=[1],
                        help='the number of processors to use')

    return parser.parse_args()

################################################################################

if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    size = comm.Get_size() # 1000 processors
    rank = comm.Get_rank() # current processor
    #rank = MPI.Get_processor_name()

    if (rank == 0):
        print("MPI process begun with ", size, " processors")

        # Parse the command-line arguments (requires the argparse module)
#        ns = parseCommandLineArguments()

#        print("temp =", ns.T)
#        print("reactive species:", ns.A)
#        print("inert species:", ns.M)
#        print("radical species:", ns.X)
#        print("number of processors:", ns.processes)

        # Determine the output directory
#        outputDirectory = os.path.dirname(os.path.abspath(ns.file[0]))

        DRIVE_PATH = os.getcwd()
        with open(os.path.join(DRIVE_PATH, 'input.dat'), 'r') as infile:
            INPUT_STRING = infile.read()

        # Load the input file for the job
        stochTraj, ntrajs, nprocs = loadInputFile(INPUT_STRING)

        print("temp =", stochTraj.temperature)
        print("reactive species:", stochTraj.A)
        print("inert species:", stochTraj.M)
        print("radical species:", stochTraj.X)
        print("number of processors:", nprocs)

        # Initialize rate coefficients and bmax values
        rates = collisions.initRates(stochTraj.A, stochTraj.X, stochTraj.M,
                                     stochTraj.temperature)

    # Distribute stoch trajectory info to processes
    comm.bcast(stochTraj, root=0)
    comm.bcast(rates, root=0)

    # Each process executes one trajectory:
    for i in range(size):
        if (i == rank):
            traj[rank] = stochTraj
            traj[rank].executeStochasticDynamics(stochTraj, rates)

    if rank == 0:
        comm.gather(traj, root=0)

        print("")