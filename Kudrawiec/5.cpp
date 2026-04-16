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

    double e = 0, d =0, gora = 0, dol1 = 0, dol2 = 0;
    double Eg_InAs = 0.17, Eg_GaAs = 0.726, bowing_Eg = 0.43;
    double VBO_InAs = -0.41, VBO_GaAs = -0.03, bowing_VBO = 0;
    double a_InAs = 6.4794+2.79*pow(10,(-5))*(300);
    double a_GaAs = 6.0959+2.92*pow(10,(-5))*300;
    double In_c11 = 1011, In_c12 =561, Ga_c11 = 1405, Ga_c12 = 620.3;
    double In_ac = -6.94, In_av = -0.36, Ga_ac = -7.5,  Ga_av = -0.8;
    double In_b = -1.8, Ga_b = -2.0;

    ofstream plik("GaInP_naprezenia2.txt");

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

        double ac = mix(x, In_ac, Ga_ac, 0);
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

        if(x == 0.8)
        {
            gora = Ec;
            dol1 = EHH;
            dol2 = ELH;
        }

        plik << x << '\t'
             << EHH <<'\t'<< Ec <<'\t'<< ELH <<'\t'<< VBO <<'\t'<< CBO << endl;
    }
    plik.close();
    cout << "Dane zapisane do pliku InGaAs_strained_vs_unstrained.txt" << endl;

    ofstream zad5("5.2.txt");

    double o = 0;
    while(o < 20)
    {
        if(o < 8 || o > 12)
        {
            zad5 << o << '\t' << VBO_GaAs+Eg_GaAs <<'\t'<< VBO_GaAs << '\t' << VBO_GaAs <<endl;
        }
        else
        {
            zad5 << o << '\t' << gora <<'\t'<< dol1 << '\t' << dol2 <<endl;
        }
        o = o + 0.2;
    }
    zad5.close();

    return 0;
}
