# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:16:14 2026

@author: miaudia
"""

import os
import json
import importlib.util
import tkinter as tk
from tkinter import ttk

# =========================
# ŚCIEŻKI
# =========================
MATERIALY_PATH = "materialy.json"
FUNKCJE_PATH = "./funkcje"

# =========================
# ŁADOWANIE MATERIAŁÓW
# =========================
def load_materials():
    try:
        with open(MATERIALY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return list(data.keys())

    except Exception as e:
        print("Błąd materialy.json:", e)
        return []


# =========================
# ŁADOWANIE FUNKCJI
# =========================
def load_functions():
    funcs = []

    try:
        for file in os.listdir(FUNKCJE_PATH):
            if file.endswith(".py"):
                funcs.append(file[:-3])

    except Exception as e:
        print("Błąd folderu funkcji:", e)

    return funcs


# =========================
# IMPORT FUNKCJI
# =========================
def import_function(module_name):

    path = os.path.join(FUNKCJE_PATH, module_name + ".py")

    spec = importlib.util.spec_from_file_location(module_name, path)

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


# =========================
# OBLICZENIA
# =========================
def calculate():

    mat1 = material1_var.get()
    mat2 = material2_var.get()
    mat3 = material3_var.get()
    mat4 = material4_var.get()

    func_name = function_var.get()

    try:
        module = import_function(func_name)

        if hasattr(module, "calculate"):

            result = module.calculate(mat1, mat2, mat3, mat4)

            result_label.config(text=f"Wynik: {result}")

        else:
            result_label.config(text="Brak calculate()")

    except Exception as e:
        result_label.config(text=f"Błąd: {e}")


# =========================
# DANE
# =========================
materials = load_materials()
functions = load_functions()

# =========================
# OKNO
# =========================
root = tk.Tk()

root.title("Miszanie Heterostruktur")
root.geometry("700x900")

root.configure(bg="#93a9db")

# =========================
# DROPDOWNY
# =========================
material1_var = tk.StringVar()
material2_var = tk.StringVar()
material3_var = tk.StringVar()
material4_var = tk.StringVar()
function_var = tk.StringVar()

ttk.Label(root, text="Materiał 1").pack(pady=5)
dropdown1 = ttk.Combobox(root, textvariable=material1_var, values=materials)
dropdown1.pack()

ttk.Label(root, text="Materiał 2").pack(pady=5)
dropdown2 = ttk.Combobox(root, textvariable=material2_var, values=materials)
dropdown2.pack()

ttk.Label(root, text="Materiał 3").pack(pady=5)
dropdown3 = ttk.Combobox(root, textvariable=material3_var, values=materials)
dropdown3.pack()

ttk.Label(root, text="Materiał 4").pack(pady=5)
dropdown4 = ttk.Combobox(root, textvariable=material4_var, values=materials)
dropdown4.pack()

ttk.Label(root, text="Funkcja").pack(pady=15)
function_dropdown = ttk.Combobox(root, textvariable=function_var, values=functions)
function_dropdown.pack()

# =========================
# PRZYCISK
# =========================
button = ttk.Button(root, text="Oblicz", command=calculate)
button.pack(pady=30)

# =========================
# WYNIK
# =========================
result_label = ttk.Label(root, text="Wynik:")
result_label.pack(pady=20)

# =========================
# START
# =========================
root.mainloop()