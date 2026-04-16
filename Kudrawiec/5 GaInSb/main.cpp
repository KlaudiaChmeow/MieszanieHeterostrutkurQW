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
    double e = 0, d = 0, gora = 0, dol1 = 0, dol2 = 0;

    // Parametry materialowe dla GaSb i InSb
    double Eg_InSb = 0.17, Eg_GaSb = 0.726, bowing_Eg = 0.43;
    double VBO_InSb = -0.41, VBO_GaSb = -0.03, bowing_VBO = 0;
    double a_InSb = 6.4794;
    double a_GaSb = 6.0959;
    double In_c11 = 684.7, In_c12 = 373.2, Ga_c11 = 884, Ga_c12 = 402;
    double In_ac = -6.94, In_av = -0.36, Ga_ac = -7.5, Ga_av = -0.8;
    double In_b = -1.8, Ga_b = -2.0;

    ofstream plik("GaInSb_naprezenia3.txt");

    for (int i = 0; i <= 100; ++i)
    {
        double x = i / 100.0;

        double Eg = mix(x, Eg_InSb, Eg_GaSb, bowing_Eg);
        double VBO = mix(x, VBO_InSb, VBO_GaSb, bowing_VBO);
        double CBO = VBO + Eg;

        double Eg_mix = mix(x, Eg_InSb, Eg_GaSb, bowing_Eg);
        double VBO_mix = mix(x, VBO_InSb, VBO_GaSb, bowing_VBO);
        double delEg = Eg_GaSb - Eg_InSb;
        double delEv = VBO_GaSb - VBO_InSb;
        double delEc = delEg - delEv;
        double Qc = delEc / (delEc + delEv);
        double CBO_mix = Qc * Eg_mix;

        double ac = mix(x, In_ac, Ga_ac, 0);
        double av = mix(x, In_av, Ga_av, 0);
        double b = mix(x, In_b, Ga_b, 0);
        double a_InGaSb = (1 - x) * a_GaSb + x * a_InSb;

        double c11 = mix(x, In_c11, Ga_c11, 0);
        double c12 = mix(x, In_c12, Ga_c12, 0);

        double ex = (a_InSb - a_InGaSb) / a_InGaSb;
        double ez = -(2.0) * ex * (c12 / c11);

        double deltaEc = ac * (2 * ex + ez);
        double deltaEv = av * (2 * ex + ez);
        double deltaEs = b * (ex - ez);

        double Ec = CBO + deltaEc;
        double EHH = VBO + deltaEv + deltaEs;
        double ELH = VBO + deltaEv - deltaEs;

        if (x == 0.4)
        {
            gora = Ec;
            dol1 = EHH;
            dol2 = ELH;
        }

        plik << x << '\t'
             << EHH << '\t' << Ec << '\t' << ELH << '\t' << VBO << '\t' << CBO << endl;
    }
    plik.close();
    cout << "Dane zapisane do pliku GaInSb_strained_vs_unstrained.txt" << endl;

    ofstream zad5("5_GaInSb3.txt");

    double o = 0;
    while (o < 20)
    {
        if (o < 6 || o > 14)
        {
            zad5 << o << '\t' << VBO_GaSb + Eg_GaSb << '\t' << VBO_GaSb << '\t' << VBO_GaSb << endl;
        }
        else
        {
            zad5 << o << '\t' << gora << '\t' << dol1 << '\t' << dol2 << endl;
        }
        o = o + 0.2;
    }
    zad5.close();

    return 0;
}
