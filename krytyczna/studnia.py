import json


def mix(x, A, B, bowing=0.0):
    return (1 - x) * B + x * A - x * (1 - x) * bowing


# Wczytanie parametrów NAZWA JSON JAKA???
with open("materials.json", "r", encoding="utf-8") as f:
    materials = json.load(f)

InSb = materials["InSb"]
GaSb = materials["GaSb"]
bowing = materials["bowing"]

gora = dol1 = dol2 = 0.0

with open("GaInSb_naprezenia3.txt", "w") as plik:

    for i in range(101):

        x = i / 100.0

        Eg = mix(
            x,
            InSb["Eg"],
            GaSb["Eg"],
            bowing["Eg"]
        )

        VBO = mix(
            x,
            InSb["VBO"],
            GaSb["VBO"],
            bowing["VBO"]
        )

        CBO = VBO + Eg

        ac = mix(x, InSb["ac"], GaSb["ac"])
        av = mix(x, InSb["av"], GaSb["av"])
        b = mix(x, InSb["b"], GaSb["b"])

        a_InGaSb = (
            (1 - x) * GaSb["a"]
            + x * InSb["a"]
        )

        c11 = mix(x, InSb["c11"], GaSb["c11"])
        c12 = mix(x, InSb["c12"], GaSb["c12"])

        ex = (InSb["a"] - a_InGaSb) / a_InGaSb
        ez = -2.0 * ex * (c12 / c11)

        deltaEc = ac * (2 * ex + ez)
        deltaEv = av * (2 * ex + ez)
        deltaEs = b * (ex - ez)

        Ec = CBO + deltaEc
        EHH = VBO + deltaEv + deltaEs
        ELH = VBO + deltaEv - deltaEs

        if abs(x - 0.4) < 1e-9:
            gora = Ec
            dol1 = EHH
            dol2 = ELH

        plik.write(
            f"{x:.2f}\t{EHH:.6f}\t{Ec:.6f}\t{ELH:.6f}\t{VBO:.6f}\t{CBO:.6f}\n"
        )

print("Dane zapisane do pliku GaInSb_naprezenia3.txt")

with open("5_GaInSb3.txt", "w") as zad5:

    o = 0.0

    while o < 20:

        if o < 6 or o > 14:
            zad5.write(
                f"{o:.1f}\t"
                f"{GaSb['VBO'] + GaSb['Eg']:.6f}\t"
                f"{GaSb['VBO']:.6f}\t"
                f"{GaSb['VBO']:.6f}\n"
            )
        else:
            zad5.write(
                f"{o:.1f}\t{gora:.6f}\t{dol1:.6f}\t{dol2:.6f}\n"
            )

        o += 0.2