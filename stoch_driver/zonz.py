import sys
import math
import numpy as np
import operator

import stoch_driver.constants as constants

#if (len(sys.argv) != 4):
#    print("usage: python zonz.py A_molecule X_molecule T(K)")
#    sys.exit()

def zCalc(mol1, mol2, temp):
    mol1 = str(mol1)
    mol2 = str(mol2)
    T = float(temp)
    m1, m2 = 0., 0.
    sig1, sig2 = 0., 0.
    eps1, eps2 = 0., 0.

    if mol1.lower() == 'ch4':
        m1 = 1.007825*4+12.0
        sig1 = 3.575
        eps1 = 435.921
    elif mol1.lower() == 'h2o':
        m1 = 1.007825*2+15.994915
        sig1 = 2.943
        eps1 = 637.056
    else:
        print("Accepts CH4 or H2O for A")

    if mol2.lower() == 'n2':
        m2 = 2.0*14.003074
        sig2 = 3.610
        eps2 = 97.839
    elif mol2.lower() == 'h2':
        m2 = 2.0*1.007825
        sig2 = 2.190
        eps2 = 304.690
    elif mol2.lower() == 'h':
        m2 = 1.007825
        sig2 = 1.530
        eps2 = 541.672
    elif mol2.lower() == 'o2':
        m2 = 2.0*15.994915
        sig2 = 3.069
        eps2 = 676.424
    elif mol2.lower() == 'o':
        m2 = 15.994915
        sig2 = 2.485
        eps2 = 235.686
    elif mol2.lower() == 'ar':
        m2 = 39.962383
        sig2 = 3.462
        eps2 = 127.697
    elif mol2.lower() == 'co2':
        m2 = 12.0+2.0*15.994915
        sig2 = 1201.184
        eps2 = 3.386
    else:
        print("Accepts H, N2, N2, O, O2, Ar, or CO2 for X")

    sig = 0.5*(sig1 + sig2)
    eps = math.sqrt(eps1*eps2)

    mu = (m1*m2/(m1+m2))/(constants.avo*1000.0)
    pref = constants.pi*math.sqrt(8.0*1.380603e-23*T/(constants.pi*mu))*1.e6*1.e-20
    zlj_pref = sig**2/(0.7+0.52*math.log(0.69502*T/eps)/math.log(10.0))
    bmax2 = 4*zlj_pref
    bmax = math.sqrt(bmax2)
    zhs = bmax2*pref
    zlj = pref*zlj_pref

    return {'zhs': zhs, 'zlj': zlj ,'bmax': bmax}
    #print('{:23} {:23} {:8}'.format("HS", "LJ", "ZHS/ZLJ"))
    #print('{:.{prec}} {:.{prec}} {:.{prec}}'.format(zhs, zlj, bmax, prec=18))
    #print('{:.{prec}} {:.{prec}}'.format(zhs, bmax, prec=18))

def pEJ(temp):
    file = 'pej2.'+str(temp)
    x = np.random.randrange(0,1)
    l=1
    for line in file:
        data = split(line)
        if (l==1):
            pnorm = data[2]
        else:
            psum += data[4]
            if (x < psum/pnorm):
                ee, jf = data[2], data[3]
                break
    
    return {'ee': ee, 'jf': jf}