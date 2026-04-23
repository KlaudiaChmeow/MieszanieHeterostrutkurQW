import matplotlib
import numpy

print("Hello World")

def mix_TernaryEg(Eg1, Eg2, bowing,n):
    f = open('output/test_ternary.dat', 'w')
    for x in range(n):
        output = str(x/n) + " " + str((x/n)*Eg1 + (1 - x/n)*Eg2 + (x/n)*(1-x/n)*bowing) + "\n"
        f.write(output)
        
def mix_QuaternaryEg1(Eg1, Eg2, Eg3, Eg4, n1, n2): # Binarka Mieszanie A z C i D i B z C i D, z reguły byśmy chcieli żeby n1 = n2 bo to nasz parametr jakości (ilość kroków)
    f = open('output/test_quaternary1.dat', 'w')
    for x in range(n1):
        for y in range(n2):
            output = str(x/n1) + " " + str (y/n2) + " " + str((x/n1)*(y/n2)*Eg1 + (x/n1)*(1-y/n2)*Eg2 + (1-x/n1)*(y/n2)*Eg3 + (1-x/n1)*(1-y/n2)*Eg4) + "\n"
            f.write(output)
            
def mix_QuaternaryEg2(Eg1, Eg2, Eg3, n1, n2): # Binarka Mieszanie A z D, B z D, C z D, z reguły byśmy chcieli żeby n1 = n2 bo to nasz parametr jakości (ilość kroków)
    f = open('output/test_quaternary2.dat', 'w')
    for x in range(n1):
        for y in range(n2):
            output = str(x/n1) + " " + str (y/n2) + " " + str((x/n1)*Eg1 + (y/n2)*Eg2 + (1 - (x/n1) - (y/n2))*Eg3) + "\n"
            f.write(output)
    
mix_TernaryEg(1.5, 1.3, 0.3, 5000)
mix_QuaternaryEg1(1.5, 1.3, 1.1, 0.1, 100, 100)
mix_QuaternaryEg2(1.5, 1.3, 0.1, 100, 100)

