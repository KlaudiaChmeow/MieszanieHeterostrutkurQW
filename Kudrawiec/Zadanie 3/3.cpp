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
    double Eg_InAs = 0.417, Eg_GaAs = 1.519, bowing_Eg = 0.477;
    double VBO_InAs = -0.59, VBO_GaAs = -0.80, bowing_VBO = -0.38;
    double a_InAs = 6.0583, a_GaAs = 5.6533;
    double In_c11 = 832.9, In_c12 =452.6, Ga_c11 = 1221, Ga_c12 = 566;
    double In_ac = -5.08, In_av = -1.00, Ga_ac = -7.17,  Ga_av = -1.16;
    double In_b = -1.8, Ga_b = -2.0;

    ofstream plik("InAsGa_naprezenia.txt");

    for (int i = 0; i <= 100; ++i)
    {
        double x = i / 100.0;

        double Eg = mix(x, Eg_InAs, Eg_GaAs, bowing_Eg);
        double VBO = mix(x, VBO_InAs, VBO_GaAs, bowing_VBO);
        double CBO = VBO + Eg;

        double Eg_mix = mix(x, Eg_InAs, Eg_GaAs, bowing_Eg);
        double VBO_mix = mix(x, VBO_InAs, VBO_GaAs, bowing_VBO);
        double delEg = Eg_GaAs - Eg_InAs;
        double delEv = VBO_GaAs - VBO_InAs;
        double delEc = delEg - delEv;
        double Qc = delEc / (delEc + delEv);
        double CBO_mix = Qc * Eg_mix;

        double ac = mix(x, In_ac, Ga_ac, 2.61);
        double av = mix(x, In_av, Ga_av, 0);
        double b = mix(x, In_b, Ga_b, 0);
        double a_InGaAs = (1 - x) * a_GaAs + x * a_InAs;

        double c11 = mix(x,In_c11, Ga_c11,0);
        double c12 = mix(x,In_c12, Ga_c12,0);

        double ex = (a_GaAs - a_InGaAs) / a_InGaAs;
        double ez = -(2.0) * ex * (c12/c11);


        double deltaEc = ac * (2 * ex + ez);
        double deltaEv = av * (2 * ex + ez);
        double deltaEs = b * (ex - ez);


        double Ec = CBO + deltaEc;
        double EHH = VBO + deltaEv + deltaEs;
        double ELH = VBO + deltaEv - deltaEs;

        plik << x << '\t'
             << EHH <<'\t'<< Ec <<'\t'<< ELH <<'\t'<< VBO <<'\t'<< CBO <<'\t'<< CBO_mix
             << endl;
    }

    plik.close();
    cout << "Dane zapisane do pliku InGaAs_strained_vs_unstrained.txt" << endl;
    return 0;
}
