# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1

@author: miaudia
"""

import app_state
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plot(database):

    # ======================================
    # PARAMETRY
    # ======================================

    well_width = app_state.well_width
    barrier_width = app_state.barrier_width

    substrate_name = app_state.current_substrate

    substrate = database["binary materials"][substrate_name]
    
    print("START STUDNIA")
    print(substrate)

    # ======================================
    # STUDNIA
    # ======================================

    CB_well = app_state.strained_bands["CB"]

    HH_well = app_state.strained_bands["HH"]

    LH_well = app_state.strained_bands["LH"]
    
    print("CB_well =", CB_well)
    print("HH_well =", HH_well)
    print("LH_well =", LH_well)

    # ======================================
    # BARIERA
    # ======================================

    CB_barrier = substrate["VBO"] + substrate["Eg"]

    VB_barrier = substrate["VBO"]

    # ======================================
    # POZYCJA
    # ======================================

    x1 = barrier_width
    x2 = barrier_width + well_width
    xmax = 2 * barrier_width + well_width

    x = [
        0,
        x1,
        x1,
        x2,
        x2,
        xmax
    ]

    # ======================================
    # PASMO PRZEWODNICTWA
    # ======================================

    y_cb = [
        CB_barrier,
        CB_barrier,
        CB_well,
        CB_well,
        CB_barrier,
        CB_barrier
    ]

    # ======================================
    # HH
    # ======================================

    y_hh = [
        VB_barrier,
        VB_barrier,
        HH_well,
        HH_well,
        VB_barrier,
        VB_barrier
    ]

    # ======================================
    # LH
    # ======================================

    y_lh = [
        VB_barrier,
        VB_barrier,
        LH_well,
        LH_well,
        VB_barrier,
        VB_barrier
    ]

    
    return x, y_cb, y_hh, y_lh