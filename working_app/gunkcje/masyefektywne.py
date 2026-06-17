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