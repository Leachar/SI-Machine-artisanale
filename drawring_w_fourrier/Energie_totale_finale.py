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
def trace_tps_energie(L, w, theta0, m_barre=None, afficher_graphe=False):
    # Si m_barre n'est pas renseignée, on la calcule avec la fonction intermédiaire
    if m_barre is None:
        m_barre = calculer_masses_barres(L)

    expr_barres = [
        energie_barre_details(i, L, w, theta0, m_barre)
        for i in range(1, len(L) + 1)
    ]
    expr_moteurs = energie_moteurs_totale(L, w, theta0, m_moteur)

    # Vitesse du stylo (bout de la dernière barre)
    vx_stylo, vy_stylo = position_vitesse_moteur(L, w, theta0)
    expr_p_stylo = puissance_stylo(vx_stylo, vy_stylo, ft=1.8)

    # Conversions Lambdify
    func_moteurs = sp.lambdify(t, expr_moteurs, "numpy")
    func_barres = [
        (sp.lambdify(t, trans, "numpy"), sp.lambdify(t, rot, "numpy"))
        for trans, rot in expr_barres
    ]
    func_p_stylo = sp.lambdify(t, expr_p_stylo, "numpy")

    # Tableau de temps
    temps = np.arange(0, t_max + delta_t, delta_t)

    # Évaluation numérique
    e_moteurs_vals = func_moteurs(temps)
    e_barres_vals = np.zeros_like(temps)

    for f_trans, f_rot in func_barres:
        e_barres_vals += f_trans(temps) + f_rot(temps)

    # Énergie cinétique instantanée globale (J)
    e_cinetique_totale = e_barres_vals + e_moteurs_vals

    # Sécurité 1 : filtre les divisions par zéro (NaN)
    e_cinetique_totale = np.nan_to_num(e_cinetique_totale, nan=0.0)

    # Puissance instantanée dissipée par le stylo (W)
    p_stylo_vals = func_p_stylo(temps)

    # Sécurité 2 : conversion si la puissance est une constante/scalaire
    if np.isscalar(p_stylo_vals) or np.ndim(p_stylo_vals) == 0:
        p_stylo_vals = np.full_like(temps, p_stylo_vals, dtype=float)

    # Sécurité 3 : filtre les NaN pour le stylo
    p_stylo_vals = np.nan_to_num(p_stylo_vals, nan=0.0)

    # Bilan énergétique global
    E_cin_moy, W_frot_total, E_globale = bilan_energetique_trace_complet(
        e_cinetique_totale, p_stylo_vals, temps
    )

    print("==================================================")
    print(f"BILAN ÉNERGÉTIQUE GLOBAL DU TRACÉ COMPLET ({t_max} s) :")
    print(
        f" - Énergie cinétique moyenne (Ec_moy)           : {E_cin_moy:.6f} J"
    )
    print(
        f" - Travail dissipé par le frottement (W_stylo)  : {W_frot_total:.6f} J"
    )
    print(" ------------------------------------------------")
    print(
        f" = ÉNERGIE TOTALE CONSOMMÉE SUR LE TRACÉ        : {E_globale:.6f} J"
    )
    print("==================================================\n")

    # Affichage optionnel du graphe (désactivé par défaut pour les boucles)
    if afficher_graphe:
        plt.figure(figsize=(9, 5))
        plt.plot(
            temps,
            e_cinetique_totale,
            label=r"Énergie cinétique instantanée ($E_c(t)$)",
            color="b",
            linewidth=1.5,
        )
        plt.title(
            f"Évolution de l'énergie cinétique au cours du temps (Δt = {delta_t} s)"
        )
        plt.xlabel("Temps (s)")
        plt.ylabel("Énergie cinétique (J)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return E_globale