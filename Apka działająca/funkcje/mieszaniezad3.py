# -*- coding: utf-8 -*-

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
# CALCULATE
# ==========================================
def calculate(material, database):

    # ======================================
    # POBRANIE SKŁADNIKÓW
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
    # TERNARY
    # InGaAs
    # ======================================
    if len(cations) == 2 and len(anions) == 1:

        cat1 = cations[0]

        cat2 = cations[1]

        an = anions[0]

        # ==================================
        # binary names
        # ==================================
        binary1 = cat1 + an

        binary2 = cat2 + an

        # ==================================
        # dane materiałów
        # ==================================
        mat1 = database["binary_materials"][binary1]

        mat2 = database["binary_materials"][binary2]

        # ==================================
        # dane pierwiastków
        # ==================================
        el1 = database["elements"][cat1]

        el2 = database["elements"][cat2]

        # ==================================
        # bowing
        # ==================================
        bowing_name = cat1 + cat2 + an

        bowing = database["bowing"][bowing_name]

        # ==================================
        # skład
        # ==================================
        x = fractions[cat1]

        # ==================================
        # bandgap
        # ==================================
        Eg = mix(
            x,
            mat1["Eg"],
            mat2["Eg"],
            bowing["Eg"]
        )

        # ==================================
        # VBO
        # ==================================
        VBO = mix(
            x,
            mat1["VBO"],
            mat2["VBO"],
            bowing["VBO"]
        )

        # ==================================
        # CBO
        # ==================================
        CBO = VBO + Eg

        # ==================================
        # deformation potentials
        # ==================================
        ac = mix(
            x,
            el1["ac"],
            el2["ac"],
            2.61
        )

        av = mix(
            x,
            el1["av"],
            el2["av"],
            0
        )

        b = mix(
            x,
            el1["b"],
            el2["b"],
            0
        )

        # ==================================
        # lattice constant
        # ==================================
        a_mix = mix(
            x,
            mat1["a"],
            mat2["a"],
            0
        )

        # ==================================
        # elastic constants
        # ==================================
        c11 = mix(
            x,
            el1["c11"],
            el2["c11"],
            0
        )

        c12 = mix(
            x,
            el1["c12"],
            el2["c12"],
            0
        )

        # ==================================
        # strain
        # substrate = material 2
        # ==================================
        ex = (mat2["a"] - a_mix) / a_mix

        ez = -(2.0) * ex * (c12 / c11)

        # ==================================
        # energy shifts
        # ==================================
        deltaEc = ac * (2 * ex + ez)

        deltaEv = av * (2 * ex + ez)

        deltaEs = b * (ex - ez)

        # ==================================
        # final bands
        # ==================================
        Ec = CBO + deltaEc

        EHH = VBO + deltaEv + deltaEs

        ELH = VBO + deltaEv - deltaEs

        # ==================================
        # tekst wyniku
        # ==================================
        result = ""

        result += "====================================\n"

        result += "MATERIAŁ\n"

        result += "====================================\n\n"

        result += f"{cat1}_{x:.2f}{cat2}_{1-x:.2f}{an}\n\n"

        result += "====================================\n"

        result += "PARAMETRY\n"

        result += "====================================\n\n"

        result += f"x = {x:.3f}\n"

        result += f"Eg = {Eg:.4f} eV\n"

        result += f"VBO = {VBO:.4f} eV\n"

        result += f"CBO = {CBO:.4f} eV\n\n"

        result += f"a = {a_mix:.4f} A\n\n"

        result += f"ex = {ex:.6f}\n"

        result += f"ez = {ez:.6f}\n\n"

        result += "====================================\n"

        result += "PASMA\n"

        result += "====================================\n\n"

        result += f"Ec  = {Ec:.4f} eV\n"

        result += f"EHH = {EHH:.4f} eV\n"

        result += f"ELH = {ELH:.4f} eV\n"

        return result

    # ======================================
    # BRAK OBSŁUGI
    # ======================================
    return "Ten typ materiału nie jest jeszcze obsługiwany"