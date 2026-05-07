import matplotlib
import numpy

print("Hello World")

def mix_TernaryEg(Eg1, Eg2, bowing,n): #Wzór A.4
    return (x/n)*Eg1 + (1 - x/n)*Eg2 + (x/n)*(1-x/n)*bowing
        
def mix_QuaternaryEg1(Eg1, Eg2, Eg3, Eg4, n1, n2): # Binarka Mieszanie A z C i D oraz B z C i D, # Wzór A.6
    return (x/n1)*(y/n2)*Eg1 + (x/n1)*(1-y/n2)*Eg2 + (1-x/n1)*(y/n2)*Eg3 + (1-x/n1)*(1-y/n2)*Eg4
            
def mix_QuaternaryEg2(Eg1, Eg2, Eg3, n1, n2): # Binarka Mieszanie A z D, B z D, C z D, Zależą wg wzoru A.8
    return (x/n1)*Eg1 + (y/n2)*Eg2 + (1 - (x/n1) - (y/n2))*Eg3
    
def mix_QuaternaryEg3(Eg1, Eg2, Eg3, x, y): # Trójnarka Mieszanie AB z D, CB z D, AC z D,Wzór A.10 (Uwaga mieszanki muszą być faktycznymi mieszankami gdzie zmieniają parametry w zależności ile ich jest)
    return ((x*y*Eg1)+(y*(1-x-y)*Eg2)+(x*(1-x-y)*Eg3))/((x*y)+(y*(1-x-y))+(x*(1-x-y)))
    
def mix_QuaternaryEg4(Eg1, Eg2, Eg3, Eg4, x, y): # Trójnarka Mieszanie AB z C, AB z D, CD z A, CD z B, ABC ABD CDA CDB Zależą wg wzoru A.9
    return (((x*(1-x))*((y*Eg1)+((1-y)*Eg2)))+((y*(1-y))*((x*Eg3)+((1-x)*Eg4))))/((x*(1-x))+(y*(1-y)))
    
