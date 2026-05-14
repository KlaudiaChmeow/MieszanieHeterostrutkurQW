import matplotlib
import numpy

# m0 - masa wolnego elektronu
# gamma1 - parametr luttingera 1
# gamma2 - parametr luttingera 2
# gamma3 - parametr luttingera 3
# delta - parametr delta spin orbita
# Ep, F - stałe z plików
# Eg - przerwa wzbroniona (odrazu z mieszania)

def electron_Effective(m0, F, Ep, Eg, delta):
    return (m0)/((1+2*F)+((Ep*(Eg + (2*delta/3)))/(Eg*(Eg+delta))))

def heavyHole_Effective_Z(m0, gamma1, gamma2):
    return (m0)/(gamma1 - 2*gamma2)

def heavyHole_Effective_110(m0, gamma1, gamma2, gamma3):
    return (2*m0)/(2*gamma1 - gamma2 - 3*gamma3)

def heavyHole_Effective_111(m0, gamma1, gamma3):
    return (m0)/(gamma1 - 2*gamma3)

def lightHole_Effective_Z(m0, gamma1, gamma2):
    return (m0)/(gamma1 + 2*gamma2)

def lightHole_Effective_110(m0, gamma1, gamma2, gamma3):
    return (2*m0)/(2*gamma1 + gamma2 + 3*gamma3)

def lightHole_Effective_111(m0, gamma1, gamma3):
    return (m0)/(gamma1 + 2*gamma3)

def spinorbital_Effective(m0, gamma1, Eg, Ep, delta):
    return (m0)/(gamma1 - ((Ep*delta)/(3*Eg*(Eg+delta))))