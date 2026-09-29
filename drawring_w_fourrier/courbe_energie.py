import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from lebonaimport import analyser_fourier
from trace_energie_cinetique import trace_tps_energie

n_moteur = int(input("Combien de moteurs voulez-vous tester ? "))
filename = input("Choisissez un fichier à exploiter entre engrenagestest.txt, lion.txt, abeilles.txt et carde.txt : ")
selection = float(input("Choisissez l'image de référence à tester (0 pour le cadre, 1 pour le lion, 2 pour les abeilles et 3 pour les engrenages) : "))

x0, y0, moteurs, barres, phi, teta = analyser_fourier(
    filename=filename, 
    n_circles=n_moteur, 
    exporter_txt=False, 
    animer=False 
)
m_moteur = 0.045  # Masse d'un moteur (kg)
def calculer_masses_barres(L, masse_lineique=0.05):
  """Calcule la masse de chaque barre en fonction de sa longueur L. masse_lineique : masse par mètre (kg/m), par défaut 0.05 kg/m (50 g/m)."""
  # en fonction de l'énoncé, avec une section circulaire de 4mm
  return [longueur * masse_lineique for longueur in L]
m_barre = calculer_masses_barres(barres, masse_lineique=0.05)  # Masse de chaque barre (kg)

trace=trace_tps_energie(barres,teta,phi,m_barre)
