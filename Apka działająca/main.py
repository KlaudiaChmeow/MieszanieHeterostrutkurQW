# -*- coding: utf-8 -*-

import os
import json
import importlib.util
import tkinter as tk
from tkinter import ttk


# ==========================================
# ŚCIEŻKI
# ==========================================
MATERIALY_PATH = "materialy.json"
FUNKCJE_PATH = "./funkcje"


# ==========================================
# PRESETY
# ==========================================
PRESETS = {

    "InGaAs": {

        "cat1": "In",
        "cat2": "Ga",

        "an1": "As",
        "an2": "",

        "x1": "0.2",
        "x2": "0.8",

        "y1": "1.0",
        "y2": "0.0"
    },

    "AlGaAs": {

        "cat1": "Al",
        "cat2": "Ga",

        "an1": "As",
        "an2": "",

        "x1": "0.3",
        "x2": "0.7",

        "y1": "1.0",
        "y2": "0.0"
    },

    "InAsP": {

        "cat1": "In",
        "cat2": "",

        "an1": "As",
        "an2": "P",

        "x1": "1.0",
        "x2": "0.0",

        "y1": "0.4",
        "y2": "0.6"
    }
}


# ==========================================
# ŁADOWANIE JSON
# ==========================================
def load_database():

    with open(MATERIALY_PATH, "r", encoding="utf-8") as f:

        return json.load(f)


database = load_database()


# ==========================================
# ŁADOWANIE PIERWIASTKÓW
# ==========================================
def load_elements():

    return list(database["elements"].keys())


# ==========================================
# ŁADOWANIE FUNKCJI
# ==========================================
def load_functions():

    funcs = []

    try:

        for file in os.listdir(FUNKCJE_PATH):

            if file.endswith(".py"):

                funcs.append(file[:-3])

    except Exception as e:

        print("Błąd folderu funkcji:", e)

    return funcs


# ==========================================
# IMPORT FUNKCJI
# ==========================================
def import_function(module_name):

    path = os.path.join(
        FUNKCJE_PATH,
        module_name + ".py"
    )

    spec = importlib.util.spec_from_file_location(
        module_name,
        path
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


# ==========================================
# NORMALIZACJA
# ==========================================
def normalize(x1, x2):

    x1 = float(x1)
    x2 = float(x2)

    s = x1 + x2

    if s == 0:

        return 0, 0

    return x1 / s, x2 / s


# ==========================================
# TWORZENIE MATERIAŁU
# ==========================================
def create_material_dict():

    material = {

        "cations": [],
        "anions": [],
        "fractions": {}
    }

    # ======================================
    # POBRANIE
    # ======================================
    cat1 = cation1_var.get()
    cat2 = cation2_var.get()

    an1 = anion1_var.get()
    an2 = anion2_var.get()

    x1 = x1_var.get()
    x2 = x2_var.get()

    y1 = y1_var.get()
    y2 = y2_var.get()

    # ======================================
    # NORMALIZACJA
    # ======================================
    x1, x2 = normalize(x1, x2)

    y1, y2 = normalize(y1, y2)

    # ======================================
    # KATIONY
    # ======================================
    if cat1 != "":

        material["cations"].append(cat1)

        material["fractions"][cat1] = x1

    if cat2 != "":

        material["cations"].append(cat2)

        material["fractions"][cat2] = x2

    # ======================================
    # ANIONY
    # ======================================
    if an1 != "":

        material["anions"].append(an1)

        material["fractions"][an1] = y1

    if an2 != "":

        material["anions"].append(an2)

        material["fractions"][an2] = y2

    return material


# ==========================================
# ŁADOWANIE PRESETU
# ==========================================
def load_preset(event=None):

    name = preset_var.get()

    if name not in PRESETS:

        return

    p = PRESETS[name]

    cation1_var.set(p["cat1"])
    cation2_var.set(p["cat2"])

    anion1_var.set(p["an1"])
    anion2_var.set(p["an2"])

    x1_var.set(p["x1"])
    x2_var.set(p["x2"])

    y1_var.set(p["y1"])
    y2_var.set(p["y2"])


# ==========================================
# OBLICZENIA
# ==========================================
def calculate():

    func_name = function_var.get()

    material = create_material_dict()

    try:

        module = import_function(func_name)

        if hasattr(module, "calculate"):

            result = module.calculate(
                material,
                database
            )

            result_box.delete(
                "1.0",
                tk.END
            )

            result_box.insert(
                tk.END,
                result
            )

        else:

            result_box.delete(
                "1.0",
                tk.END
            )

            result_box.insert(
                tk.END,
                "Brak calculate()"
            )

    except Exception as e:

        result_box.delete(
            "1.0",
            tk.END
        )

        result_box.insert(
            tk.END,
            f"Błąd:\n{e}"
        )


# ==========================================
# DANE
# ==========================================
elements = load_elements()

functions = load_functions()


# ==========================================
# OKNO
# ==========================================
root = tk.Tk()

root.title("Heterostruktury")

root.geometry("1300x800")

root.configure(bg="#93a9db")


# ==========================================
# GRID
# ==========================================
root.grid_columnconfigure(0, weight=2)

root.grid_columnconfigure(1, weight=3)

root.grid_rowconfigure(0, weight=1)


# ==========================================
# LEWY PANEL
# ==========================================
left_frame = tk.Frame(

    root,

    bg="#cdd8f5",

    bd=2,

    relief="ridge",

    width=450
)

left_frame.grid(

    row=0,

    column=0,

    sticky="ns",

    padx=20,

    pady=20
)

left_frame.grid_propagate(False)


# ==========================================
# PRAWY PANEL
# ==========================================
right_frame = tk.Frame(

    root,

    bg="#dfe6f7",

    bd=2,

    relief="ridge"
)

right_frame.grid(

    row=0,

    column=1,

    sticky="nsew",

    padx=20,

    pady=20
)


# ==========================================
# VARIABLES
# ==========================================
preset_var = tk.StringVar()

cation1_var = tk.StringVar()
cation2_var = tk.StringVar()

anion1_var = tk.StringVar()
anion2_var = tk.StringVar()

x1_var = tk.StringVar(value="1.0")
x2_var = tk.StringVar(value="0.0")

y1_var = tk.StringVar(value="1.0")
y2_var = tk.StringVar(value="0.0")

function_var = tk.StringVar()


# ==========================================
# TYTUŁ
# ==========================================
title_label = tk.Label(

    left_frame,

    text="KALKULATOR HETEROSTRUKTUR",

    bg="#cdd8f5",

    font=("Arial", 16, "bold"),

    justify="center"
)

title_label.pack(pady=20)


# ==========================================
# PRESETY
# ==========================================
tk.Label(

    left_frame,

    text="Gotowa mieszanina",

    bg="#cdd8f5",

    font=("Arial", 11, "bold"),

    justify="center"

).pack(pady=5)


preset_dropdown = ttk.Combobox(

    left_frame,

    textvariable=preset_var,

    values=list(PRESETS.keys()),

    width=20,

    justify="center"

)

preset_dropdown.pack()

preset_dropdown.bind(
    "<<ComboboxSelected>>",
    load_preset
)


# ==========================================
# KATIONY
# ==========================================
tk.Label(

    left_frame,

    text="Kation 1",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Combobox(

    left_frame,

    textvariable=cation1_var,

    values=[""] + elements,

    width=20,

    justify="center"

).pack()


tk.Label(

    left_frame,

    text="Udział x1",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Entry(

    left_frame,

    textvariable=x1_var,

    width=22,

    justify="center"

).pack()


tk.Label(

    left_frame,

    text="Kation 2",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Combobox(

    left_frame,

    textvariable=cation2_var,

    values=[""] + elements,

    width=20,

    justify="center"

).pack()


tk.Label(

    left_frame,

    text="Udział x2",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Entry(

    left_frame,

    textvariable=x2_var,

    width=22,

    justify="center"

).pack()


# ==========================================
# ANIONY
# ==========================================
tk.Label(

    left_frame,

    text="Anion 1",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Combobox(

    left_frame,

    textvariable=anion1_var,

    values=[""] + elements,

    width=20,

    justify="center"

).pack()


tk.Label(

    left_frame,

    text="Udział y1",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Entry(

    left_frame,

    textvariable=y1_var,

    width=22,

    justify="center"

).pack()


tk.Label(

    left_frame,

    text="Anion 2",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Combobox(

    left_frame,

    textvariable=anion2_var,

    values=[""] + elements,

    width=20,

    justify="center"

).pack()


tk.Label(

    left_frame,

    text="Udział y2",

    bg="#cdd8f5",

    font=("Arial", 11),

    justify="center"

).pack(pady=5)


ttk.Entry(

    left_frame,

    textvariable=y2_var,

    width=22,

    justify="center"

).pack()


# ==========================================
# FUNKCJA
# ==========================================
tk.Label(

    left_frame,

    text="Funkcja",

    bg="#cdd8f5",

    font=("Arial", 11, "bold"),

    justify="center"

).pack(pady=5)


ttk.Combobox(

    left_frame,

    textvariable=function_var,

    values=functions,

    width=20,

    justify="center"

).pack()


# ==========================================
# BUTTON
# ==========================================
calculate_button = tk.Button(

    left_frame,

    text="Oblicz",

    command=calculate,

    font=("Arial", 12, "bold"),

    bg="#6d8edb",

    fg="white",

    activebackground="#5678c7",

    width=18,

    height=2,

    relief="flat"

)

calculate_button.pack(pady=30)


# ==========================================
# RESULT BOX
# ==========================================
result_box = tk.Text(

    right_frame,

    width=70,

    height=45,

    font=("Consolas", 11),

    bg="white",

    fg="#222222",

    wrap="word",

    bd=2,

    relief="solid"

)

result_box.tag_configure(

    "center",

    justify="center"

)

result_box.pack(

    fill="both",

    expand=True,

    padx=10,

    pady=10

)

# ==========================================
# START
# ==========================================
root.mainloop()