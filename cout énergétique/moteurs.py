# Programme pour l'énergie des moteurs :

import sympy as sp


# L = [0.05, 0.02, 0.1]     #liste des longueurs des barres 
# w = [15, 12, 13]      #liste des vitesses angulaires des barres 
# m = 0.045      #masse d'un moteur (en kg)
# t = sp.Symbol('t')

# def equations_mouvement_derivees(L, w):   #fonction pour calculer les équations de positon et les dérivées des composantes
#     t = sp.Symbol('t')
#     x = 0
#     y = 0
    
#     for i in range(len(L) -1):
#         x += L[i] * sp.cos(w[i] * t)
#         y += L[i] * sp.sin(w[i] * t)
        
#     vx = sp.diff(x, t)
#     vy = sp.diff(y, t)
#     return x, y, vx, vy

# def energie_cinetique(vx, vy):   #fonction pour calculer l'énergie cinétqiue d'un moteur 
#     Ec = 1/2*m*(vx**2 + vy**2)
#     return Ec

# def energie_cinetique_totale(L, w):
#     Ec_totale = 0
    
#     # On parcourt chaque moteur (chaque articulation)
#     for k in range(1, len(L) + 1):
#         # Sous-listes des barres et vitesses jusqu'au k-ième moteur
#         L_sub = L[:k]
#         w_sub = w[:k]
        
#         # Obtention des vitesses vx, vy pour le moteur k
#         _, _, vx, vy = equations_mouvement_derivees(L_sub, w_sub)
        
#         # Ajout de l'énergie cinétique de ce moteur à la somme
#         Ec_totale += energie_cinetique(vx, vy)
        
#     return Ec_totale

# # 1. Calcul de l'énergie cinétique totale
# Ec_tot = energie_cinetique_totale(L, w)

# # 2. Affichage du résultat
# print("Énergie cinétique totale :")
# print(Ec_tot)

import sympy as sp

# Données
L = [0.05, 0.01]    # Longueurs des barres (m)
w = [15,  35]         # Vitesses angulaires (rad/s)
m = 0.045                # Masse d'un moteur (kg)

def position_et_vitesse(L_sub, w_sub):
    """Calcule la vitesse du point situé au bout de la chaîne L_sub."""
    t = sp.Symbol('t')
    x = 0
    y = 0
    
    # On parcourt TOUTES les barres fournies dans la sous-liste
    for i in range(len(L_sub)):
        x += L_sub[i] * sp.cos(w_sub[i] * t)
        y += L_sub[i] * sp.sin(w_sub[i] * t)
        
    vx = sp.diff(x, t)
    vy = sp.diff(y, t)
    return vx, vy

def energie_cinetique(vx, vy, m):
    """Calcul de l'énergie cinétique d'une masse m."""
    return 0.5 * m * (vx**2 + vy**2)

def energie_cinetique_totale(L, w, m):
    Ec_totale = 0
    
    # On parcourt chaque moteur k (de 1 à n)
    for k in range(1, len(L) + 1):
        # Le moteur k est au bout de la barre k-1 (donc barres 0 à k-2)
        L_sub = L[:k-1]
        w_sub = w[:k-1]
        
        # Moteur 1 (k=1) : fixé au bâti -> vitesse nulle
        if not L_sub:
            vx, vy = 0, 0
        else:
            vx, vy = position_et_vitesse(L_sub, w_sub)
            
        Ec_totale += energie_cinetique(vx, vy, m)
        
    return Ec_totale

# 1. Calcul
Ec_tot = energie_cinetique_totale(L, w, m)

# 2. Affichage (sp.simplify permet d'obtenir la valeur numérique directe)
print("Énergie cinétique totale (en Joules) :")
print(sp.simplify(Ec_tot))