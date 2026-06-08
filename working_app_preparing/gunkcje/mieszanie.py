# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:59:22 2026

@author: miaudia
"""

import app_state
import copy

# ==========================================
# FUNKCJA DO APLIKACJI
# plik: funkcje/naprezenia.py
# ==========================================


# ==========================================
# MIESZANIE
# ==========================================
def mix(x, A, B, bowing=0):

    return (1 - x) * B + x * A - x * (1 - x) * bowing


# ==========================================
# SZUKANIE MATERIAŁU
# ==========================================
def find_material(database, el1, el2):

    materials = database["binary materials"]

    # ======================================
    # A + B
    # ======================================
    name1 = el1 + el2

    if name1 in materials:

        return name1, materials[name1]

    # ======================================
    # B + A
    # ======================================
    name2 = el2 + el1

    if name2 in materials:

        return name2, materials[name2]

    # ======================================
    # BRAK
    # ======================================
    return None, None


# ==========================================
# SZUKANIE BOWING
# ==========================================
def find_bowing(database, name):

    bowings = database["bowing"]

    if name in bowings:

        return bowings[name]

    return {

        "Eg": 0,

        "VBO": 0
    }

def mix_parameter(
        parameter,
        cations,
        anions,
        fractions,
        database):

    n_cat = len(cations)
    n_an = len(anions)

    # =====================================
    # BINARKA
    # =====================================

    if n_cat == 1 and n_an == 1:

        _, mat = find_material(
            database,
            cations[0],
            anions[0]
        )

        if mat is None:
            raise ValueError(
                f"Nie znaleziono materiału "
                f"{cations[0]}{anions[0]}"
            )

        return mat[parameter]

    # =====================================
    # TRÓJNARKA (2+1)
    # InGaAs
    # =====================================

    elif n_cat == 2 and n_an == 1:

        cat1 = cations[0]
        cat2 = cations[1]

        an = anions[0]

        x = fractions[cat1]

        _, mat1 = find_material(
            database,
            cat1,
            an
        )

        _, mat2 = find_material(
            database,
            cat2,
            an
        )

        bowing = find_bowing(
            database,
            cat1 + cat2 + an
        )

        return mix(
            x,
            mat1[parameter],
            mat2[parameter],
            bowing.get(parameter, 0)
        )

    # =====================================
    # TRÓJNARKA (1+2)
    # GaAsP
    # =====================================

    elif n_cat == 1 and n_an == 2:

        cat = cations[0]

        an1 = anions[0]
        an2 = anions[1]

        y = fractions[an1]

        _, mat1 = find_material(
            database,
            cat,
            an1
        )

        _, mat2 = find_material(
            database,
            cat,
            an2
        )

        bowing = find_bowing(
            database,
            cat + an1 + an2
        )

        return mix(
            y,
            mat1[parameter],
            mat2[parameter],
            bowing.get(parameter, 0)
        )

    # =====================================
    # CZWÓRKA (2+2)
    # InGaAsP
    # =====================================

    elif n_cat == 2 and n_an == 2:

        cat1 = cations[0]
        cat2 = cations[1]

        an1 = anions[0]
        an2 = anions[1]

        x = fractions[cat1]
        y = fractions[an1]

        _, m11 = find_material(
            database,
            cat1,
            an1
        )

        _, m21 = find_material(
            database,
            cat2,
            an1
        )

        _, m12 = find_material(
            database,
            cat1,
            an2
        )

        _, m22 = find_material(
            database,
            cat2,
            an2
        )

        return (
              x*y*m11[parameter]
            + (1-x)*y*m21[parameter]
            + x*(1-y)*m12[parameter]
            + (1-x)*(1-y)*m22[parameter]
        )

    # =====================================
    # CZWÓRKA (3+1)
    # AlGaInAs
    # =====================================

    elif n_cat == 3 and n_an == 1:

        an = anions[0]

        value = 0

        for cat in cations:

            frac = fractions[cat]

            _, mat = find_material(
                database,
                cat,
                an
            )

            value += frac * mat[parameter]

        return value

    # =====================================
    # CZWÓRKA (1+3)
    # GaAsPSb
    # =====================================

    elif n_cat == 1 and n_an == 3:

        cat = cations[0]

        value = 0

        for an in anions:

            frac = fractions[an]

            _, mat = find_material(
                database,
                cat,
                an
            )

            value += frac * mat[parameter]

        return value

    # =====================================
    # BRAK OBSŁUGI
    # =====================================

    raise ValueError(
        f"Nieobsługiwany skład: "
        f"{n_cat} kationów i {n_an} anionów"
    )


# ==========================================
# GENEROWANIE ZALEŻNOŚCI PASM OD SKŁADU
# ==========================================
def calculate_band_dependency(material, database):
    import numpy as np  # Import wewnątrz funkcji dla zachowania spójności środowiska graficznego
    
    cations = material["cations"]
    anions = material["anions"]
    fractions = material["fractions"]
    
    n_cat = len(cations)
    n_an = len(anions)
    mat_copy = copy.deepcopy(material)
    
    # Obsługa wykresów 3D dla kombinacji 2:2, 3:1, 1:3
    if (n_cat == 2 and n_an == 2) or (n_cat == 3 and n_an == 1) or (n_cat == 1 and n_an == 3):
        N = 41  # Rozdzielczość siatki 3D
        vec = np.linspace(0.0, 1.0, N)
        X, Y = np.meshgrid(vec, vec)
        Z_VBO = np.zeros_like(X)
        Z_CBO = np.zeros_like(X)
        
        if n_cat == 2 and n_an == 2:
            var_cat = cations[0]
            dep_cat = cations[1]
            var_an = anions[0]
            dep_an = anions[1]
            
            for i in range(N):
                for j in range(N):
                    x = X[i, j]
                    y = Y[i, j]
                    mat_copy["fractions"][var_cat] = x
                    mat_copy["fractions"][dep_cat] = 1.0 - x
                    mat_copy["fractions"][var_an] = y
                    mat_copy["fractions"][dep_an] = 1.0 - y
                    
                    vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
                    eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                    Z_VBO[i, j] = vbo
                    Z_CBO[i, j] = vbo + eg
                    
            xlabel = f"Udział kationu {var_cat} (x)"
            ylabel = f"Udział anionu {var_an} (y)"
            
        elif n_cat == 3 and n_an == 1:
            c1, c2, c3 = cations[0], cations[1], cations[2]
            
            for i in range(N):
                for j in range(N):
                    x1 = X[i, j]
                    x2 = Y[i, j]
                    if x1 + x2 <= 1.00001:
                        x3 = max(0.0, 1.0 - x1 - x2)
                        mat_copy["fractions"][c1] = x1
                        mat_copy["fractions"][c2] = x2
                        mat_copy["fractions"][c3] = x3
                        
                        vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
                        eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                        Z_VBO[i, j] = vbo
                        Z_CBO[i, j] = vbo + eg
                    else:
                        Z_VBO[i, j] = np.nan
                        Z_CBO[i, j] = np.nan
                        
            xlabel = f"Udział kationu {c1} (x1)"
            ylabel = f"Udział kationu {c2} (x2)"
            
        elif n_cat == 1 and n_an == 3:
            a1, a2, a3 = anions[0], anions[1], anions[2]
            
            for i in range(N):
                for j in range(N):
                    y1 = X[i, j]
                    y2 = Y[i, j]
                    if y1 + y2 <= 1.00001:
                        y3 = max(0.0, 1.0 - y1 - y2)
                        mat_copy["fractions"][a1] = y1
                        mat_copy["fractions"][a2] = y2
                        mat_copy["fractions"][a3] = y3
                        
                        vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
                        eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                        Z_VBO[i, j] = vbo
                        Z_CBO[i, j] = vbo + eg
                    else:
                        Z_VBO[i, j] = np.nan
                        Z_CBO[i, j] = np.nan
                        
            xlabel = f"Udział anionu {a1} (y1)"
            ylabel = f"Udział anionu {a2} (y2)"
            
        return True, X, Y, Z_VBO, Z_CBO, xlabel, ylabel

    else:
        # Standardowy wykres 2D dla pozostałych kombinacji
        x_steps = [i / 100.0 for i in range(101)]
        vbo_coords = []
        cbo_coords = []
        
        if len(cations) == 2 and len(anions) == 1:
            var_el = cations[0]
            dep_el = cations[1]
            for x in x_steps:
                mat_copy["fractions"][var_el] = x
                mat_copy["fractions"][dep_el] = 1.0 - x
                vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
                eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                vbo_coords.append(vbo)
                cbo_coords.append(vbo + eg)
            label = f"Udział kationu {var_el} (x)"
            
        elif len(cations) == 1 and len(anions) == 2:
            var_el = anions[0]
            dep_el = anions[1]
            for y in x_steps:
                mat_copy["fractions"][var_el] = y
                mat_copy["fractions"][dep_el] = 1.0 - y
                vbo = mix_parameter("VBO", cations, anions, mat_copy["fractions"], database)
                eg = mix_parameter("Eg", cations, anions, mat_copy["fractions"], database)
                vbo_coords.append(vbo)
                cbo_coords.append(vbo + eg)
            label = f"Udział anionu {var_el} (y)"
            
        else:
            for x in x_steps:
                vbo = mix_parameter("VBO", cations, anions, fractions, database)
                eg = mix_parameter("Eg", cations, anions, fractions, database)
                vbo_coords.append(vbo)
                cbo_coords.append(vbo + eg)
            label = "Skład niezmienny (materiały binarne)"
            
        return False, x_steps, None, vbo_coords, cbo_coords, label, ""


# ==========================================
# CALCULATE
# ==========================================
def calculate(material, database):

    # ======================================
    # POBRANIE
    # ======================================
    cations = material["cations"]

    anions = material["anions"]

    fractions = material["fractions"]

    # ======================================
    # SPRAWDZENIE
    # ======================================
    if len(cations) == 0:

        return "Brak kationów"

    if len(anions) == 0:

        return "Brak anionów"

    # ======================================
    # OBSŁUGIWANE MATERIAŁY
    # ======================================
    
    n_cat = len(cations)
    n_an = len(anions)
    
    if (
        (n_cat == 1 and n_an == 1) or
        (n_cat == 2 and n_an == 1) or
        (n_cat == 1 and n_an == 2) or
        (n_cat == 2 and n_an == 2) or
        (n_cat == 3 and n_an == 1) or
        (n_cat == 1 and n_an == 3)
    ):

        # ==================================
        # Eg
        # ==================================
        Eg = mix_parameter(
            "Eg",
            cations,
            anions,
            fractions,
            database
        )
        
        VBO = mix_parameter(
            "VBO",
            cations,
            anions,
            fractions,
            database
        )
        
        ac = mix_parameter(
            "ac",
            cations,
            anions,
            fractions,
            database
        )
        
        av = mix_parameter(
            "av",
            cations,
            anions,
            fractions,
            database
        )
        
        b = mix_parameter(
            "b",
            cations,
            anions,
            fractions,
            database
        )
        
        a_mix = mix_parameter(
            "a",
            cations,
            anions,
            fractions,
            database
        )
        
        c11 = mix_parameter(
            "c11",
            cations,
            anions,
            fractions,
            database
        )
        
        c12 = mix_parameter(
            "c12",
            cations,
            anions,
            fractions,
            database
        )
        
        deltaSO = mix_parameter(
            "deltaSO",
            cations,
            anions,
            fractions,
            database
        )
        
        CBO = VBO + Eg
        
        app_state.mixed_material = {
            "Eg": Eg,
            "VBO": VBO,
            "CBO": CBO,
            "a": a_mix,
            "ac": ac,
            "av": av,
            "b": b,
            "c11": c11,
            "c12": c12,
            "deltaSO": deltaSO
        }

        # ==================================
        # TEKST
        # ==================================
        result = ""

        result += "====================================\n"

        result += "MATERIAŁ\n"

        result += "====================================\n\n"

        result += "Kationy:\n"

        for c in cations:
            result += (
                f"{c}: "
                f"{fractions[c]:.3f}\n"
            )
        
        result += "\nAniony:\n"
        
        for a in anions:
            result += (
                f"{a}: "
                f"{fractions[a]:.3f}\n"
            )
        
        result += "\n"

        result += "====================================\n"


        result += "PARAMETRY\n"

        result += "====================================\n\n"

        result += f"Eg = {Eg:.4f} eV\n"

        result += f"VB = {VBO:.4f} eV\n"

        result += f"CB = {CBO:.4f} eV\n\n"

        result += f"a = {a_mix:.4f} A\n\n"

        result += f"c11 = {c11:.4f}\n"

        result += f"c12 = {c12:.4f}\n\n"

        result += "====================================\n"

        return result

    # ======================================
    # BRAK OBSŁUGI
    # ======================================
    return "Ten typ materiału nie jest jeszcze obsługiwany"