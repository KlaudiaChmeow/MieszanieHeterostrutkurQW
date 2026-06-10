# -*- coding: utf-8 -*-
"""
Zmodyfikowany plik: mieszanie.py
Dodano obsługę mas efektywnych oraz generowanie wykresów mas.
"""

import app_state
import copy

# Słownik energii Kane'a (Ep w eV) dla materiałów binarnych,
# których brakuje w pliku materialy.json (wg standardowych danych Vurgaftmana)
EP_FALLBACK = {
    "GaAs": 25.7, "AlAs": 21.1, "InAs": 21.1,
    "GaP": 31.3, "AlP": 17.7, "InP": 20.7,
    "GaSb": 27.0, "AlSb": 18.7, "InSb": 23.3,
    "GaN": 25.0, "AlN": 30.0, "InN": 19.0
}

def get_param(mat, mat_name, parameter):
    """Bezpieczne pobieranie parametru z obsługą wartości domyślnych Ep."""
    if parameter in mat:
        return mat[parameter]
    if parameter == "Ep":
        return EP_FALLBACK.get(mat_name, 23.0)
    return 0.0

# ==========================================
# MIESZANIE podstawowe
# ==========================================
def mix(x, A, B, bowing=0):
    return (1 - x) * B + x * A - x * (1 - x) * bowing

# ==========================================
# Masy Efektywne
# ==========================================

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

# ==========================================
# SZUKANIE MATERIAŁU i BOWINGU
# ==========================================
def find_material(database, el1, el2):
    materials = database["binary materials"]
    name1 = el1 + el2
    if name1 in materials:
        return name1, materials[name1]
    name2 = el2 + el1
    if name2 in materials:
        return name2, materials[name2]
    return None, None

def find_bowing(database, name):
    bowings = database["bowing"]
    if name in bowings:
        return bowings[name]
    return {"Eg": 0, "VBO": 0}

# ==========================================
# INTERPOLACJA PARAMETRÓW (ZMODYFIKOWANA)
# ==========================================
def mix_parameter(parameter, cations, anions, fractions, database):
    n_cat = len(cations)
    n_an = len(anions)

    # BINARKA
    if n_cat == 1 and n_an == 1:
        name, mat = find_material(database, cations[0], anions[0])
        if mat is None:
            raise ValueError(f"Nie znaleziono materiału {cations[0]}{anions[0]}")
        return get_param(mat, name, parameter)

    # TRÓJNARKA (2 kationy, 1 anion) - np. InGaAs
    elif n_cat == 2 and n_an == 1:
        cat1, cat2 = cations[0], cations[1]
        an = anions[0]
        x = fractions[cat1]
        name1, mat1 = find_material(database, cat1, an)
        name2, mat2 = find_material(database, cat2, an)
        bowing = find_bowing(database, cat1 + cat2 + an)
        return mix(x, get_param(mat1, name1, parameter), get_param(mat2, name2, parameter), bowing.get(parameter, 0))

    # TRÓJNARKA (1 kation, 2 aniony) - np. GaAsP
    elif n_cat == 1 and n_an == 2:
        cat = cations[0]
        an1, an2 = anions[0], anions[1]
        y = fractions[an1]
        name1, mat1 = find_material(database, cat, an1)
        name2, mat2 = find_material(database, cat, an2)
        bowing = find_bowing(database, cat + an1 + an2)
        return mix(y, get_param(mat1, name1, parameter), get_param(mat2, name2, parameter), bowing.get(parameter, 0))

    # CZWÓRKA (2+2) - np. InGaAsP
    elif n_cat == 2 and n_an == 2:
        cat1, cat2 = cations[0], cations[1]
        an1, an2 = anions[0], anions[1]
        x = fractions[cat1]
        y = fractions[an1]
        n11, m11 = find_material(database, cat1, an1)
        n21, m21 = find_material(database, cat2, an1)
        n12, m12 = find_material(database, cat1, an2)
        n22, m22 = find_material(database, cat2, an2)
        return (
              x * y * get_param(m11, n11, parameter)
            + (1 - x) * y * get_param(m21, n21, parameter)
            + x * (1 - y) * get_param(m12, n12, parameter)
            + (1 - x) * (1 - y) * get_param(m22, n22, parameter)
        )

    # CZWÓRKA (3+1) lub (1+3)
    elif (n_cat == 3 and n_an == 1) or (n_cat == 1 and n_an == 3):
        elements_list = cations if n_cat == 3 else anions
        fixed_el = anions[0] if n_cat == 3 else cations[0]
        value = 0
        for el in elements_list:
            frac = fractions[el]
            name, mat = find_material(database, el, fixed_el) if n_cat == 3 else find_material(database, fixed_el, el)
            value += frac * get_param(mat, name, parameter)
        return value

    raise ValueError(f"Nieobsługiwany skład: {n_cat} kationów i {n_an} anionów")

# ==========================================
# GENEROWANIE ZALEŻNOŚCI PASM OD SKŁADU
# ==========================================
def calculate_band_dependency(material, database):
    import numpy as np
    cations, anions = material["cations"], material["anions"]
    n_cat, n_an = len(cations), len(anions)
    mat_copy = copy.deepcopy(material)
    
    if (n_cat == 2 and n_an == 2) or (n_cat == 3 and n_an == 1) or (n_cat == 1 and n_an == 3):
        N = 41
        vec = np.linspace(0.0, 1.0, N)
        X, Y = np.meshgrid(vec, vec)
        Z_VBO, Z_CBO = np.zeros_like(X), np.zeros_like(X)
        
        for i in range(N):
            for j in range(N):
                if n_cat == 2 and n_an == 2:
                    mat_copy["fractions"][cations[0]], mat_copy["fractions"][cations[1]] = X[i, j], 1.0 - X[i, j]
                    mat_copy["fractions"][anions[0]], mat_copy["fractions"][anions[1]] = Y[i, j], 1.0 - Y[i, j]
                    valid = True
                else:
                    valid = (X[i, j] + Y[i, j] <= 1.00001)
                    if valid:
                        if n_cat == 3:
                            mat_copy["fractions"][cations[0]], mat_copy["fractions"][cations[1]] = X[i, j], Y[i, j]
                            mat_copy["fractions"][cations[2]] = max(0.0, 1.0 - X[i, j] - Y[i, j])
                        else:
                            mat_copy["fractions"][anions[0]], mat_copy["fractions"][anions[1]] = X[i, j], Y[i, j]
                            mat_copy["fractions"][anions[2]] = max(0.0, 1.0 - X[i, j] - Y[i, j])
                
                if valid:
                    vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
                    eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                    Z_VBO[i, j], Z_CBO[i, j] = vbo, vbo + eg
                else:
                    Z_VBO[i, j], Z_CBO[i, j] = np.nan, np.nan
                    
        xlabel = f"Udział {cations[0]}" if n_cat >= 2 else f"Udział {anions[0]}"
        ylabel = f"Udział {anions[0]}" if n_cat == 2 and n_an == 2 else f"Udział {cations[1] if n_cat==3 else anions[1]}"
        return True, X, Y, Z_VBO, Z_CBO, xlabel, ylabel
    else:
        x_steps = [i / 100.0 for i in range(101)]
        vbo_coords, cbo_coords = [], []
        var_el = cations[0] if len(cations) == 2 else (anions[0] if len(anions) == 2 else None)
        dep_el = cations[1] if len(cations) == 2 else (anions[1] if len(anions) == 2 else None)
        
        for step in x_steps:
            if var_el:
                mat_copy["fractions"][var_el], mat_copy["fractions"][dep_el] = step, 1.0 - step
            vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
            eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
            vbo_coords.append(vbo)
            cbo_coords.append(vbo + eg)
            
        label = f"Udział {var_el} (x)" if var_el else "Skład niezmienny"
        return False, x_steps, None, vbo_coords, cbo_coords, label, ""

# ==========================================
# NOWOŚĆ: GENEROWANIE ZALEŻNOŚCI MAS OD SKŁADU
# ==========================================
def calculate_mass_dependency(material, database):
    """Zwraca dane do wykresu zależności mas efektywnych (elektronów i ciężkich dziur Z) od składu."""
    import numpy as np
    cations, anions = material["cations"], material["anions"]
    n_cat, n_an = len(cations), len(anions)
    mat_copy = copy.deepcopy(material)
    m0 = 1.0

    if (n_cat == 2 and n_an == 2) or (n_cat == 3 and n_an == 1) or (n_cat == 1 and n_an == 3):
        N = 41
        vec = np.linspace(0.0, 1.0, N)
        X, Y = np.meshgrid(vec, vec)
        Z_me, Z_mhh, Z_mlh, Z_mhh110, Z_mlh110, Z_mhh111, Z_mlh111, Z_SO = np.zeros_like(X), np.zeros_like(X), np.zeros_like(X), np.zeros_like(X), np.zeros_like(X), np.zeros_like(X), np.zeros_like(X), np.zeros_like(X)

        for i in range(N):
            for j in range(N):
                if n_cat == 2 and n_an == 2:
                    mat_copy["fractions"][cations[0]], mat_copy["fractions"][cations[1]] = X[i, j], 1.0 - X[i, j]
                    mat_copy["fractions"][anions[0]], mat_copy["fractions"][anions[1]] = Y[i, j], 1.0 - Y[i, j]
                    valid = True
                else:
                    valid = (X[i, j] + Y[i, j] <= 1.00001)
                    if valid:
                        if n_cat == 3:
                            mat_copy["fractions"][cations[0]], mat_copy["fractions"][cations[1]] = X[i, j], Y[i, j]
                            mat_copy["fractions"][cations[2]] = max(0.0, 1.0 - X[i, j] - Y[i, j])
                        else:
                            mat_copy["fractions"][anions[0]], mat_copy["fractions"][anions[1]] = X[i, j], Y[i, j]
                            mat_copy["fractions"][anions[2]] = max(0.0, 1.0 - X[i, j] - Y[i, j])

                if valid:
                    Eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                    dSO = mix_parameter("deltaSO", cations, anions, mat_copy["fractions"], database)
                    g1 = mix_parameter("gamma1", cations, anions, mat_copy["fractions"], database)
                    g2 = mix_parameter("gamma2", cations, anions, mat_copy["fractions"], database)
                    g3 = mix_parameter("gamma3", cations, anions, mat_copy["fractions"], database)
                    F = mix_parameter("F", cations, anions, mat_copy["fractions"], database)
                    Ep = mix_parameter("Ep", cations, anions, mat_copy["fractions"], database)

                    Z_me[i, j] = electron_Effective(m0, F, Ep, Eg, dSO)
                    Z_mhh[i, j] = heavyHole_Effective_Z(m0, g1, g2)
                    Z_mlh[i, j] = lightHole_Effective_Z(m0, g1, g2)
                    Z_mhh110[i, j] = heavyHole_Effective_110(m0,g1,g2,g3)
                    Z_mlh110[i, j] = lightHole_Effective_110(m0,g1,g2,g3)
                    Z_mhh111[i, j] = heavyHole_Effective_111(m0,g1,g3)
                    Z_mlh111[i, j] = lightHole_Effective_111(m0,g1,g3)
                    Z_SO[i, j] = spinorbital_Effective(m0,g1,Eg,Ep,dSO)
                else:
                    Z_me[i, j], Z_mhh[i, j], Z_mlh[i, j], Z_mhh110[i, j], Z_mlh110[i, j], Z_mhh111[i, j], Z_mlh111[i, j], Z_SO[i, j] = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

        xlabel = f"Udział {cations[0]}" if n_cat >= 2 else f"Udział {anions[0]}"
        ylabel = f"Udział {anions[0]}" if n_cat == 2 and n_an == 2 else f"Udział {cations[1] if n_cat==3 else anions[1]}"
        return True, X, Y, Z_me, Z_mhh, Z_mlh, Z_mhh110, Z_mlh110, Z_mhh111, Z_mlh111, xlabel, ylabel, Z_SO
    else:
        x_steps = [i / 100.0 for i in range(101)]
        me_coords, mhh_coords, mlh_coords, mhh111_coords, mlh111_coords, mhh110_coords, mlh110_coords, so_coords = [], [], [], [], [], [], [], [], []
        var_el = cations[0] if len(cations) == 2 else (anions[0] if len(anions) == 2 else None)
        dep_el = cations[1] if len(cations) == 2 else (anions[1] if len(anions) == 2 else None)

        for step in x_steps:
            if var_el:
                mat_copy["fractions"][var_el], mat_copy["fractions"][dep_el] = step, 1.0 - step
            Eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
            dSO = mix_parameter("deltaSO", cations, anions, mat_copy["fractions"], database)
            g1 = mix_parameter("gamma1", cations, anions, mat_copy["fractions"], database)
            g2 = mix_parameter("gamma2", cations, anions, mat_copy["fractions"], database)
            g3 = mix_parameter("gamma3", cations, anions, mat_copy["fractions"], database)
            F = mix_parameter("F", cations, anions, mat_copy["fractions"], database)
            Ep = mix_parameter("Ep", cations, anions, mat_copy["fractions"], database)

            me_coords.append(electron_Effective(m0, F, Ep, Eg, dSO))
            mhh_coords.append(heavyHole_Effective_Z(m0, g1, g2))
            mlh_coords.append(lightHole_Effective_Z(m0, g1, g2))
            mhh111_coords.append(heavyHole_Effective_111(m0,g1,g3))
            mlh111_coords.append(lightHole_Effective_111(m0,g1,g3))
            mhh110_coords.append(heavyHole_Effective_110(m0,g1,g2,g3))
            mlh110_coords.append(lightHole_Effective_110(m0,g1,g2,g3))
            so_coords.append(spinorbital_Effective(m0,g1,Eg,Ep,dSO))

        label = f"Udział {var_el} (x)" if var_el else "Skład niezmienny"
        return False, x_steps, me_coords, mhh_coords, mlh_coords, mhh111_coords, mlh111_coords, mhh110_coords, mlh110_coords, label, "", so_coords

# ==========================================
# GLÓWNA FUNKCJA OBLICZENIOWA
# ==========================================
def calculate(material, database):
    cations = material["cations"]
    anions = material["anions"]
    fractions = material["fractions"]

    if len(cations) == 0: return "Brak kationów"
    if len(anions) == 0: return "Brak anionów"
    
    n_cat, n_an = len(cations), len(anions)
    
    if (n_cat <= 3 and n_an <= 1) or (n_cat <= 1 and n_an <= 3) or (n_cat == 2 and n_an == 2):
        # Miksowanie standardowych parametrów pasmowych i strukturalnych
        Eg = mix_parameter("Eg", cations, anions, fractions, database)
        VBO = mix_parameter("VBO", cations, anions, fractions, database)
        ac = mix_parameter("ac", cations, anions, fractions, database)
        av = mix_parameter("av", cations, anions, fractions, database)
        b = mix_parameter("b", cations, anions, fractions, database)
        a_mix = mix_parameter("a", cations, anions, fractions, database)
        c11 = mix_parameter("c11", cations, anions, fractions, database)
        c12 = mix_parameter("c12", cations, anions, fractions, database)
        deltaSO = mix_parameter("deltaSO", cations, anions, fractions, database)
        CBO = VBO + Eg
        
        # MIKXOWANIE PARAMETRÓW DO MAS EFEKTYWNYCH
        gamma1 = mix_parameter("gamma1", cations, anions, fractions, database)
        gamma2 = mix_parameter("gamma2", cations, anions, fractions, database)
        gamma3 = mix_parameter("gamma3", cations, anions, fractions, database)
        F = mix_parameter("F", cations, anions, fractions, database)
        Ep = mix_parameter("Ep", cations, anions, fractions, database)
        
        # Obliczenie punktowych mas efektywnych (w jednostkach m0)
        m0 = 1.0
        m_e = electron_Effective(m0, F, Ep, Eg, deltaSO)
        m_hhz = heavyHole_Effective_Z(m0, gamma1, gamma2)
        m_hh111 = heavyHole_Effective_111(m0, gamma1, gamma3)
        m_hh110 = heavyHole_Effective_110(m0, gamma1, gamma2, gamma3)
        m_lhz = lightHole_Effective_Z(m0, gamma1, gamma2)
        m_lh110 = lightHole_Effective_110(m0, gamma1, gamma2, gamma3)
        m_lh111 = lightHole_Effective_111(m0, gamma1, gamma3)
        m_so = spinorbital_Effective(m0, gamma1, Eg, Ep, deltaSO)

        # Zapis do stanu aplikacji
        app_state.mixed_material = {
            "Eg": Eg, "VBO": VBO, "CBO": CBO, "a": a_mix,
            "ac": ac, "av": av, "b": b, "c11": c11, "c12": c12, "deltaSO": deltaSO,
            "gamma1": gamma1, "gamma2": gamma2, "gamma3": gamma3, "F": F, "Ep": Ep,
            "me": m_e, "mhh_z": m_hhz, "mhh_111": m_hh111, "mhh_110": m_hh110, "mlh_z": m_lhz, "mlh_110": m_lh110, "mlh_111": m_lh111, "mso": m_so
        }

        # Budowanie czytelnego wyniku tekstowego
        result = "====================================\n"
        result += "MATERIAŁ (SKŁAD)\n"
        result += "====================================\n\nKationy:\n"
        for c in cations: result += f"  {c}: {fractions[c]:.3f}\n"
        result += "\nAniony:\n"
        for a in anions: result += f"  {a}: {fractions[a]:.3f}\n"
        
        result += "\n====================================\n"
        result += "PARAMETRY PASMOWE I STRUKTURALNE\n"
        result += "====================================\n"
        result += f"Eg  = {Eg:.4f} eV\nVB  = {VBO:.4f} eV\nCB  = {CBO:.4f} eV\n"
        result += f"a   = {a_mix:.4f} Å\nc11 = {c11:.4f}\nc12 = {c12:.4f}\n"
        
        result += "\n====================================\n"
        result += "MASY EFEKTYWNE (w jednostkach m0)\n"
        result += "====================================\n"
        result += f"m_e (elektron)         = {m_e:.4f}\n"
        result += f"m_hhZ (ciężka dziura Z) = {m_hhz:.4f}\n"
        result += f"m_lhZ (lekka dziura Z)  = {m_lhz:.4f}\n"
        result += f"m_so (spin-orbitalna)   = {m_so:.4f}\n"
        result += "====================================\n"
        return result

    return "Ten typ materiału nie jest jeszcze obsługiwany"