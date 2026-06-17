# -*- coding: utf-8 -*-

import os
import json
import importlib.util
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
import app_state
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# ==========================================
# ŚCIEŻKI
# ==========================================
MATERIALY_PATH = "materialy.json"
FUNKCJE_PATH = "working_app\\gunkcje"


# ==========================================
# PRESETY
# ==========================================
PRESETS = {

    # ======================================
    # TRÓJNARKI
    # ======================================

    "InGaAs": {

        "cat1": "In",
        "cat2": "Ga",
        "cat3": "",

        "an1": "As",
        "an2": "",
        "an3": "",

        "x1": "0.2",
        "x2": "0.8",
        "x3": "0.0",

        "y1": "1.0",
        "y2": "0.0",
        "y3": "0.0"
    },

    "GaAsP": {

        "cat1": "Ga",
        "cat2": "",
        "cat3": "",

        "an1": "As",
        "an2": "P",
        "an3": "",

        "x1": "1.0",
        "x2": "0.0",
        "x3": "0.0",

        "y1": "0.8",
        "y2": "0.2",
        "y3": "0.0"
    },

    # ======================================
    # CZWÓRKI 2+2
    # ======================================

    "InGaAsP": {

        "cat1": "In",
        "cat2": "Ga",
        "cat3": "",

        "an1": "As",
        "an2": "P",
        "an3": "",

        "x1": "0.53",
        "x2": "0.47",
        "x3": "0.0",

        "y1": "0.75",
        "y2": "0.25",
        "y3": "0.0"
    },

    "InGaAsSb": {

        "cat1": "In",
        "cat2": "Ga",
        "cat3": "",

        "an1": "As",
        "an2": "Sb",
        "an3": "",

        "x1": "0.3",
        "x2": "0.7",
        "x3": "0.0",

        "y1": "0.5",
        "y2": "0.5",
        "y3": "0.0"
    },

    # ======================================
    # CZWÓRKI 3+1
    # ======================================

    "AlGaInAs": {

        "cat1": "Al",
        "cat2": "Ga",
        "cat3": "In",

        "an1": "As",
        "an2": "",
        "an3": "",

        "x1": "0.2",
        "x2": "0.3",
        "x3": "0.5",

        "y1": "1.0",
        "y2": "0.0",
        "y3": "0.0"
    },

    "AlGaInP": {

        "cat1": "Al",
        "cat2": "Ga",
        "cat3": "In",

        "an1": "P",
        "an2": "",
        "an3": "",

        "x1": "0.2",
        "x2": "0.3",
        "x3": "0.5",

        "y1": "1.0",
        "y2": "0.0",
        "y3": "0.0"
    },

    # ======================================
    # CZWÓRKI 1+3
    # ======================================

    "GaAsPSb": {

        "cat1": "Ga",
        "cat2": "",
        "cat3": "",

        "an1": "As",
        "an2": "P",
        "an3": "Sb",

        "x1": "1.0",
        "x2": "0.0",
        "x3": "0.0",

        "y1": "0.4",
        "y2": "0.3",
        "y3": "0.3"
    },

    "InAsPSb": {

        "cat1": "In",
        "cat2": "",
        "cat3": "",

        "an1": "As",
        "an2": "P",
        "an3": "Sb",

        "x1": "1.0",
        "x2": "0.0",
        "x3": "0.0",

        "y1": "0.4",
        "y2": "0.2",
        "y3": "0.4"
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
# UPEWNIENIE SIĘ ŻE RESULT BOX ISTNIEJE
# ==========================================
def ensure_result_box():
    global result_box
    try:
        if result_box and result_box.winfo_exists():
            return
    except:
        pass
        
    clear_right_frame()
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
    result_box.tag_configure("center", justify="center")
    result_box.pack(fill="both", expand=True, padx=10, pady=10)


# ==========================================
# ŁADOWANIE KATIONÓW
# ==========================================
def load_cations():

    result = []

    for el, data in database["elements"].items():

        if data.get("type") == "cation":

            result.append(el)

    return result


# ==========================================
# ŁADOWANIE ANIONÓW
# ==========================================
def load_anions():

    result = []

    for el, data in database["elements"].items():

        if data.get("type") == "anion":

            result.append(el)

    return result


# ==========================================
# TWORZENIE MATERIAŁU
# ==========================================
def create_material_dict():

    material = {

        "cations": [],
        "anions": [],
        "fractions": {}
    }

    cation_data = [

        (cation1_var.get(), x1_var.get()),
        (cation2_var.get(), x2_var.get()),
        (cation3_var.get(), x3_var.get())
    ]

    anion_data = [

        (anion1_var.get(), y1_var.get()),
        (anion2_var.get(), y2_var.get()),
        (anion3_var.get(), y3_var.get())
    ]

    for name, frac in cation_data:

        if name == "":
            continue

        material["cations"].append(name)

        material["fractions"][name] = float(frac)

    for name, frac in anion_data:

        if name == "":
            continue

        material["anions"].append(name)

        material["fractions"][name] = float(frac)

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
    cation3_var.set(p["cat3"])
    
    anion1_var.set(p["an1"])
    anion2_var.set(p["an2"])
    anion3_var.set(p["an3"])
    
    x1_var.set(p["x1"])
    x2_var.set(p["x2"])
    x3_var.set(p["x3"])
    
    y1_var.set(p["y1"])
    y2_var.set(p["y2"])
    y3_var.set(p["y3"])


# ==========================================
# WALIDACJA
# ==========================================
def validate_fractions():

    try:

        cation_values = [

            float(x1_var.get()),
            float(x2_var.get()),
            float(x3_var.get())
        ]

        anion_values = [

            float(y1_var.get()),
            float(y2_var.get()),
            float(y3_var.get())
        ]

    except:

        return False, "Udziały muszą być liczbami"
    
    if cation1_var.get() == cation2_var.get() and cation1_var.get() != "" and cation2_var.get() != "":
        return (False, "Nie można ustawiać takich samych materiałów")
    if cation1_var.get() == cation3_var.get() and cation1_var.get() != "" and cation3_var.get() != "":
        return (False, "Nie można ustawiać takich samych materiałów")
    if cation2_var.get() == cation3_var.get() and cation2_var.get() != "" and cation3_var.get() != "":
        return (False, "Nie można ustawiać takich samych materiałów")
    if anion1_var.get() == anion2_var.get() and anion1_var.get() != "" and anion2_var.get() != "":
        return (False, "Nie można ustawiać takich samych materiałów")
    if anion1_var.get() == anion3_var.get() and anion1_var.get() != "" and anion3_var.get() != "":
        return (False, "Nie można ustawiać takich samych materiałów")
    if anion2_var.get() == anion3_var.get() and anion2_var.get() != "" and anion3_var.get() != "":
        return (False, "Nie można ustawiać takich samych materiałów")
    
    for value in cation_values + anion_values:

        if value < 0 or value > 1:

            return (
                False,
                "Udziały muszą należeć do przedziału <0,1>"
            )

    active_cat = []

    if cation1_var.get() != "":
        active_cat.append(float(x1_var.get()))

    if cation2_var.get() != "":
        active_cat.append(float(x2_var.get()))

    if cation3_var.get() != "":
        active_cat.append(float(x3_var.get()))

    active_an = []

    if anion1_var.get() != "":
        active_an.append(float(y1_var.get()))

    if anion2_var.get() != "":
        active_an.append(float(y2_var.get()))

    if anion3_var.get() != "":
        active_an.append(float(y3_var.get()))

    eps = 1e-6

    if len(active_cat) > 0:

        if abs(sum(active_cat) - 1.0) > eps:

            return (
                False,
                f"Suma udziałów kationów = {sum(active_cat):.4f}\n"
                f"Musi wynosić 1"
            )

    if len(active_an) > 0:

        if abs(sum(active_an) - 1.0) > eps:

            return (
                False,
                f"Suma udziałów anionów = {sum(active_an):.4f}\n"
                f"Musi wynosić 1"
            )
        
    active_elements = 0

    for var in [
        cation1_var,
        cation2_var,
        cation3_var,
        anion1_var,
        anion2_var,
        anion3_var
    ]:

        if var.get() != "":
            active_elements += 1

    if active_elements > 4:

        return (
            False,
            "Maksymalnie można wybrać 4 składniki "
            "(kationy + aniony)"
        )

    return True, ""


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
# POKAZ PARAMETRY MATERIALU
# ==========================================
def show_material_parameters():

    ensure_result_box()
    result_box.delete("1.0", tk.END)

    result_box.insert(
        tk.END,
        "PARAMETRY MATERIAŁU\n\n"
    )

    result_box.insert(
        tk.END,
        f"Kationy: {app_state.current_material['cations']}\n"
    )

    result_box.insert(
        tk.END,
        f"Aniony: {app_state.current_material['anions']}\n"
    )
    
    
# ==========================================
# CLEAR LEFT
# ==========================================
def clear_left_frame():

    for widget in left_frame.winfo_children():
        widget.destroy()
        
        
# ==========================================
# NEXT
# ==========================================
def next_window():

    valid, message = validate_fractions()

    if not valid:

        tk.messagebox.showerror(
            "Błąd",
            message
        )
    
        return

    app_state.current_material = create_material_dict()

    show_substrate_screen()
    
    module = import_function("mieszanie")
    
    result = module.calculate(
        app_state.current_material,
        database
    )
    
    ensure_result_box()
    result_box.delete("1.0", tk.END)

    result_box.insert(
        tk.END,
        result,
        "center"
    )
    
    
# ==========================================
# PIERWSZE OKNO
# ==========================================    
def show_mixing_screen():
    
    clear_left_frame()
    ensure_result_box()
    
    # ==========================================
    # TYTUŁ
    # ==========================================
    tk.Label(
        left_frame,
        text="KALKULATOR HETEROSTRUKTUR III-V",
        bg="#cdd8f5",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    # ==========================================
    # PRESET
    # ==========================================
    tk.Label(
        left_frame,
        text="Preset",
        bg="#cdd8f5",
        font=("Arial", 11, "bold")
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
    cation_frame = tk.Frame(
        left_frame,
        bg="#cdd8f5"
    )

    cation_frame.pack(pady=10)

    tk.Label(
        cation_frame,
        text="KATIONY",
        bg="#cdd8f5",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        pady=5
    )

    ttk.Combobox(
        cation_frame,
        textvariable=cation1_var,
        values=[""] + cations,
        width=8,
        justify="center"
    ).grid(row=1, column=0, padx=5)

    ttk.Combobox(
        cation_frame,
        textvariable=cation2_var,
        values=[""] + cations,
        width=8,
        justify="center"
    ).grid(row=1, column=1, padx=5)

    ttk.Combobox(
        cation_frame,
        textvariable=cation3_var,
        values=[""] + cations,
        width=8,
        justify="center"
    ).grid(row=1, column=2, padx=5)

    ttk.Entry(
        cation_frame,
        textvariable=x1_var,
        width=8,
        justify="center"
    ).grid(row=2, column=0, padx=5, pady=5)

    ttk.Entry(
        cation_frame,
        textvariable=x2_var,
        width=8,
        justify="center"
    ).grid(row=2, column=1, padx=5, pady=5)

    ttk.Entry(
        cation_frame,
        textvariable=x3_var,
        width=8,
        justify="center"
    ).grid(row=2, column=2, padx=5, pady=5)

    # ==========================================
    # ANIONY
    # ==========================================
    anion_frame = tk.Frame(
        left_frame,
        bg="#cdd8f5"
    )

    anion_frame.pack(pady=10)

    tk.Label(
        anion_frame,
        text="ANIONY",
        bg="#cdd8f5",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        pady=5
    )

    ttk.Combobox(
        anion_frame,
        textvariable=anion1_var,
        values=[""] + anions,
        width=8,
        justify="center"
    ).grid(row=1, column=0, padx=5)

    ttk.Combobox(
        anion_frame,
        textvariable=anion2_var,
        values=[""] + anions,
        width=8,
        justify="center"
    ).grid(row=1, column=1, padx=5)

    ttk.Combobox(
        anion_frame,
        textvariable=anion3_var,
        values=[""] + anions,
        width=8,
        justify="center"
    ).grid(row=1, column=2, padx=5)

    ttk.Entry(
        anion_frame,
        textvariable=y1_var,
        width=8,
        justify="center"
    ).grid(row=2, column=0, padx=5, pady=5)

    ttk.Entry(
        anion_frame,
        textvariable=y2_var,
        width=8,
        justify="center"
    ).grid(row=2, column=1, padx=5, pady=5)

    ttk.Entry(
        anion_frame,
        textvariable=y3_var,
        width=8,
        justify="center"
    ).grid(row=2, column=2, padx=5, pady=5)

    # ==========================================
    # BUTTON
    # ==========================================
    tk.Button(
        left_frame,
        text="Next",
        command=next_window,
        font=("Arial", 12, "bold"),
        bg="#6d8edb",
        fg="white",
        activebackground="#5678c7",
        width=18,
        height=2,
        relief="flat"
    ).pack(pady=30)
    
    
# ==========================================
# DODAWANIE PODŁOŻA
# ==========================================  
def show_substrate_screen():

    clear_left_frame()

    tk.Label(
        left_frame,
        text="WYBÓR PODŁOŻA",
        font=("Arial",16,"bold"),
        bg="#cdd8f5"
    ).pack(pady=20)
    
    substrates = load_substrates()

    ttk.Combobox(
        left_frame,
        textvariable=substrate_var,
        values=substrates,
        width=20,
        justify="center"
    ).pack(pady=20)
    
    tk.Button(
        left_frame,
        text="Dalej",
        command=confirm_substrate,
        width=20,
        height=2
    ).pack(pady=20)
 
       
# ==========================================
# PRZYCISK POTWIERDZENIA
# ==========================================    
def confirm_substrate():

    if substrate_var.get() == "":

        tk.messagebox.showerror(
            "Błąd",
            "Wybierz podłoże"
        )

        return

    app_state.current_substrate = substrate_var.get()

    module = import_function("naprezenia")
    module.calculate_strain(database)
    
    show_operations_screen()
    
    ensure_result_box()
    result_box.delete("1.0", tk.END)

    result = ""
    
    # ======================================
    # PARAMETRY MATERIAŁU
    # ======================================
    result += "PARAMETRY MATERIAŁU\n"
    result += "====================================\n\n"
    
    result += f"Eg  = {app_state.mixed_material['Eg']:.4f} eV\n"
    result += f"VBO = {app_state.mixed_material['VBO']:.4f} eV\n"
    result += f"CBO = {app_state.mixed_material['CBO']:.4f} eV\n\n"
    
    result += f"a   = {app_state.mixed_material['a']:.4f} A\n"
    result += f"c11 = {app_state.mixed_material['c11']:.4f}\n"
    result += f"c12 = {app_state.mixed_material['c12']:.4f}\n\n"
    
    # ======================================
    # NAPRĘŻENIA
    # ======================================
    result += "NAPRĘŻENIA\n"
    result += "====================================\n\n"
    
    result += f"Podłoże = {app_state.current_substrate}\n\n"
    
    result += f"eps_xx = {app_state.strain['eps_xx']:.6e}\n"
    result += f"eps_yy = {app_state.strain['eps_yy']:.6e}\n"
    result += f"eps_zz = {app_state.strain['eps_zz']:.6e}\n\n"
    
    # ======================================
    # PASMA
    # ======================================
    result += "PASMA ENERGETYCZNE\n"
    result += "====================================\n\n"
    
    result += "Przed naprężeniem:\n"
    
    result += f"CB = {app_state.mixed_material['CBO']:.4f} eV\n"
    result += f"VB = {app_state.mixed_material['VBO']:.4f} eV\n"
    result += f"Eg = {app_state.mixed_material['Eg']:.4f} eV\n\n"
    
    result += "Po naprężeniu:\n"
    
    result += f"CB = {app_state.strained_bands['CB']:.4f} eV\n"
    result += f"HH = {app_state.strained_bands['HH']:.4f} eV\n"
    result += f"LH = {app_state.strained_bands['LH']:.4f} eV\n"
    
    result += f"Eg(HH) = {app_state.strained_bands['Eg_HH']:.4f} eV\n"
    result += f"Eg(LH) = {app_state.strained_bands['Eg_LH']:.4f} eV\n"
    
    result_box.insert(
        tk.END,
        result,
        "center"
    )

    
def load_substrates():

    return list(
        database["binary materials"].keys()
    )
    
    
# ==========================================
# OKNO OPERACJI
# ==========================================
def show_operations_screen():

    clear_left_frame()

    tk.Label(
        left_frame,
        text="OPERACJE NA MATERIALE",
        bg="#cdd8f5",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    material_name = ""
    
    for c in app_state.current_material["cations"]:
        material_name += (
            f"{c}"
            f"{app_state.current_material['fractions'][c]:.2f}"
        )
    
    for a in app_state.current_material["anions"]:
        material_name += a
    
    tk.Label(
        left_frame,
        text=material_name,
        bg="#cdd8f5",
        font=("Arial", 12, "bold")
    ).pack(pady=10)
    
    tk.Label(
        left_frame,
        text="PODŁOŻE",
        bg="#cdd8f5",
        font=("Arial", 10, "bold")
    ).pack(pady=(10, 0))
    
    tk.Label(
        left_frame,
        text=app_state.current_substrate,
        bg="#cdd8f5",
        font=("Arial", 12)
    ).pack(pady=(0, 10))
        
    # NOWY PRZYCISK: GENEROWANIE WYKRESU PASM
    tk.Button(
        left_frame,
        text="Pokaż wykres pasm",
        command=draw_band_energy,
        width=40,
        height=2
    ).pack(pady=10)

    tk.Button(
        left_frame,
        text="Pokaż wykres mas efektywnych w Z",
        command=draw_mass_dependency,
        width=40,
        height=2
    ).pack(pady=5)
    
    tk.Button(
        left_frame,
        text="Pokaż wykres mas efektywnych 111",
        command=draw_mass_dependency_111,
        width=40,
        height=2
    ).pack(pady=5)
    
    tk.Button(
        left_frame,
        text="Pokaż wykres mas efektywnych 110",
        command=draw_mass_dependency_110,
        width=40,
        height=2
    ).pack(pady=5)
    
    tk.Button(
        left_frame,
        text="Pokaż wykres oddziaływania S-O",
        command=draw_S_O,
        width=40,
        height=2
    ).pack(pady=5)
    
    tk.Button(
        left_frame,
        text="Grubość krytyczna",
        command=draw_critical_thickness,
        width=40,
        height=2
    ).pack(pady=5)
    
    tk.Button(
        left_frame,
        text="Studnia kwantowa",
        command=show_qw_form,
        width=25,
        height=2
    ).pack(pady=5)
    
    tk.Button(
        left_frame,
        text="← Wróć",
        command=show_mixing_screen,
        width=25,
        height=2
    ).pack(pady=20)
    
    
    
# ==========================================
# RYSOWANIE WYKRESU ENERGII PASM (Wspiera 2D i 3D)
# ==========================================
def draw_band_energy():
    clear_right_frame()
    
    if app_state.current_material is None:
        tk.messagebox.showerror("Błąd", "Brak wybranego materiału")
        return
        
    module = import_function("mieszanie")
    
    try:
        res = module.calculate_band_dependency(
            app_state.current_material,
            database
        )
    except Exception as e:
        traceback.print_exc()
        tk.messagebox.showerror("Błąd", f"Nie udało się obliczyć zależności pasm: {e}")
        return

    fig = Figure(figsize=(6, 5), dpi=100)
    from matplotlib.patches import Patch
    
    is_3d = res[0]
    
    if is_3d:
        # Obsługa renderowania powierzchni trójwymiarowej (3D)
        _, X, Y, Z_VBO, Z_CBO, xlabel, ylabel = res
        ax = fig.add_subplot(111, projection='3d')
        
        surf_cb = ax.plot_surface(X, Y, Z_CBO, cmap="Reds", alpha=0.75, edgecolor='none')
        surf_vb = ax.plot_surface(X, Y, Z_VBO, cmap="Blues", alpha=0.75, edgecolor='none')
        
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=9, fontweight='bold')
        ax.set_zlabel("Energia (eV)", fontsize=9, fontweight='bold')
        
        # Tworzenie sztucznej legendy dla powierzchni 3D przy użyciu obiektów Patch
        legend_elements = [
            Patch(facecolor='#d9534f', edgecolor='none', alpha=0.7, label='Pasmo przewodnictwa (CB)'),
            Patch(facecolor='#0275d8', edgecolor='none', alpha=0.7, label='Pasmo walencyjne (VB)')
        ]
        ax.legend(handles=legend_elements, loc="best")
    else:
        # Klasyczna obsługa wykresu liniowego (2D)
        _, x_steps, _, vbo_coords, cbo_coords, xlabel, _ = res
        ax = fig.add_subplot(111)
        
        ax.plot(x_steps, cbo_coords, label="Pasmo przewodnictwa (CB)", color="#d9534f", linewidth=2.5)
        ax.plot(x_steps, vbo_coords, label="Pasmo walencyjne (VB)", color="#0275d8", linewidth=2.5)
        
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel("Energia (eV)", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="best")
        
    ax.set_title("Zależność energii pasm od składu stopu", fontsize=12, fontweight='bold', pad=15)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    app_state.plot_canvas = canvas
    app_state.band_plot_figure = fig
        
# ==========================================
#  RYSOWANIE WYKRESU MAS EFEKTYWNYCH (2D i 3D)
# ==========================================
def draw_mass_dependency():
    clear_right_frame()
    
    if app_state.current_material is None:
        tk.messagebox.showerror("Błąd", "Brak wybranego materiału")
        return
        
    module = import_function("mieszanie")
    
    try:
        res = module.calculate_mass_dependency(
            app_state.current_material,
            database
        )
    except Exception as e:
        traceback.print_exc()
        tk.messagebox.showerror("Błąd", f"Nie udało się obliczyć zależności mas: {e}")
        return

    fig = Figure(figsize=(6, 5), dpi=100)
    from matplotlib.patches import Patch
    
    is_3d = res[0]
    
    if is_3d:
        # Obsługa renderowania powierzchni trójwymiarowej (3D) dla mas efektywnych
        _, X, Y, Z_me, Z_mhh, Z_mlh, xlabel, ylabel = res[0], res[1], res[2], res[3], res[4], res[5], res[10], res[11]
        ax = fig.add_subplot(111, projection='3d')
        
        surf_me = ax.plot_surface(X, Y, Z_me, cmap="Purples", alpha=0.75, edgecolor='none')
        surf_mhh = ax.plot_surface(X, Y, Z_mhh, cmap="Greens", alpha=0.75, edgecolor='none')
        surf_mlh = ax.plot_surface(X, Y, Z_mlh, cmap="Reds", alpha=0.75, edgecolor='none')
        
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=9, fontweight='bold')
        ax.set_zlabel("Masa efektywna (m0)", fontsize=9, fontweight='bold')
        
        # Tworzenie sztucznej legendy
        legend_elements = [
            Patch(facecolor='#8e44ad', edgecolor='none', alpha=0.7, label='Masa elektronu (m_e)'),
            Patch(facecolor='#27ae60', edgecolor='none', alpha=0.7, label='Masa ciężkiej dziury (m_hh)'),
            Patch(facecolor='#f31212', edgecolor='none', alpha=0.7, label='Masa lekkiej dziury (m_lh)')
        ]
        ax.legend(handles=legend_elements, loc="best")
    else:
        # Obsługa wykresu liniowego (2D) dla mas efektywnych
        _, x_steps, me_coords, mhh_coords, mlh_coords, xlabel, _ = res[0], res[1], res[2], res[3], res[4], res[9], res[10]
        ax = fig.add_subplot(111)
        
        ax.plot(x_steps, me_coords, label="m_e (elektron)", color="#8e44ad", linewidth=2.5)
        ax.plot(x_steps, mhh_coords, label="m_hh (ciężka dziura)", color="#27ae60", linewidth=2.5)
        ax.plot(x_steps, mlh_coords, label="m_lh (lekka dziura)", color="#f31230", linewidth=2.5)
        
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel("Masa efektywna (m0)", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="best")
        
    ax.set_title("Zależność mas efektywnych od składu", fontsize=12, fontweight='bold', pad=15)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    app_state.plot_canvas = canvas
    app_state.band_plot_figure = fig

# ==========================================
#  RYSOWANIE WYKRESU MAS EFEKTYWNYCH w kierunku 111 (2D i 3D)
# ==========================================
def draw_mass_dependency_111():
    clear_right_frame()
    
    if app_state.current_material is None:
        tk.messagebox.showerror("Błąd", "Brak wybranego materiału")
        return
        
    module = import_function("mieszanie")
    
    try:
        res = module.calculate_mass_dependency(
            app_state.current_material,
            database
        )
    except Exception as e:
        traceback.print_exc()
        tk.messagebox.showerror("Błąd", f"Nie udało się obliczyć zależności mas: {e}")
        return

    fig = Figure(figsize=(6, 5), dpi=100)
    from matplotlib.patches import Patch
    
    is_3d = res[0]
    
    if is_3d:
        # Obsługa renderowania powierzchni trójwymiarowej (3D) dla mas efektywnych
        _, X, Y, Z_me, Z_mhh111, Z_mlh111, xlabel, ylabel = res[0], res[1], res[2], res[3], res[8], res[9], res[10], res[11]
        ax = fig.add_subplot(111, projection='3d')
        
        surf_me = ax.plot_surface(X, Y, Z_me, cmap="Purples", alpha=0.75, edgecolor='none')
        surf_mhh111 = ax.plot_surface(X, Y, Z_mhh111, cmap="Greens", alpha=0.75, edgecolor='none')
        surf_mlh111 = ax.plot_surface(X, Y, Z_mlh111, cmap="Reds", alpha=0.75, edgecolor='none')
        
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=9, fontweight='bold')
        ax.set_zlabel("Masa efektywna (m0)", fontsize=9, fontweight='bold')
        
        # Tworzenie sztucznej legendy
        legend_elements = [
            Patch(facecolor='#8e44ad', edgecolor='none', alpha=0.7, label='Masa elektronu (m_e)'),
            Patch(facecolor='#27ae60', edgecolor='none', alpha=0.7, label='Masa ciężkiej dziury kierunku 111 (m_hh111)'),
            Patch(facecolor='#f31212', edgecolor='none', alpha=0.7, label='Masa lekkiej dziury kierunku 111 (m_lh111)')
        ]
        ax.legend(handles=legend_elements, loc="best")
    else:
        # Obsługa wykresu liniowego (2D) dla mas efektywnych
        _, x_steps, me_coords, mhh111_coords, mlh111_coords, xlabel, _ = res[0], res[1], res[2], res[5], res[6], res[9], res[10]
        ax = fig.add_subplot(111)
        
        ax.plot(x_steps, me_coords, label="m_e (elektron)", color="#8e44ad", linewidth=2.5)
        ax.plot(x_steps, mhh111_coords, label="m_hh111 (ciężka dziura)", color="#27ae60", linewidth=2.5)
        ax.plot(x_steps, mlh111_coords, label="m_lh111 (lekka dziura)", color="#f31230", linewidth=2.5)
        
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel("Masa efektywna (m0)", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="best")
        
    ax.set_title("Zależność mas efektywnych od składu", fontsize=12, fontweight='bold', pad=15)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    app_state.plot_canvas = canvas
    app_state.band_plot_figure = fig

# ==========================================
#  RYSOWANIE WYKRESU MAS EFEKTYWNYCH w kierunku 110 (2D i 3D)
# ==========================================
def draw_mass_dependency_110():
    clear_right_frame()
    
    if app_state.current_material is None:
        tk.messagebox.showerror("Błąd", "Brak wybranego materiału")
        return
        
    module = import_function("mieszanie")
    
    try:
        res = module.calculate_mass_dependency(
            app_state.current_material,
            database
        )
    except Exception as e:
        traceback.print_exc()
        tk.messagebox.showerror("Błąd", f"Nie udało się obliczyć zależności mas: {e}")
        return

    fig = Figure(figsize=(6, 5), dpi=100)
    from matplotlib.patches import Patch
    
    is_3d = res[0]
    
    if is_3d:
        # Obsługa renderowania powierzchni trójwymiarowej (3D) dla mas efektywnych
        _, X, Y, Z_me, Z_mhh110, Z_mlh110, xlabel, ylabel = res[0], res[1], res[2], res[3], res[6], res[7], res[10], res[11]
        ax = fig.add_subplot(111, projection='3d')
        
        surf_me = ax.plot_surface(X, Y, Z_me, cmap="Purples", alpha=0.75, edgecolor='none')
        surf_mhh110 = ax.plot_surface(X, Y, Z_mhh110, cmap="Greens", alpha=0.75, edgecolor='none')
        surf_mlh110 = ax.plot_surface(X, Y, Z_mlh110, cmap="Reds", alpha=0.75, edgecolor='none')
        
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=9, fontweight='bold')
        ax.set_zlabel("Masa efektywna (m0)", fontsize=9, fontweight='bold')
        
        # Tworzenie sztucznej legendy
        legend_elements = [
            Patch(facecolor='#8e44ad', edgecolor='none', alpha=0.7, label='Masa elektronu (m_e)'),
            Patch(facecolor='#27ae60', edgecolor='none', alpha=0.7, label='Masa ciężkiej dziury kierunku 110 (m_hh110)'),
            Patch(facecolor='#f31212', edgecolor='none', alpha=0.7, label='Masa lekkiej dziury kierunku 110 (m_lh110)')
        ]
        ax.legend(handles=legend_elements, loc="best")
    else:
        # Obsługa wykresu liniowego (2D) dla mas efektywnych
        _, x_steps, me_coords, mhh110_coords, mlh110_coords, xlabel, _ = res[0], res[1], res[2], res[7], res[8], res[9], res[10]
        ax = fig.add_subplot(111)
        ax = fig.add_subplot(111)
        
        ax.plot(x_steps, me_coords, label="m_e (elektron)", color="#8e44ad", linewidth=2.5)
        ax.plot(x_steps, mhh110_coords, label="m_hh110 (ciężka dziura)", color="#27ae60", linewidth=2.5)
        ax.plot(x_steps, mlh110_coords, label="m_lh110 (lekka dziura)", color="#f31212", linewidth=2.5)
        
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel("Masa efektywna (m0)", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="best")
        
    ax.set_title("Zależność mas efektywnych od składu", fontsize=12, fontweight='bold', pad=15)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    app_state.plot_canvas = canvas
    app_state.band_plot_figure = fig

# ==========================================
#  RYSOWANIE WYKRESU Spin Orbita (2D i 3D)
# ==========================================
def draw_S_O():
    clear_right_frame()
    
    if app_state.current_material is None:
        tk.messagebox.showerror("Błąd", "Brak wybranego materiału")
        return
        
    module = import_function("mieszanie")
    
    try:
        res = module.calculate_mass_dependency(
            app_state.current_material,
            database
        )
    except Exception as e:
        traceback.print_exc()
        tk.messagebox.showerror("Błąd", f"Nie udało się obliczyć zależności mas: {e}")
        return

    fig = Figure(figsize=(6, 5), dpi=100)
    from matplotlib.patches import Patch
    
    is_3d = res[0]
    
    if is_3d:
        # Obsługa renderowania powierzchni trójwymiarowej (3D) dla mas efektywnych
        _, X, Y, Z_so, xlabel, ylabel = res[0], res[1], res[2], res[12], res[10], res[11]
        ax = fig.add_subplot(111, projection='3d')
        
        surf_so = ax.plot_surface(X, Y, Z_so, cmap="Purples", alpha=0.75, edgecolor='none')
        
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=9, fontweight='bold')
        ax.set_zlabel("Oddziaływanie Spin-Orbital (so)", fontsize=9, fontweight='bold')
        
        # Tworzenie sztucznej legendy
        legend_elements = [
            Patch(facecolor='#8e44ad', edgecolor='none', alpha=0.7, label='Masa efektywna oddziaływania Spin-Orbital (so)'),
        ]
        ax.legend(handles=legend_elements, loc="best")
    else:
        # Obsługa wykresu liniowego (2D) dla mas efektywnych
        _, x_steps, so_coords, xlabel, _ = res[0], res[1], res[11], res[9], res[10]
        ax = fig.add_subplot(111)
        
        ax.plot(x_steps, so_coords, label="so (Spin-Orbital)", color="#8e44ad", linewidth=2.5)
        
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel("Oddziaływanie Spin-Orbital (so)", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(loc="best")
        
    ax.set_title("Zależność Spin-Orbital od składu", fontsize=12, fontweight='bold', pad=15)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    app_state.plot_canvas = canvas
    app_state.band_plot_figure = fig
    
# ==============================================================================
# UNIWERSALNE RYSOWANIE WYKRESU GRUBOŚCI KRYTYCZNEJ (AUTODETEKCJA 2D / 3D STRUKTURY)
# ==============================================================================
def draw_critical_thickness():
    clear_right_frame()
    
    # Pobranie wszystkich wpisanych kationów i anionów
    cat1 = cation1_var.get().strip()
    cat2 = cation2_var.get().strip()
    cat3 = cation3_var.get().strip()
    
    an1 = anion1_var.get().strip()
    an2 = anion2_var.get().strip()
    an3 = anion3_var.get().strip()
    
    sub = substrate_var.get().strip()
    
    if not sub:
        tk.messagebox.showerror("Błąd", "Wybierz podłoże (substrate) przed wykreśleniem.")
        return
        
    # Odfiltrowanie niepustych elementów
    cations_list = [c for c in [cat1, cat2, cat3] if c]
    anions_list = [a for a in [an1, an2, an3] if a]
    total_elements = len(cations_list) + len(anions_list)
    
    # Dynamiczny import modułu obliczeniowego
    module = import_function("krytyczna")
    fig = Figure(figsize=(7, 6), dpi=100)
    
    # --------------------------------------------------------------------------
    # PRZYPADEK 1: UKŁAD 3-ELEMENTOWY (WYKRES 2D)
    # --------------------------------------------------------------------------
    if total_elements == 3:
        try:
            x_vec, hc_vec, xlabel = module.get_ternary_2d_data(
                database, cations_list, anions_list, sub, FUNKCJE_PATH
            )
        except Exception as e:
            traceback.print_exc()
            tk.messagebox.showerror("Błąd", f"Nie udało się przeliczyć układu 3-elementowego: {e}")
            return
            
        ax = fig.add_subplot(111)
        ax.plot(x_vec, hc_vec, color='#1f77b4', linewidth=2.5, label='hc (Matthews-Blakeslee)')
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel("Grubość krytyczna hc [nm]", fontsize=9, fontweight='bold')
        
        # Generowanie ładnego opisu na podstawie wykrytych pierwiastków
        w_formula = "".join(cations_list) + "".join(anions_list)
        ax.set_title(f"Model Matthews-Blakeslee dla układu 3-elementowego\nStop: {w_formula} / Podłoże: {sub}", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_xlim(0, 1)
        
    # --------------------------------------------------------------------------
    # PRZYPADEK 2: UKŁAD 4-ELEMENTOWY (WYKRES 3D SURFACE Z MASKOWANIEM GIBBSA DLA 3+1/1+3 LUB PEŁNY DLA 2+2)
    # --------------------------------------------------------------------------
    elif total_elements == 4:
        try:
            # Pobranie danych (siatka X, Y oraz macierz grubości Z)
            X, Y, Z, xlabel, ylabel = module.get_quaternary_3d_data(
                database, cations_list, anions_list, sub, FUNKCJE_PATH
            )
        except Exception as e:
            traceback.print_exc()
            tk.messagebox.showerror("Błąd", f"Nie udało się wygenerować danych: {e}")
            return
            
        # Zmiana: Tworzymy zwykłą oś 2D zamiast osi z parametrem projection='3d'
        ax = fig.add_subplot(111)
        
        # Rysowanie dwuwymiarowej mapy cieplnej. 
        # pcolormesh świetnie radzi sobie z wartościami np.nan (pozostawia je przezroczyste/białe)
        im = ax.pcolormesh(X, Y, Z, cmap='viridis', shading='auto')
        
        # Dodanie paska skali kolorystycznej (colorbar) określającego grubość krytyczną
        cbar = fig.colorbar(im, ax=ax, shrink=0.9, aspect=15)
        cbar.set_label("Grubość krytyczna hc [nm]", fontsize=9, fontweight='bold')
        
        # Ustawienia etykiet osi (zostają dokładnie takie same)
        ax.set_xlabel(xlabel, fontsize=9, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=9, fontweight='bold')
        
        # Tytuł wykresu zmieniony na mapę cieplną
        ax.set_title(f"Mapa cieplna grubości krytycznej hc\nPodłoże: {sub}", fontsize=10, fontweight='bold', pad=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # Opcjonalnie: wymuszenie równej skali osi, jeśli zakresy x i y są identyczne (0 do 1)
        ax.set_aspect('equal', 'box')
        
    else:
        tk.messagebox.showerror("Błąd", f"Wykryto {total_elements} pierwiastków. Obsługiwane są wyłącznie układy 3 lub 4 elementowe.")
        return
        
    fig.tight_layout()

    # Odświeżenie i osadzenie widoku w oknie interfejsu Tkinter
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    app_state.plot_canvas = canvas
    app_state.band_plot_figure = fig
    
 # ==========================================
 # STUDNIA KWANTOWA
 # ==========================================   
 
def draw_quantum_well():

    app_state.well_width = abs(float(
        well_width_var.get()
    ))

    app_state.barrier_width = abs(float(
        barrier_width_var.get()
    ))

    module = import_function("studnia")

    x, y_cb, y_hh, y_lh = module.plot(database)

    clear_right_frame()

    fig = Figure(figsize=(7, 5), dpi=100)

    ax = fig.add_subplot(111)

    ax.plot(
        x,
        y_cb,
        linewidth=3,
        label="Pasmo przewodnictwa"
    )

    ax.plot(
        x,
        y_hh,
        "--",
        linewidth=3,
        label="Pasmo HH"
    )

    ax.plot(
        x,
        y_lh,
        linewidth=3,
        label="Pasmo LH"
    )

    ax.set_xlabel("Pozycja [nm]")
    ax.set_ylabel("Energia [eV]")

    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(
        fig,
        master=right_frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    app_state.plot_canvas = canvas
    
def show_qw_form():

    clear_left_frame()

    tk.Label(
        left_frame,
        text="STUDNIA KWANTOWA",
        bg="#cdd8f5",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        left_frame,
        text="Szerokość studni [nm]",
        bg="#cdd8f5"
    ).pack()

    tk.Entry(
        left_frame,
        textvariable=well_width_var
    ).pack(pady=5)

    tk.Label(
        left_frame,
        text="Szerokość bariery [nm]",
        bg="#cdd8f5"
    ).pack()

    tk.Entry(
        left_frame,
        textvariable=barrier_width_var
    ).pack(pady=5)

    tk.Button(
        left_frame,
        text="Rysuj",
        command=draw_quantum_well
    ).pack(pady=20)
    
    tk.Button(
        left_frame,
        text="← Wróć",
        command=show_mixing_screen,
        width=25,
        height=2
    ).pack(pady=20)
    

# ==========================================
# CZYSZCZENIE OKNA
# ==========================================
def clear_right_frame():

    for widget in right_frame.winfo_children():
        widget.destroy()
        
# ==========================================
# DANE
# ==========================================
cations = load_cations()

anions = load_anions()


# ==========================================
# OKNO
# ==========================================
root = tk.Tk()

root.title("Heterostruktury III-V")

root.geometry("1150x700")

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
    width=350
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

substrate_var = tk.StringVar()

well_width_var = tk.StringVar(value="4")
barrier_width_var = tk.StringVar(value="8")

cation1_var = tk.StringVar()
cation2_var = tk.StringVar()
cation3_var = tk.StringVar()

anion1_var = tk.StringVar()
anion2_var = tk.StringVar()
anion3_var = tk.StringVar()

x1_var = tk.StringVar(value="1.0")
x2_var = tk.StringVar(value="0.0")
x3_var = tk.StringVar(value="0.0")

y1_var = tk.StringVar(value="1.0")
y2_var = tk.StringVar(value="0.0")
y3_var = tk.StringVar(value="0.0")


# Initial creation of result box
result_box = None
ensure_result_box()

# ==========================================
# START
# ==========================================
show_mixing_screen()
root.mainloop()