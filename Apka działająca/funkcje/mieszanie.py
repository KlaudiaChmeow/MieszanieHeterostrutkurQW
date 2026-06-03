# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:59:22 2026

@author: miaudia
"""

# -*- coding: utf-8 -*-

import app_state

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