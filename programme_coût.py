# fonction pour le cout en euros 
# barres en metres 
import matplotlib.pyplot as plt 
def Cout(barres,stylos,moteurtiges):
    cout_total=35*moteurtiges+moteurtiges*0.10+ 2*stylos + barres*5
    return cout_total

moteurs=[1,2,3,4,5]
barres=[1,2,3,4,5]
cout_total=[]
for i in range(len(moteurs)) :
    cout=Cout(barres[i],4,moteurs[i])
    cout_total.append(cout)
plt.plot(moteurs,cout_total)
plt.xlabel("Nombre de moteurs")
plt.xlabel("Cout en Euros")
plt.title("Cout en fonction des moteurs")
plt.grid() 
plt.show()