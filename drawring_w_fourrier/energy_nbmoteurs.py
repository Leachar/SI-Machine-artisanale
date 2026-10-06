import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from matplotlib.patches import Rectangle
from lebonaimport import analyser_fourier
from Energie_totale_finale import *


n_moteur_max = int(input("Choississez le nombre maximal de moteurs "))
filename = input("Choisissez un fichier à exploiter entre engrenages.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))
n_moteur=list(range(1, n_moteur_max + 1))
energytot=[]


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


plt.plot(n_moteur,energytot)
plt.xlabel("Nombre de moteurs")
plt.ylabel("Energie")
plt.title("Energie en fonction des moteurs")
plt.grid()
plt.show()



