# -*- coding: utf-8 -*-

# ==========================================
#STANDARD DO TEGO JAK POBIERA Z BAZY DANYCH INFO
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

    materials = database["binary_materials"]

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
    # TERNARY:
    # In_x Ga_(1-x) As
    # ======================================
    if len(cations) == 2 and len(anions) == 1:

        # ==================================
        # SKŁADNIKI
        # ==================================
        cat1 = cations[0]

        cat2 = cations[1]

        an = anions[0]

        # ==================================
        # SKŁAD
        # ==================================
        x = fractions[cat1]

        # ==================================
        # SZUKANIE BINARY
        # ==================================
        name1, mat1 = find_material(
            database,
            cat1,
            an
        )

        name2, mat2 = find_material(
            database,
            cat2,
            an
        )

        # ==================================
        # SPRAWDZENIE
        # ==================================
        if mat1 is None:

            return (
                f"Nie znaleziono:\n"
                f"{cat1 + an}\n"
                f"ani\n"
                f"{an + cat1}"
            )

        if mat2 is None:

            return (
                f"Nie znaleziono:\n"
                f"{cat2 + an}\n"
                f"ani\n"
                f"{an + cat2}"
            )

        # ==================================
        # BOWING
        # ==================================
        bowing_name = cat1 + cat2 + an

        bowing = find_bowing(
            database,
            bowing_name
        )

        # ==================================
        # SUBSTRATE
        # ==================================
        substrate = mat2

        # ==================================
        # Eg
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
        # ac
        # ==================================
        ac = mix(
            x,
            mat1["ac"],
            mat2["ac"],
            0
        )

        # ==================================
        # av
        # ==================================
        av = mix(
            x,
            mat1["av"],
            mat2["av"],
            0
        )

        # ==================================
        # b
        # ==================================
        b = mix(
            x,
            mat1["b"],
            mat2["b"],
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
            mat1["c11"],
            mat2["c11"],
            0
        )

        c12 = mix(
            x,
            mat1["c12"],
            mat2["c12"],
            0
        )

        # ==================================
        # strain
        # ==================================
        ex = (
            substrate["a"] - a_mix
        ) / a_mix

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
        # TEKST
        # ==================================
        result = ""

        result += "====================================\n"

        result += "MATERIAŁ\n"

        result += "====================================\n\n"

        result += (
            f"{cat1}_{x:.2f}"
            f"{cat2}_{1-x:.2f}"
            f"{an}\n\n"
        )

        result += "====================================\n"

        result += "BINARY\n"

        result += "====================================\n\n"

        result += f"{name1}\n"

        result += f"{name2}\n\n"

        result += "====================================\n"

        result += "PARAMETRY\n"

        result += "====================================\n\n"

        result += f"Eg = {Eg:.4f} eV\n"

        result += f"VBO = {VBO:.4f} eV\n"

        result += f"CBO = {CBO:.4f} eV\n\n"

        result += f"a = {a_mix:.4f} A\n\n"

        result += f"c11 = {c11:.4f}\n"

        result += f"c12 = {c12:.4f}\n\n"

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