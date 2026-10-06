import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from lebonaimport import analyser_fourier
from trace_energie_cinetique import trace_tps_energie
from precision_main import compute_precision
from programme_coût import Cout
from Energie_totale_finale import *

n_moteur_max = int(input("Choississez le nombre maximal de moteurs "))
filename = input("Choisissez un fichier à exploiter entre engrenages.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))
n_moteur=list(range(1, n_moteur_max + 1))
energytot=[]
precisiontot=[]
cout_total=[]
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


# # --- Affichage avec sous-graphiques ---
# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 8), sharex=True)

# # 1. Précision
# ax1.plot(n_moteur, precisiontot, label="Précision", color="blue", marker="o")
# ax1.set_ylabel("Précision")
# ax1.grid(True)
# ax1.legend(loc="upper left")

# # 2. Énergie
# ax2.plot(n_moteur, energytot, label="Énergie", color="green", marker="s")
# ax2.set_ylabel("Énergie")
# ax2.grid(True)
# ax2.legend(loc="upper left")

# # 3. Coût
# ax3.plot(n_moteur, cout_total, label="Coût (€)", color="red", marker="^")
# ax3.set_xlabel("Nombre de moteurs")
# ax3.set_ylabel("Coût (€)")
# ax3.grid(True)
# ax3.legend(loc="upper left")

# fig.suptitle("Précision, Énergie et Coût en fonction du nombre de moteurs")
# plt.tight_layout()
# plt.show()

#si on veut tout sur un seul graphique entre 0 et 1
# --- Normalisation des séries ---
p_max = max(precisiontot) if max(precisiontot) != 0 else 1
e_max = max(energytot) if max(energytot) != 0 else 1
c_max = max(cout_total) if max(cout_total) != 0 else 1

prec_norm = [p / p_max for p in precisiontot]
e_norm = [e / e_max for e in energytot]
cout_norm = [c / c_max for c in cout_total]

# --- Affichage ---
plt.figure(figsize=(8, 5))
plt.plot(n_moteur, prec_norm, label="Précision (normalisée)", color="blue", marker="o")
plt.plot(n_moteur, e_norm, label="Énergie (normalisée)", color="green", marker="s")
plt.plot(n_moteur, cout_norm, label="Coût (normalisé)", color="red", marker="^")

plt.xlabel("Nombre de moteurs")
plt.ylabel("Valeur relative (0 à 1)")
plt.title("Évolution relative de la précision, de l'énergie et du coût")
plt.legend()
plt.grid(True)
plt.show()
#
#decommander un bloc ctrl K control U
# on voit pas bien les courbes
# plt.plot(n_moteur,precisiontot,label="Precision",color="Blue")
# plt.plot(n_moteur,energytot,label="Energie",color="green")
# plt.plot(n_moteur,cout_total,label="Cout en euros",color="red")
# plt.xlabel("Nombre de moteurs")
# plt.ylabel("Valeurs")
# plt.title("Precision,cout et energie en fonction des moteurs")
# plt.legend()
# plt.grid()
# plt.show()

# def optimiser_moteurs(n_moteur, precisiontot, energytot, cout_total, seuil_precision=0.81):
#     # Normalisation des variables pour qu'elles restent comparables
#     e_max = max(energytot) if max(energytot) > 0 else 1
#     c_max = max(cout_total) if max(cout_total) > 0 else 1

#     scores = []
    
#     for i in range(len(n_moteur)):
#         p = precisiontot[i]
#         e_norm = energytot[i] / e_max
#         c_norm = cout_total[i] / c_max
        
#         # Application d'une forte pénalité si la précision est insuffisante
#         if p < seuil_precision:
#             penalite = 1000  
#         else:
#             penalite = 0
            
#         # Score à minimiser (poids à ajuster selon tes priorités)
#         score = 0.5 * e_norm + 0.5 * c_norm + penalite
#         scores.append(score)

#     idx_opt = np.argmin(scores)
#     return n_moteur[idx_opt], precisiontot[idx_opt], energytot[idx_opt], cout_total[idx_opt]

# # Utilisation
# m_opt, p_opt, e_opt, c_opt = optimiser_moteurs(n_moteur, precisiontot, energytot, cout_total)
# print(f"Moteurs optimaux : {m_opt} (Précision : {p_opt:.3f}, Énergie : {e_opt:.3f}, Coût : {c_opt} €)")
