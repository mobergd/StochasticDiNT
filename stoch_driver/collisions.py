import os
import sys
import math
import numpy
import random

import stoch_driver.zonz as zonz

def counter(ef, jf):

    return {'ef': ef, 'jf': jf}

def prepAMTraj(ef, jf, temp, bmax):

    ran = random.randrange(0,1)
#    jf = jf
    efev = ef*27.211/627.509 # kcal/mol -> eV
#    temp = temp
#    bmax = bmax
  
    ftemplate = open("inputM","rt")
    fout = open("input","wt")
    for line in ftemplate:
        fout.write(line.replace('RANSEED',ran).replace('JJJ',jf).
        replace('EEE',efev).replace('TEMP',temp).replace('BBBMAX',bmax))

    ftemplate.close()
    fout.close()

    return {'ef': ef, 'jf': jf}

def prepAXTraj(nmodes, ef, jf, temp, bmax):

    ran = random.randrange(0,1)
    bb = bmax/349.7630749 # B (cm-1 -> kcal/mol)
    ej = bb*jf**2
    efev = (ef-ej)*27.211/627.509 # kcal/mol -> eV
    efevt = efev/8.61692E-05/nmodes # kB (eV), nmodes = 3*natom - 6

    ftemplate = open("inputM","rt")
    fout = open("input","wt")
    for line in ftemplate:
        fout.write(line.replace('RANSEED',ran).replace('JJJ',jf).
        replace('EEE',efev).replace('ETE',efevt).replace('TEMP',temp).
        replace('BBBMAX',bmax))

    ftemplate.close()
    fout.close()

    return {'ef': ef, 'jf': jf}

def initRates(A, X, M, temp):

    zhsA = [[0 for j in range(len(A))] for i in range(len(A))]
    zhsX = [[0 for j in range(len(X))] for i in range(len(A))]
    zhsM = [[0 for j in range(len(M))] for i in range(len(A))]
    zljA = [[0 for j in range(len(A))] for i in range(len(A))]
    zljX = [[0 for j in range(len(X))] for i in range(len(A))]
    zljM = [[0 for j in range(len(M))] for i in range(len(A))]
    bmaxA = [[0 for j in range(len(A))] for i in range(len(A))]
    bmaxX = [[0 for j in range(len(X))] for i in range(len(A))]
    bmaxM = [[0 for j in range(len(M))] for i in range(len(A))]

    # Calculate collision rates for each species combination
    # As with As
    if len(A) > 0:
        for i in range(len(A)):
            for j in range(len(A)):
                zhsA[i,j], zljA[i,j], bmaxA[i,j] = zonz.zCalc(A[i], A[j], temp)
    # As with Xs
    if len(X) > 0: 
        for i in range(len(A)):
            for j in range(len(X)):
                zhsX[i,j], zljX[i,j], bmaxX[i,j] = zonz.zCalc(A[i], X[j], temp)
    # As with Ms
    if len(M) > 0:
        for i in range(len(A)):
            for j in range(len(M)):
                zhsM[i,j], zljM[i,j], bmaxM[i,j] = zonz.zCalc(A[i], M[j], temp)

    return zhsA, zljA, bmaxA, zhsX, zljX, bmaxX, zhsM, zljM, bmaxM

def normMoleFracs(xA, xX, xM, zhsA, zhsX, zhsM, 
                  zljA, zljX, zljM, bmaxA, bmaxX, bmaxM):

    numA = len(xA)
    numX = len(xX)
    numM = len(xM)

    # Probabilities
    totalspecies = numA + numX + numM

    w = []
    for j in range(totalspecies):
        w[j] = 0

    # Counter (A+M)
    w[0] = bmaxM[0] * xA[0] * xM[0] * zljM[0] / zljM[0]

    # A + X
    for j in range(numX):
        w[j+1] = bmaxX[j] * xA[0] * xX[j] * zhsX[j]/zljM[0]

    # A + M
    for j in range(numM):
        w[j+numX+1] = bmaxM[j] * xA[0] * xM[j] * zhsM[j]/zljM[0]

    # Normalize
    totalw = sum(w[j], j=range(len(w)))
    for j in range(len(w)):
        w[j] = w[j]/totalw
        if (j==0):
            print("% counter: ", w[0])
        elif (j < numX):
            print("% A[",0,"] + X[",j,"]: ", w[j+1])
        else:
            print("% A[",0,"] + M[",j,"]: ", w[j+numX+1])

    return w
