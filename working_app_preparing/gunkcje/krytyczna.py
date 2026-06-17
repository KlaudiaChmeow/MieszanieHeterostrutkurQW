import numpy as np
import scipy
import app_state

def lattice_mismatch(a_layer, a_substrate):
    """
    f = (a_layer - a_substrate) / a_substrate
    """
    return (a_layer - a_substrate) / a_substrate

def critical_thickness_MB(f, b, nu=0.31, alpha=np.pi/4):
    """
    Matthews-Blakeslee critical thickness.
    Zwraca hc w [nm].
    """
    # Zabezpieczenie przed brakiem niedopasowania - grubość nieskończona
    if abs(f) < 1e-7:
        return float('inf')

    def equation(h):
        return (
            h
            - (b / (8 * np.pi * abs(f) * (1 + nu)))
            * ((1 - nu * np.cos(alpha)**2) / np.cos(alpha))
            * np.log(h / b)
        )

    h0 = 1e-8  # initial guess [m]

    try:
        hc = scipy.optimize.fsolve(equation, h0)[0]
        return hc * 1e9  # nm
    except Exception:
        return np.nan

def get_plot_data(database):
    """
    Funkcja pobierająca dane dla aktualnego materiału z app_state.
    Wyrzuca tablice z danymi potrzebne do wygenerowania wykresu w main.py.
    """
    if getattr(app_state, 'mixed_material', None) is None or getattr(app_state, 'current_substrate', None) is None:
        raise ValueError("Brak wymaganego materiału lub podłoża w app_state.")

    # Stałe sieci z aktualnie obliczonego stanu
    a_layer = app_state.mixed_material["a"]
    substrate_name = app_state.current_substrate
    a_sub = database["binary materials"][substrate_name]["a"]

    # Rzeczywiste niedopasowanie
    f_current = lattice_mismatch(a_layer, a_sub)

    # Wektor Burgersa
    b_current = (a_layer * 1e-10) / np.sqrt(2)

    # Aktualna grubość krytyczna
    hc_current = critical_thickness_MB(f_current, b_current)

    # Generowanie osi X (różne warianty niedopasowania f)
    # Skalujemy wykres względem wartości f_current, aby czerwony punkt zawsze się zmieścił
    f_max = max(0.03, abs(f_current) * 1.2) if abs(f_current) > 0.001 else 0.03
    f_values = np.linspace(0.0001, f_max, 200)
    
    # Generowanie osi Y (grubości krytyczne dla różnych f)
    hc_values = []
    for fv in f_values:
        hc_tmp = critical_thickness_MB(fv, b_current)
        hc_values.append(hc_tmp)

    return f_values, hc_values, abs(f_current), hc_current