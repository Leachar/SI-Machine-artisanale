# fonction pour le cout en euros 
# barres en metres 
import matplotlib.pyplot as plt 
def Cout(barres,stylos,moteurtiges):
    cout_total=35*moteurtiges+moteurtiges*0.10+ 2*stylos + barres*5
    return cout_total

def tracer_cout_moteur(moteurs,barres):
    liste_moteurs = list(range(1, moteurs + 1))
    cout_total=[]
    for i in range(len(liste_moteurs)) :
        cout=Cout(sum(barres[:i +1]),4,liste_moteurs[i])
        cout_total.append(cout)
    plt.plot(liste_moteurs,cout_total)
    plt.xlabel("Nombre de moteurs")
    plt.ylabel("Cout en Euros")
    plt.title("Cout en fonction des moteurs")
    plt.grid()
    plt.show()
# moteurs=[1,2,3,4,5]
# barres=[1,2,3,4,5]
# cout_total=[]
# for i in range(len(moteurs)) :
#     cout=Cout(barres[i],4,moteurs[i])
#     cout_total.append(cout)
# plt.plot(moteurs,cout_total)
# plt.xlabel("Nombre de moteurs")
# plt.xlabel("Cout en Euros")
# plt.title("Cout en fonction des moteurs")
# plt.grid() 
# plt.show()