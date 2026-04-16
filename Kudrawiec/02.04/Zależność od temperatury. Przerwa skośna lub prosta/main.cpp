#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>

// Funkcja obliczająca energię wierzchołków pasm w zależności od składu i temperatury
double calculate_band_energy(double composition, double temperature) {
    // Przybliżony model zależności energetycznej (do zastąpienia rzeczywistym modelem)
    const double Eg_GaSb = 0.812 - (0.0004 * temperature); // Eg dla GaSb w eV
    const double Eg_InSb = 0.235 - (0.0003 * temperature); // Eg dla InSb w eV
    const double bowing = 0.415; // Współczynnik ugięcia

    return (1 - composition) * Eg_GaSb + composition * Eg_InSb - bowing * composition * (1 - composition);
}

// Funkcja generująca dane dla danej temperatury i zapisująca do pliku
void generate_data(double temperature) {
    if (temperature < 0) {
        std::cerr << "Temperatura nie może być ujemna: " << temperature << "K" << std::endl;
        return;
    }

    std::string filename = "band_energy_T" + std::to_string((int)temperature) + "K.dat";
    std::ofstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Nie można otworzyć pliku: " << filename << std::endl;
        return;
    }

    file << "# Skład (x)   Energia pasma (eV)\n";
    file << std::fixed << std::setprecision(6);

    for (double x = 0.0; x <= 1.0; x += 0.05) {
        double energy = calculate_band_energy(x, temperature);
        file << x << " " << energy << "\n";
    }

    file.close();
    if (file.fail()) {
        std::cerr << "Błąd zapisu do pliku: " << filename << std::endl;
    } else {
        std::cout << "Dane zapisane w: " << filename << std::endl;
    }
}

int main() {
    const std::vector<double> temperatures = {0, 10, 300, 600};

    for (double T : temperatures) {
        generate_data(T);
    }

    return 0;
}
