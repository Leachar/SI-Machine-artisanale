import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from lebonaimport import analyser_fourier
from trace_energie_cinetique import trace_tps_energie
from precision_main import compute_precision
from programme_coût import Cout
from Energie_totale_finale import *

# --- 1. SAISIES ET CALCULS (Code optimisé) ---
n_moteur_max = int(input("Choisissez le nombre maximal de moteurs : "))
filename = input("Choisissez un fichier à exploiter entre engrenages.txt, lion.txt, abeilles.txt et cadre.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))

n_moteur = list(range(1, n_moteur_max + 1))

x0, y0, moteurs_max, barres_max, phi_max, teta_max = analyser_fourier(
    filename=filename,
    n_circles=n_moteur_max,
    exporter_txt=False,
    animer=False,
)

energytot = []
precisiontot = []
cout_total = []

for k in range(1, n_moteur_max + 1):
    barres_k = barres_max[:k]
    phi_k = phi_max[:k]
    teta_k = teta_max[:k]

    energie = trace_tps_energie(barres_k, teta_k, phi_k)
    precision = compute_precision(
        x0,
        y0,
        barres_k,
        teta_k,
        phi_k,
        selection,
        periode=0.10,
        display_plot=False,
    )
    cout = Cout(sum(barres_k), 4, k)

    energytot.append(energie)
    precisiontot.append(precision)
    cout_total.append(cout)


# --- 2. PARTIE OPTIMISATION (À AJOUTER ICI) ---

# Conversion en tableaux NumPy pour simplifier les calculs
P = np.array(precisiontot)
C = np.array(cout_total)
E = np.array(energytot)

# Valeurs de référence FIXES (pour éviter le décalage quand n_moteur_max change)
COUT_REF = 800  # Budget/coût max fixe de référence (en €)
ENERGIE_REF = 15  # Énergie max fixe de référence
# Calcul des grandeurs relatives fixes
C_norm = C / COUT_REF
E_norm = E / ENERGIE_REF

# Calcul du score d'optimisation
opti = (P**5) / np.exp((C_norm**2) + E_norm)

# Extraction de l'indice de la valeur maximale
idx_opti = np.argmax(opti)
moteur_optimal = n_moteur[idx_opti]

print(
    f"Nombre de moteurs optimal : {moteur_optimal} | Précision : {P[idx_opti]:.2f} | Coût : {C[idx_opti]} €"
)


# --- 3. AFFICHAGE DU GRAPHIQUE ---

plt.figure(figsize=(9, 5))
plt.plot(n_moteur, opti, color="blue", label="Score d'optimisation")
plt.axvline(
    x=moteur_optimal,
    color="red",
    linestyle="--",
    label=f"Optimum ({moteur_optimal} moteurs)",
)

plt.xlabel("Nombre de moteurs")
plt.ylabel("Score relatif")
plt.title("Recherche du nombre optimal de moteurs")
plt.grid(True)
plt.legend()
plt.show()