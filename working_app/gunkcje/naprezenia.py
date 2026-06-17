# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 19:11:02 2026

@author: miaudia
"""

import app_state


def calculate_strain(database):

    material = app_state.mixed_material

    substrate_name = app_state.current_substrate

    substrate = database["binary materials"][substrate_name]

    # ======================================
    # PARAMETRY MATERIAŁU
    # ======================================

    a_layer = material["a"]
    a_sub = substrate["a"]

    c11 = material["c11"]
    c12 = material["c12"]

    ac = material["ac"]
    av = material["av"]
    b = material["b"]

    CB0 = material["CBO"]
    VB0 = material["VBO"]

    # ======================================
    # ODKSZTAŁCENIA
    # ======================================
    eps_xx = (a_sub - a_layer) / a_layer
    
    eps_yy = eps_xx

    eps_zz = -2 * (c12 / c11) * eps_xx

    # ======================================
    # HYDROSTATIC STRAIN
    # ======================================

    eps_h = eps_xx + eps_yy + eps_zz

    # ======================================
    # BIAxIAL STRAIN
    # ======================================

    eps_b = eps_xx + eps_yy - 2 * eps_zz

    # ======================================
    # PRZESUNIĘCIA PASM
    # ======================================

    dEc = ac * eps_h

    dEhh = (
        av * eps_h
        - 0.5 * b * eps_b
    )

    dElh = (
        av * eps_h
        + 0.5 * b * eps_b
    )

    # ======================================
    # PASMA PO ODKSZTAŁCENIU
    # ======================================

    CB = CB0 + dEc

    HH = VB0 + dEhh

    LH = VB0 + dElh

    Eg_HH = CB - HH

    Eg_LH = CB - LH

    # ======================================
    # ZAPIS DO APP_STATE
    # ======================================

    app_state.strain = {

        "eps_xx": eps_xx,
        "eps_yy": eps_yy,
        "eps_zz": eps_zz,

        "eps_h": eps_h,
        "eps_b": eps_b,

        "dEc": dEc,
        "dEhh": dEhh,
        "dElh": dElh
    }

    app_state.strained_bands = {

        "CB": CB,
        "HH": HH,
        "LH": LH,

        "Eg_HH": Eg_HH,
        "Eg_LH": Eg_LH
    }

    return app_state.strain