import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from precision_main import compute_precision
from lebonaimport import analyser_fourier


n_moteur_max = int(input("Choississez le nombre maximal de moteurs "))
filename = input("Choisissez un fichier à exploiter entre engrenages.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))
n_moteur=list(range(1, n_moteur_max + 1))
precisiontot=[]
for i in range(len(n_moteur)):
   
    x0, y0, moteurs, barres, phi, teta = analyser_fourier(
        filename=filename, 
        n_circles=n_moteur[i], 
        exporter_txt=False, 
        animer=False 
    )
    precision = compute_precision(x0, y0, barres, teta, phi, selection, periode=0.10, display_plot=False)
    precisiontot.append(precision)
plt.plot(n_moteur,precisiontot)
plt.xlabel("Nombre de moteurs")
plt.ylabel("Precision")
plt.title("Precision en fonction des moteurs")
plt.grid()
plt.show()



