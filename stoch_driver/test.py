import argparse

parser = argparse.ArgumentParser(prog='MC DiNT',description='Monte Carlo setup for DiNT')
parser.add_argument('--temp', type=float, help='Input temperature (K)')
parser.add_argument('-A', type=str, action='append', nargs='+', help='adds a reactive species to the system')
parser.add_argument('-M', type=str, action='append', nargs='+', help='adds an inert species to the system')
parser.add_argument('-X', type=str, action='append', nargs='+', help='adds a radical species to the system')

ns = parser.parse_args()

print("temp =",ns.temp)
print("reactive species:",ns.A)
print("inert species:",ns.M)
print("radical species:",ns.X)

#print("range M =",len(ns.M))
#print("range M =",range(len(ns.M)))
