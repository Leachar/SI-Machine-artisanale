import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from lebonaimport import analyser_fourier
from trace_energie_cinetique import trace_tps_energie
from precision_main import compute_precision
from programme_coût import Cout
from Energie_totale_finale import *
import math
# Coût et énergie de référence FIXES (ex: valeur max possible dans ton cahier des charges)
COUT_REF = 1000  # En euros (coût max toléré ou coût de 50 moteurs)
ENERGIE_REF = 15 # En Joules
n_moteur_max = int(input("Choississez le nombre maximal de moteurs "))
filename = input("Choisissez un fichier à exploiter entre engrenagestest.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))
n_moteur=list(range(1, n_moteur_max + 1))
energytot=[]
precisiontot=[]
cout_total=[]
opti=[]
for i in range(len(n_moteur)):
   
    x0, y0, moteurs, barres, phi, teta = analyser_fourier(
        filename=filename, 
        n_circles=n_moteur[i], 
        exporter_txt=False, 
        animer=False 
    )
    m_barre = calculer_masses_barres(barres, masse_lineique=0.05)
    
    energie = trace_tps_energie(barres, teta, phi)


    energytot.append(energie)
    precision = compute_precision(x0, y0, barres, teta, phi, selection, periode=0.10, display_plot=False)
    precisiontot.append(precision)
    cout=Cout(sum(barres[:i +1]),4,n_moteur[i])
    cout_total.append(cout)
    # 1. Normalisation
    

    # La normalisation ne dépend plus de la taille du tableau testé
    C_norm = cout / COUT_REF
    E_norm = energie / ENERGIE_REF

    # La formule conserve la même échelle peu importe n_moteur_max
    optic = (precision**5) / np.exp((C_norm**2) + E_norm)
    #opticalc=(((precision)/(0.77))**5)/math.exp((cout/800)**2+(energie/10))
    opti.append(optic)

plt.plot(n_moteur,opti,color="Blue")
# plt.plot(n_moteur,energytot,label="Energie",color="green")
# plt.plot(n_moteur,cout_total,label="Cout en euros",color="red")
# plt.xlabel("Nombre de moteurs")
plt.ylabel("Valeurs")
plt.title("test")

plt.grid()
plt.show()