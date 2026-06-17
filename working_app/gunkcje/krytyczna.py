# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.optimize import fsolve
import importlib.util

def critical_thickness_MB(f, b, nu=0.31, alpha=np.pi/4):
    """
    Oblicza grubość krytyczną hc [nm] z uwikłanego równania modelu Matthewsa-Blakeslee.
    Filtruje skrajne wartości zmierzające do nieskończoności (dla f bliskiego 0).
    """
    if abs(f) < 1e-6:
        return 1000.0  # Obcięcie dla estetyki skali wykresu

    def equation(h):
        if h <= 0:
            return 1e10  # Zabezpieczenie logarytmu przed wartościami ujemnymi
        return (
            h
            - (b / (8 * np.pi * abs(f) * (1 + nu)))
            * ((1 - nu * np.cos(alpha)**2) / np.cos(alpha))
            * np.log(h / b)
        )

    h0 = 1e-8  # Przybliżenie startowe (10 nm)
    try:
        hc = fsolve(equation, h0)[0]
        hc_nm = hc * 1e9  # Konwersja na nanometry
        if hc_nm > 1000.0 or hc_nm < 0:
            return 1000.0
        return hc_nm
    except Exception:
        return 1000.0

def get_binary_lattice(database, cat, an):
    """Bezpiecznie pobiera stałą sieci materiału binarnego z bazy danych."""
    materials = database["binary materials"]
    name1 = cat + an
    if name1 in materials:
        return materials[name1]["a"]
    name2 = an + cat
    if name2 in materials:
        return materials[name2]["a"]
    raise ValueError(f"Brak materiału binarnego dla pary: {cat} i {an}")

def get_ternary_2d_data(database, cations, anions, substrate_name, funkcje_path):
    """
    Generuje dane 2D dla układów 3-elementowych (np. InGaAs lub GaAsP).
    Zwraca wektor składu, wektor hc oraz etykietę osi X.
    """
    mieszanie_spec = importlib.util.spec_from_file_location("mieszanie", os.path.join(funkcje_path, "mieszanie.py"))
    mieszanie = importlib.util.module_from_spec(mieszanie_spec)
    mieszanie_spec.loader.exec_module(mieszanie)

    a_sub = database["binary materials"][substrate_name]["a"]
    x_vec = np.linspace(0.0, 1.0, 100)
    hc_vec = []

    cats = [c for c in cations if c]
    ans = [a for a in anions if a]

    if len(cats) == 2 and len(ans) == 1:
        # Przypadek: 2 kationy, 1 anion (np. In_x Ga_1-x As)
        a1 = get_binary_lattice(database, cats[0], ans[0])
        a2 = get_binary_lattice(database, cats[1], ans[0])
        xlabel = f"Skład kationu {cats[0]} (x)"
        for x in x_vec:
            a_layer = mieszanie.mix(x, a1, a2)
            f = (a_layer - a_sub) / a_sub
            b = (a_layer * 1e-10) / np.sqrt(2)
            hc_vec.append(critical_thickness_MB(f, b))
            
    elif len(cats) == 1 and len(ans) == 2:
        # Przypadek: 1 kation, 2 aniony (np. Ga As_x P_1-x)
        a1 = get_binary_lattice(database, cats[0], ans[0])
        a2 = get_binary_lattice(database, cats[0], ans[1])
        xlabel = f"Skład anionu {ans[0]} (x)"
        for x in x_vec:
            a_layer = mieszanie.mix(x, a1, a2)
            f = (a_layer - a_sub) / a_sub
            b = (a_layer * 1e-10) / np.sqrt(2)
            hc_vec.append(critical_thickness_MB(f, b))
    else:
        raise ValueError("Niepoprawna kombinacja pierwiastków dla układu 3-elementowego.")

    return x_vec, np.array(hc_vec), xlabel

def get_quaternary_3d_data(database, cations, anions, substrate_name, funkcje_path):
    """
    Generuje siatkę 3D dla układu czteroskładnikowego.
    Obsługuje zarówno układy 3+1/1+3 (warunek x + y <= 1), jak i 2+2 (x i y niezależne).
    """
    mieszanie_spec = importlib.util.spec_from_file_location("mieszanie", os.path.join(funkcje_path, "mieszanie.py"))
    mieszanie = importlib.util.module_from_spec(mieszanie_spec)
    mieszanie_spec.loader.exec_module(mieszanie)

    a_sub = database["binary materials"][substrate_name]["a"]
    
    x_vec = np.linspace(0.0, 1.0, 60)
    y_vec = np.linspace(0.0, 1.0, 60)
    X, Y = np.meshgrid(x_vec, y_vec)
    Z = np.zeros_like(X)

    cats = [c for c in cations if c]
    ans = [a for a in anions if a]

    if len(cats) == 3 and len(ans) == 1:
        # Mieszanie 3 kationów i 1 anionu (np. Al_x In_y Ga_(1-x-y) As)
        a1 = get_binary_lattice(database, cats[0], ans[0])
        a2 = get_binary_lattice(database, cats[1], ans[0])
        a3 = get_binary_lattice(database, cats[2], ans[0])
        xlabel = f"Skład kationu {cats[0]} (x)"
        ylabel = f"Skład kationu {cats[1]} (y)"
        
        for i in range(len(y_vec)):
            for j in range(len(x_vec)):
                x_val = X[i, j]
                y_val = Y[i, j]
                if x_val + y_val <= 1.0001:
                    a_layer = mieszanie.mix(x_val, a1, a3) + mieszanie.mix(y_val, a2, a3) - a3
                    f = (a_layer - a_sub) / a_sub
                    b = (a_layer * 1e-10) / np.sqrt(2)
                    Z[i, j] = critical_thickness_MB(f, b)
                else:
                    Z[i, j] = np.nan  # Maskowanie punktów poza trójkątem składu

    elif len(cats) == 1 and len(ans) == 3:
        # Mieszanie 1 kationu i 3 anionów (np. Ga As_x P_y Sb_(1-x-y))
        a1 = get_binary_lattice(database, cats[0], ans[0])
        a2 = get_binary_lattice(database, cats[0], ans[1])
        a3 = get_binary_lattice(database, cats[0], ans[2])
        xlabel = f"Skład anionu {ans[0]} (x)"
        ylabel = f"Skład anionu {ans[1]} (y)"
        
        for i in range(len(y_vec)):
            for j in range(len(x_vec)):
                x_val = X[i, j]
                y_val = Y[i, j]
                if x_val + y_val <= 1.0001:
                    a_layer = mieszanie.mix(x_val, a1, a3) + mieszanie.mix(y_val, a2, a3) - a3
                    f = (a_layer - a_sub) / a_sub
                    b = (a_layer * 1e-10) / np.sqrt(2)
                    Z[i, j] = critical_thickness_MB(f, b)
                else:
                    Z[i, j] = np.nan

    elif len(cats) == 2 and len(ans) == 2:
        # Mieszanie 2 kationów i 2 anionów (np. In_x Ga_1-x As_y P_1-y)
        a11 = get_binary_lattice(database, cats[0], ans[0])
        a21 = get_binary_lattice(database, cats[1], ans[0])
        a12 = get_binary_lattice(database, cats[0], ans[1])
        a22 = get_binary_lattice(database, cats[1], ans[1])
        xlabel = f"Skład kationu {cats[0]} (x)"
        ylabel = f"Skład anionu {ans[0]} (y)"

        for i in range(len(y_vec)):
            for j in range(len(x_vec)):
                x_val = X[i, j]
                y_val = Y[i, j]
                # Interpolacja 2+2 (bilinearna)
                a_layer = (
                    x_val * y_val * a11 +
                    (1 - x_val) * y_val * a21 +
                    x_val * (1 - y_val) * a12 +
                    (1 - x_val) * (1 - y_val) * a22
                )
                f = (a_layer - a_sub) / a_sub
                b = (a_layer * 1e-10) / np.sqrt(2)
                Z[i, j] = critical_thickness_MB(f, b)

    else:
        raise ValueError("Nieobsługiwany układ 4-składnikowy. Wymagane: 3+1, 1+3 lub 2+2.")

    return X, Y, Z, xlabel, ylabel