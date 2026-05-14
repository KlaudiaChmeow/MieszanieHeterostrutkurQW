#include <iostream>
#include <fstream>
#include <cmath>
#include <iomanip>

using namespace std;

double mix(double x, double A, double B, double bowing)
{
    return (1 - x) * B + x * A - x * (1 - x) * bowing;
}

int main()
{
    // Wartoœci dla GaInSb i InSb
    double Eg_InSb = 0.235, Eg_GaSb = 0.726, bowing_Eg = 0.378;
    double VBO_InSb = -0.54, VBO_GaSb = -0.76, bowing_VBO = -0.40;
    double a_InSb = 6.479, a_GaSb = 6.095;
    double In_c11 = 761.4, In_c12 = 249.6, Ga_c11 = 1155.6, Ga_c12 = 561.2;
    double In_ac = -5.13, In_av = -1.02, Ga_ac = -7.45,  Ga_av = -1.22;
    double In_b = -1.89, Ga_b = -2.04;

    ofstream plik("GaInSb_InSb_naprezenia.txt");

    for (int i = 0; i <= 100; ++i)
    {
        double x = i / 100.0;

        // Obliczanie energii pasma dla GaInSb
        double Eg = mix(x, Eg_InSb, Eg_GaSb, bowing_Eg);
        double VBO = mix(x, VBO_InSb, VBO_GaSb, bowing_VBO);
        double CBO = VBO + Eg;

        // Parametry mieszane
        double Eg_mix = mix(x, Eg_InSb, Eg_GaSb, bowing_Eg);
        double VBO_mix = mix(x, VBO_InSb, VBO_GaSb, bowing_VBO);
        double delEg = Eg_GaSb - Eg_InSb;
        double delEv = VBO_GaSb - VBO_InSb;
        double delEc = delEg - delEv;
        double Qc = delEc / (delEc + delEv);
        double CBO_mix = Qc * Eg_mix;

        // Parametry strukturalne
        double ac = mix(x, In_ac, Ga_ac, 2.61);
        double av = mix(x, In_av, Ga_av, 0);
        double b = mix(x, In_b, Ga_b, 0);
        double a_InGaSb = (1 - x) * a_GaSb + x * a_InSb;

        double c11 = mix(x, In_c11, Ga_c11, 0);
        double c12 = mix(x, In_c12, Ga_c12, 0);

        // Obliczenia zwi¹zane z naprê¿eniami
        double ex = (a_GaSb - a_InGaSb) / a_InGaSb;
        double ez = -(2.0) * ex * (c12/c11);

        double deltaEc = ac * (2 * ex + ez);
        double deltaEv = av * (2 * ex + ez);
        double deltaEs = b * (ex - ez);

        // Obliczanie energii pasm
        double Ec = CBO + deltaEc;
        double EHH = VBO + deltaEv + deltaEs;
        double ELH = VBO + deltaEv - deltaEs;

        // Zapis do pliku
        plik << x << '\t'
             << EHH <<'\t'<< Ec <<'\t'<< ELH <<'\t'<< VBO <<'\t'<< CBO <<'\t'<< CBO_mix
             << endl;
    }

    plik.close();
    cout << "Dane zapisane do pliku GaInSb_InSb_naprezenia.txt" << endl;
    return 0;
}
