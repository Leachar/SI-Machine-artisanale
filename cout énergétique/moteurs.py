# # Programme pour l'énergie des moteurs

# import sympy as sp

# # Données
# L = [0.05, 0.01]    # Longueurs des barres (m)
# w = [15,  35]         # Vitesses angulaires (rad/s)
# m = 0.045       # Masse d'un moteur (kg)
# theta0 = [0, 0, 0]       #angles initaux

# def position_et_vitesse(L_sub, w_sub):
#     """Calcule la vitesse du point situé au bout de la chaîne L_sub."""
#     t = sp.Symbol('t')
#     x = 0
#     y = 0
    
#     # On parcourt TOUTES les barres fournies dans la sous-liste
#     for i in range(len(L_sub)):
#         x += L_sub[i] * sp.cos(w_sub[i] * t)
#         y += L_sub[i] * sp.sin(w_sub[i] * t)
        
#     vx = sp.diff(x, t)
#     vy = sp.diff(y, t)
#     return vx, vy

# def energie_cinetique(vx, vy, m):
#     """Calcul de l'énergie cinétique d'une masse m."""
#     return 0.5 * m * (vx**2 + vy**2)

# def energie_cinetique_totale(L, w, m):
#     Ec_totale = 0
    
#     # On parcourt chaque moteur k (de 1 à n)
#     for k in range(1, len(L) + 1):
#         # Le moteur k est au bout de la barre k-1 (donc barres 0 à k-2)
#         L_sub = L[:k-1]
#         w_sub = w[:k-1]
        
#         # Moteur 1 (k=1) : fixé au bâti -> vitesse nulle
#         if not L_sub:
#             vx, vy = 0, 0
#         else:
#             vx, vy = position_et_vitesse(L_sub, w_sub)
            
#         Ec_totale += energie_cinetique(vx, vy, m)
        
#     return Ec_totale

# # 1. Calcul
# Ec_tot = energie_cinetique_totale(L, w, m)

# # 2. Affichage (sp.simplify permet d'obtenir la valeur numérique directe)
# print("Énergie cinétique totale (en Joules) :")
# print(sp.simplify(Ec_tot))


# #Programme pour la vitesse des barres :

# def energie_cinetique_barre(i, L, w, theta0, m):
#     """
#     Calcule l'énergie cinétique globale (translation du centre de masse + rotation propre) 
#     de la barre i.
#     i : indice de la barre (1-indexed)
#     """
#     t = sp.Symbol('t')
    
#     # --- 1. Énergie de rotation ---
#     w_i_cumul = sum(w[:i])
    
#     # Moment d'inertie par rapport au centre de masse : 1/12 * m_i * L_i^2
#     J_i = (1 / 12) * m[i - 1] * (L[i - 1] ** 2)
#     Ec_rot = 0.5 * J_i * (w_i_cumul ** 2)
    
#     # --- 2. Position du centre de masse (x_i, y_i) ---
#     x_i = 0
#     y_i = 0
    
#     # Somme des barres précédentes
#     for j in range(i - 1):
#         theta_j = w[j] * t + theta0[j]
#         x_i += L[j] * sp.cos(theta_j)
#         y_i += L[j] * sp.sin(theta_j)
        
#     # Ajout du demi-tronçon de la barre i
#     theta_i = w[i - 1] * t + theta0[i - 1]
#     x_i += 0.5 * L[i - 1] * sp.cos(theta_i)
#     y_i += 0.5 * L[i - 1] * sp.sin(theta_i)
    
#     # --- 3. Vitesse du centre de masse et énergie de translation ---
#     vx_i = sp.diff(x_i, t)
#     vy_i = sp.diff(y_i, t)
#     V_i_carre = vx_i**2 + vy_i**2
    
#     Ec_trans = 0.5 * m[i - 1] * V_i_carre
    
#     # --- 4. Énergie totale de la barre i ---
#     return sp.simplify(Ec_trans + Ec_rot)

# # --- Calcul et affichage évalués à t = 0 ---
# t = sp.Symbol('t')
# Ec_totale_systeme = 0

# for i in range(1, len(L) + 1):
#     Ec_trans, Ec_rot = energie_cinetique_barre(i, L, w, theta0, m)
    
#     # Évaluation numérique à t = 0
#     val_trans = float(Ec_trans.subs(t, 0))
#     val_rot = float(Ec_rot.subs(t, 0))
#     val_tot = val_trans + val_rot
    
#     Ec_totale_systeme += val_tot
    
#     print(f"--- BARRE {i} ---")
#     print(f"  Ec_trans = {val_trans:.6f} J")
#     print(f"  Ec_rot   = {val_rot:.6f} J")
#     print(f"  Somme    = {val_tot:.6f} J\n")

# print("====================================")
# print(f"Énergie cinétique totale du système (t=0) : {Ec_totale_systeme:.6f} J")

import sympy as sp

# ==========================================
# 1. DONNÉES DU SYSTÈME
# ==========================================
L = [0.05, 0.02, 0.1]          # Longueurs des barres (m)
w = [15, 12, 13]               # Vitesses angulaires des barres (rad/s)
theta0 = [0, 0, 0]             # Angles initiaux à t=0 (rad)

m_moteur = 0.045               # Masse d'un moteur (kg)
m_barre = [0.03, 0.03, 0.03]   # Masse de chaque barre (kg)

t = sp.Symbol('t')

# ==========================================
# 2. FONCTIONS POUR LES MOTEURS
# ==========================================
def position_vitesse_moteur(L_sub, w_sub, theta0_sub):
    x, y = 0, 0
    for i in range(len(L_sub)):
        angle = w_sub[i] * t + theta0_sub[i]
        x += L_sub[i] * sp.cos(angle)
        y += L_sub[i] * sp.sin(angle)
    return sp.diff(x, t), sp.diff(y, t)

def energie_moteurs_totale(L, w, theta0, m_mot):
    Ec_mot = 0
    for k in range(1, len(L) + 1):
        L_sub, w_sub, theta0_sub = L[:k-1], w[:k-1], theta0[:k-1]
        if not L_sub:
            vx, vy = 0, 0
        else:
            vx, vy = position_vitesse_moteur(L_sub, w_sub, theta0_sub)
        
        # Énergie du moteur k
        Ec_mot += 0.5 * m_mot * (vx**2 + vy**2)
    return sp.simplify(Ec_mot)

# ==========================================
# 3. FONCTIONS POUR LES BARRES
# ==========================================
def energie_barre_details(i, L, w, theta0, m_b):
    # Rotation propre autour du centre de masse (J = 1/12 * m * L^2)
    w_cumul = sum(w[:i])
    J_i = (1 / 12) * m_b[i - 1] * (L[i - 1] ** 2)
    Ec_rot = 0.5 * J_i * (w_cumul ** 2)
    
    # Position du centre de masse (x_G, y_G)
    x_G, y_G = 0, 0
    for j in range(i - 1):
        angle_j = w[j] * t + theta0[j]
        x_G += L[j] * sp.cos(angle_j)
        y_G += L[j] * sp.sin(angle_j)
        
    angle_i = w[i - 1] * t + theta0[i - 1]
    x_G += 0.5 * L[i - 1] * sp.cos(angle_i)
    y_G += 0.5 * L[i - 1] * sp.sin(angle_i)
    
    # Translation du centre de masse
    vx_G = sp.diff(x_G, t)
    vy_G = sp.diff(y_G, t)
    Ec_trans = 0.5 * m_b[i - 1] * (vx_G**2 + vy_G**2)
    
    return sp.simplify(Ec_trans), sp.simplify(Ec_rot)

# ==========================================
# 4. EXÉCUTION ET AFFICHAGE
# ==========================================
print("=== ÉNERGIE DES BARRES (DÉTAILS À t = 0) ===")
Ec_barres_totale = 0

for i in range(1, len(L) + 1):
    Ec_trans, Ec_rot = energie_barre_details(i, L, w, theta0, m_barre)
    
    # Évaluation numérique à t = 0
    val_trans = float(Ec_trans.subs(t, 0))
    val_rot = float(Ec_rot.subs(t, 0))
    val_tot = val_trans + val_rot
    
    Ec_barres_totale += val_tot
    
    # print(f"Barre {i} :")
    # print(f"  Ec_trans = {val_trans:.6f} J")
    # print(f"  Ec_rot   = {val_rot:.6f} J")
    # print(f"  Total    = {val_tot:.6f} J")

print(f"\nÉnergie totale des barres (t=0) : {Ec_barres_totale:.6f} J")

print("\n=== ÉNERGIE DES MOTEURS (t = 0) ===")
Ec_moteurs_symbolique = energie_moteurs_totale(L, w, theta0, m_moteur)
Ec_moteurs_valeur = float(Ec_moteurs_symbolique.subs(t, 0))
print(f"Énergie totale des moteurs (t=0) : {Ec_moteurs_valeur:.6f} J")

print("\n==========================================")
print(f"ÉNERGIE CINÉTIQUE GLOBALE DU SYSTÈME (t=0) : {Ec_barres_totale + Ec_moteurs_valeur:.6f} J")