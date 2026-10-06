import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


#pour appeler energie = trace_tps_energie(barres, teta, phi) # Au début de ton fichier principal
#from trace_energie_cinetique import trace_tps_energie

# Dans ta boucle
#energie = trace_tps_energie(barres, teta, phi)





# ==========================================
# 1. PARAMÈTRES ET SYMBOLES GLOBAUX
# ==========================================
m_moteur = 0.045  # Masse d'un moteur (kg)
t_max = 0.1  # Durée totale de la simulation (s)
delta_t = 0.01  # Pas de temps Δt (s)
t = sp.Symbol("t")


def calculer_masses_barres(L, masse_lineique=0.05):
    """Calcule la masse de chaque barre en fonction de sa longueur L."""
    return [longueur * masse_lineique for longueur in L]


# ==========================================
# 2. FONCTIONS POUR LES MOTEURS
# ==========================================
def position_vitesse_moteur(L_sub, w_sub, theta0_sub):
    x, y = 0, 0
    w_cumule = 0
    for i in range(len(L_sub)):
        w_cumule += w_sub[i]
        angle_barre = w_cumule * t + theta0_sub[i]

        x += L_sub[i] * sp.cos(angle_barre)
        y += L_sub[i] * sp.sin(angle_barre)

    vx = sp.diff(x, t)
    vy = sp.diff(y, t)

    return vx, vy


def energie_moteurs_totale(L, w, theta0, m_mot):
    Ec_tot = 0
    for k in range(1, len(L) + 1):
        L_sub, w_sub, theta0_sub = L[: k - 1], w[: k - 1], theta0[: k - 1]
        if not L_sub:
            vx, vy = 0, 0
        else:
            vx, vy = position_vitesse_moteur(L_sub, w_sub, theta0_sub)
        Ec_tot += 0.5 * m_mot * (vx**2 + vy**2)

    return sp.expand(Ec_tot)


# ==========================================
# 3. FONCTIONS POUR LES BARRES
# ==========================================
def energie_barre_details(i, L, w, theta0, m_b):
    # 1. Rotation propre globale
    w_cumul = sum(w[:i])
    J_i = (1 / 12) * m_b[i - 1] * (L[i - 1] ** 2)
    Ec_rot = 0.5 * J_i * (w_cumul**2)

    # 2. Position du centre de masse (x_G, y_G)
    x_G, y_G = 0, 0
    w_cumule = 0

    for j in range(i - 1):
        w_cumule += w[j]
        angle_barre = w_cumule * t + theta0[j]
        x_G += L[j] * sp.cos(angle_barre)
        y_G += L[j] * sp.sin(angle_barre)

    w_cumule += w[i - 1]
    angle_barre_i = w_cumule * t + theta0[i - 1]
    x_G += 0.5 * L[i - 1] * sp.cos(angle_barre_i)
    y_G += 0.5 * L[i - 1] * sp.sin(angle_barre_i)

    # 3. Vitesse du centre de masse et énergie de translation
    vx_G = sp.diff(x_G, t)
    vy_G = sp.diff(y_G, t)
    Ec_trans = 0.5 * m_b[i - 1] * (vx_G**2 + vy_G**2)

    return sp.expand(Ec_trans), sp.expand(Ec_rot)


# ==========================================
# 4. FONCTION POUR LE STYLO ET BILAN
# ==========================================
def puissance_stylo(vx, vy, ft=1.8):
    """Exprime la puissance instantanée dissipée par frottement (en Watts)."""
    return ft * sp.sqrt(vx**2 + vy**2)


def bilan_energetique_trace_complet(e_cinetique_totale, p_stylo_vals, temps):
    # 1. Énergie cinétique moyenne maintenue par le mécanisme (J)
    E_c_moyenne = np.mean(e_cinetique_totale)

    # 2. Travail total dissipé par le frottement du stylo (J)
    W_frottement_total = np.trapezoid(p_stylo_vals, temps)

    # 3. Énergie globale consommée sur le tracé (J)
    E_globale_total = E_c_moyenne + W_frottement_total

    return E_c_moyenne, W_frottement_total, E_globale_total


# ==========================================
# 5. FONCTION PRINCIPALE (3 LISTES EN ENTRÉE)
# ==========================================
import numpy as np


def trace_tps_energie(
    L,
    w,
    theta0,
    m_barre=None,
    m_moteur=0.1,
    J_moteur=1e-4,
    ft=1.8,
    t_max=1.0,
    delta_t=0.001,
):
    # 1. Conversion des entrées en tableaux NumPy
    L = np.asarray(L, dtype=float)
    w = np.asarray(w, dtype=float)
    theta0 = np.asarray(theta0, dtype=float)

    if m_barre is None:
        m_barre = np.asarray(calculer_masses_barres(L), dtype=float)
    else:
        m_barre = np.asarray(m_barre, dtype=float)

    # 2. Vecteur temps
    temps = np.arange(0, t_max + delta_t, delta_t)
    T = len(temps)

    # 3. Calcul des angles theta_i(t) pour chaque barre i à chaque instant t (Matrice N x T)
    # L'utilisation de [:, None] et [None, :] réalise le produit vectoriel instantané (broadcasting)
    theta = w[:, None] * temps[None, :] + theta0[:, None]

    # 4. Composantes de vitesse relatives de chaque segment de barre
    vx_elem = -L[:, None] * w[:, None] * np.sin(theta)  # Matrice (N, T)
    vy_elem = L[:, None] * w[:, None] * np.cos(theta)  # Matrice (N, T)

    # 5. Vitesses absolues cumulées aux articulations (embouts des barres)
    v_joints_x = np.cumsum(vx_elem, axis=0)
    v_joints_y = np.cumsum(vy_elem, axis=0)

    # Vitesses à la base de chaque barre i (vitesse du moteur/joint i-1)
    v_base_x = np.vstack([np.zeros((1, T)), v_joints_x[:-1]])
    v_base_y = np.vstack([np.zeros((1, T)), v_joints_y[:-1]])

    # 6. Vitesse du centre de masse G_i de chaque barre (au milieu du segment)
    v_Gi_x = v_base_x + 0.5 * vx_elem
    v_Gi_y = v_base_y + 0.5 * vy_elem

    # 7. Énergie cinétique des barres (Translation + Rotation)
    e_trans_barres = 0.5 * m_barre[:, None] * (v_Gi_x**2 + v_Gi_y**2)
    I_G = (1.0 / 12.0) * m_barre * (L**2)
    e_rot_barres = 0.5 * I_G[:, None] * (w[:, None] ** 2)

    # Somme des énergies de toutes les barres à chaque instant t
    e_barres_vals = np.sum(e_trans_barres + e_rot_barres, axis=0)

    # 8. Énergie cinétique des moteurs (Masse en translation à la base + Rotation du rotor)
    e_trans_moteurs = 0.5 * m_moteur * (v_base_x**2 + v_base_y**2)
    e_rot_moteurs = 0.5 * J_moteur * (w[:, None] ** 2)
    e_moteurs_vals = np.sum(e_trans_moteurs + e_rot_moteurs, axis=0)

    # 9. Énergie cinétique totale instantanée
    e_cinetique_totale = e_barres_vals + e_moteurs_vals

    # 10. Puissance dissipée par le stylo (bout de la dernière barre)
    vx_stylo = v_joints_x[-1]
    vy_stylo = v_joints_y[-1]
    v_stylo = np.sqrt(vx_stylo**2 + vy_stylo**2)
    p_stylo_vals = ft * v_stylo

    # 11. Bilan énergétique global
    E_cin_moy, W_frot_total, E_globale = bilan_energetique_trace_complet(
        e_cinetique_totale, p_stylo_vals, temps
    )

    return E_globale