### System info ###
# system label
label = 'CH4* + H (+ H2)'

# reactive species
reactants(
    A = ['CH4'],
    natoms = [5],
    xA = [0.1],
    B = [[4.3348849804121254,"cm-1"]]
)

# reactive colliders
x_Colliders(
    X = ['H'],
    natoms = [1],
    xX = [0.01]
)

# nonreactive colliders
m_Colliders(
    M = ['H2'],
    natoms = [2],
    xM = [1.0]
)

# other trajectory info
trajectory(
    temp = (1000.0,"K"),
    steps = 3000
)

### Directory info ###

potentials(
   PES = ['ch4hALL','alkT']
)

dirSetup(
   procs = 36,
   ntrajs = 36
)
