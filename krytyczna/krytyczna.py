import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# parametry materiałów PRZYKŁADOWE NADANE PRZEZE MNIE:

# Stałe sieci [Angstrom]
a_InAs = 6.0583
a_GaAs = 5.6533
a_InP  = 5.8687
a_GaP  = 5.4505


# FUNKCJA PRAWA VEGARDA

def vegard_quaternary(x, y):
    """
    Przykład dla In_xGa_(1-x)As_yP_(1-y)

    x - udział In
    y - udział As
    """

    a = (
        x * y * a_InAs +
        (1 - x) * y * a_GaAs +
        x * (1 - y) * a_InP +
        (1 - x) * (1 - y) * a_GaP
    )

    return a



# NIEDOPASOWANIE SIECIOWE


def lattice_mismatch(a_layer, a_substrate):
    """
    f = (a_layer - a_substrate) / a_substrate
    """

    return (a_layer - a_substrate) / a_substrate

# ==============================

def critical_thickness_MB(f, b, nu=0.31, alpha=np.pi/4):
    """
    Matthews-Blakeslee critical thickness

    f     - lattice mismatch
    b     - Burgers vector [m]
    nu    - Poisson ratio
    alpha - angle

    Zwraca hc w [nm]
    """

    def equation(h):
        return (
            h
            - (
                b / (8 * np.pi * abs(f) * (1 + nu))
            )
            * (
                (1 - nu * np.cos(alpha)**2)
                / np.cos(alpha)
            )
            * np.log(h / b)
        )

    h0 = 1e-8  # initial guess [m]

    hc = fsolve(equation, h0)[0]

    return hc * 1e9  # nm


# ==============================
# PRZYKŁAD OBLICZENIA
# ==============================

# Skład InGaAsP
x = 0.53
y = 0.22

# Podłoże InP
a_sub = a_InP

# Stała sieci warstwy
a_layer = vegard_quaternary(x, y)

# Niedopasowanie
f = lattice_mismatch(a_layer, a_sub)

# Wektor Burgersa
# b = a/sqrt(2)
b = (a_layer * 1e-10) / np.sqrt(2)

# Obliczenie hc
hc = critical_thickness_MB(f, b)

print("=== WYNIKI ===")
print(f"Stała sieci warstwy: {a_layer:.4f} Å")
print(f"Niedopasowanie sieciowe: {f*100:.4f} %")
print(f"Grubość krytyczna hc: {hc:.2f} nm")


# ==============================
# WYKRES hc(f)
# ==============================

f_values = np.linspace(0.0001, 0.03, 200)
hc_values = []

for fv in f_values:
    hc_tmp = critical_thickness_MB(fv, b)
    hc_values.append(hc_tmp)

plt.figure(figsize=(7,5))
plt.semilogy(f_values * 100, hc_values)

plt.xlabel("Niedopasowanie sieciowe [%]")
plt.ylabel("Grubość krytyczna hc [nm]")
plt.title("Matthews-Blakeslee Critical Thickness")
plt.grid(True)

plt.show()