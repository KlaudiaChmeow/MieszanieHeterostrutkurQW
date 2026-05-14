#include <iostream>
#include <fstream>
#include <cmath>
#include <iomanip>

using namespace std;

int main()
{
    double x, y, krok=0.1;
    ofstream file("x1.txt");

    for(double x = 0.0; x <= 1.0; x += krok)
    {
        #dla Eg
        y = (1.0 - x)* 0.812 + x * 0.235 - x * (1.0 - x) * 0.415;

        #dla VBO:
        #y = (1.0 - x)* (0.0) + x * (-0.03) - x * (1.0 - x) * 0.1;

        file << x << "\t" << y << "\n";
    }
    file.close();
    return 0;
}
