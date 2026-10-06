# Main
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from precision_main import compute_precision
from lebonaimport import analyser_fourier
from programme_coût import tracer_cout_moteur
from programme_coût import Cout

n_moteur = int(input("Combien de moteurs voulez-vous tester ? "))
filename = input("Choisissez un fichier à exploiter entre engrenagestest.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))

x0, y0, moteurs, barres, phi, teta = analyser_fourier(filename=filename, n_circles=n_moteur, exporter_txt=True, animer=True)

# Demande à l'utilisateur quel graphique afficher
choix = input("Quel graphique voulez-vous afficher ? (1: Précision, 2: Coût, 3: Les deux) : ").strip()

if choix in ["1", "3"]:
    precision = compute_precision(x0, y0, barres, teta, phi, selection, periode=0.1, display_plot=True)
    plt.show()

if choix in ["2", "3"]:
    tracecout = tracer_cout_moteur(moteurs, barres)
    plt.show()



# cout_total=[]
# for i in range(len(moteurs)) :
#     cout=Cout(barres[i],4,moteurs[i])
#     cout_total.append(cout)
# plt.plot(moteurs,cout_total)
# plt.xlabel("Nombre de moteurs")
# plt.xlabel("Cout en Euros")
# plt.title("Cout en fonction des moteurs")
# plt.grid() 
