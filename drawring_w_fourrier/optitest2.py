import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from lebonaimport import analyser_fourier
from trace_energie_cinetique import trace_tps_energie
from precision_main import compute_precision
from programme_coût import Cout
from Energie_totale_finale import *
import math

n_moteur_max = int(input("Choississez le nombre maximal de moteurs "))
filename = input("Choisissez un fichier à exploiter entre engrenages.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))
n_moteur=list(range(1, n_moteur_max + 1))
# 1. ÉTAPE 1 : Calcul des métriques pour tous les moteurs
energytot = []
precisiontot = []
cout_total = []

for i in range(len(n_moteur)):
    x0, y0, moteurs, barres, phi, teta = analyser_fourier(
        filename=filename,
        n_circles=n_moteur[i],
        exporter_txt=False,
        animer=False,
    )
    energie = trace_tps_energie(barres, teta, phi)
    precision = compute_precision(
        x0, y0, barres, teta, phi, selection, periode=0.10, display_plot=False
    )
    cout = Cout(sum(barres[: i + 1]), 4, n_moteur[i])

    energytot.append(energie)
    precisiontot.append(precision)
    cout_total.append(cout)

# Convertir en tableaux NumPy pour faciliter les calculs
P = np.array(precisiontot)
C = np.array(cout_total)
E = np.array(energytot)

# 2. ÉTAPE 2 : Normalisation entre 0 et 1
# Pour la précision : 1 est le meilleur
P_norm = (P - P.min()) / (P.max() - P.min() + 1e-8)

# Pour le coût et l'énergie : 0 est le meilleur (on inverse donc pour l'optimisation)
C_norm = (C - C.min()) / (C.max() - C.min() + 1e-8)
E_norm = (E - E.min()) / (E.max() - E.min() + 1e-8)

# 3. ÉTAPE 3 : Fonction d'optimisation avec poids configurables
# Pondérations : ajuste ces poids selon tes priorités (ex: α=0.5 pour la précision, β=0.3 pour le coût, γ=0.2 pour l'énergie)
alpha = 0.5
beta = 0.3
gamma = 0.2

# Score où l'on cherche à maximiser la précision et minimiser (coût + énergie)
opti = alpha * P_norm - beta * C_norm - gamma * E_norm

# Trouver l'indice optimal
idx_opti = np.argmax(opti)
print(
    f"Nombre de moteurs optimal : {n_moteur[idx_opti]} (Score: {opti[idx_opti]:.3f})"
)

# Affichage
plt.figure()
plt.plot(n_moteur, opti, label="Score d'optimisation", color="blue")
plt.axvline(
    x=n_moteur[idx_opti],
    color="red",
    linestyle="--",
    label=f"Optimum ({n_moteur[idx_opti]} moteurs)",
)
plt.xlabel("Nombre de moteurs")
plt.ylabel("Score relatif")
plt.title("Optimisation du nombre de moteurs")
plt.legend()
plt.grid(True)
plt.show()