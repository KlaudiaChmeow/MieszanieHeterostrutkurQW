#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

// Funkcja obliczaj¹ca przerwê energetyczn¹ dla materia³u GaInSb
// Model: Eg(x, T) = Eg_0(x) - alpha(x) * T^2 / (T + beta(x))

double Eg_Gamma(double x, double T) {
    double Eg0 = 0.726 * (1 - x) + 0.17 * x - 0.477 * x * (1 - x);  // Empiryczna zale¿noœæ dla GaInSb
    double alpha = 0.417 * (1 - x) + 0.267 * x;
    double beta = 140 * (1 - x) + 93 * x;
    return Eg0 - alpha * T * T / (T + beta);
}

double Eg_X(double x, double T) {
    double Eg0 = 1.16 * (1 - x) + 1.12 * x;
    double alpha = 0.45 * (1 - x) + 0.3 * x;
    double beta = 150 * (1 - x) + 100 * x;
    return Eg0 - alpha * T * T / (T + beta);
}

double Eg_L(double x, double T) {
    double Eg0 = 0.91 * (1 - x) + 0.6 * x;
    double alpha = 0.38 * (1 - x) + 0.26 * x;
    double beta = 130 * (1 - x) + 90 * x;
    return Eg0 - alpha * T * T / (T + beta);
}

int main() {
    std::ofstream file("energy_gap_data_GaInSb.txt");
    if (!file) {
        std::cerr << "B³¹d otwarcia pliku!" << std::endl;
        return 1;
    }

    std::vector<double> temperatures = {0, 10, 300, 600};
    file << "x T Eg_Gamma Eg_X Eg_L" << std::endl;

    for (double x = 0.0; x <= 1.0; x += 0.05) {
        for (double T : temperatures) {
            double EgG = Eg_Gamma(x, T);
            double EgX = Eg_X(x, T);
            double EgL = Eg_L(x, T);
            file << x << " " << T << " " << EgG << " " << EgX << " " << EgL << std::endl;
        }
    }

    file.close();
    std::cout << "Dane zapisano do pliku energy_gap_data_GaInSb.txt" << std::endl;
    return 0;
}
