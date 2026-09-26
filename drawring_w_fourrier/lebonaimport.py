#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ============================================================
# 1. CHARGEMENT ET PRÉTRAITEMENT
# ============================================================

def load_points(filename):
    """
    Charge un fichier TXT. Cherche automatiquement dans le dossier du script.
    """
    script_dir = Path(__file__).parent
    filepath = script_dir / filename

    if not filepath.exists():
        filepath = Path(filename)

    if not filepath.exists():
        raise FileNotFoundError(f"❌ Le fichier '{filename}' est introuvable dans {script_dir.resolve()}")

    points = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.replace(",", " ").split()
            if len(parts) >= 2:
                try:
                    points.append([float(parts[0]), float(parts[1])])
                except ValueError:
                    continue

    if len(points) < 3:
        raise ValueError("Le fichier doit contenir au moins 3 points valides.")

    return np.array(points, dtype=float)


def resample_curve(points, n_samples=1024):
    """Rééchantillonne la courbe de manière uniforme."""
    if not np.allclose(points[0], points[-1]):
        points = np.vstack([points, points[0]])

    differences = np.diff(points, axis=0)
    distances = np.sqrt(np.sum(differences ** 2, axis=1))
    cumulative = np.concatenate([[0], np.cumsum(distances)])
    total_length = cumulative[-1]

    if total_length == 0:
        raise ValueError("Tous les points sont identiques.")

    new_distances = np.linspace(0, total_length, n_samples, endpoint=False)
    x = np.interp(new_distances, cumulative, points[:, 0])
    y = np.interp(new_distances, cumulative, points[:, 1])

    return x, y


# ============================================================
# 2. EXPORT DU FICHIER TXT
# ============================================================

def export_txt_file(filename, n_moteurs, barres, phi, teta, period, x_0, y_0):
    """Crée le fichier texte récapitulatif avec les paramètres."""
    script_dir = Path(__file__).parent
    input_path = Path(filename)
    output_path = script_dir / f"{input_path.stem}_fourier_params.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("====================================================================================\n")
        f.write(f"                    PARAMÈTRES DE FOURIER - FICHIER : {filename}\n")
        f.write("====================================================================================\n\n")

        f.write("--- 1. INFORMATIONS GÉNÉRALES ---\n")
        f.write(f"Nombre de cercles / moteurs : {n_moteurs}\n")
        f.write(f"Période de rotation (T)      : {period:.4f} secondes\n")
        f.write(f"Position initiale (t=0)     : X0 = {x_0:.6f}, Y0 = {y_0:.6f}\n\n")

        f.write("--- 2. DÉTAIL DES MOTEURS / BARRES ---\n")
        header = f"{'Moteur N°':<10} | {'Longueur barre':<18} | {'Vitesse (rad/s)':<18} | {'Phase t=0 (rad)':<18} | {'Phase t=0 (deg)':<14}\n"
        f.write(header)
        f.write("-" * len(header) + "\n")

        for i in range(n_moteurs):
            f.write(f"{i+1:<10} | {barres[i]:<18.6f} | {teta[i]:<18.6f} | {phi[i]:<18.6f} | {np.degrees(phi[i]):<14.2f}\n")

        f.write("-" * len(header) + "\n")

    print(f"📄 Fichier texte généré : {output_path.name}")


# ============================================================
# 3. TRACÉ ET ANIMATION
# ============================================================

def tracer_animation(circles, original_x, original_y, period, title=""):
    """Affiche l'animation interactive avec Matplotlib."""
    frames = 400
    fig, ax = plt.subplots(figsize=(8, 8))

    margin = max(np.ptp(original_x), np.ptp(original_y)) * 0.2
    ax.set_xlim(np.min(original_x) - margin, np.max(original_x) + margin)
    ax.set_ylim(np.min(original_y) - margin, np.max(original_y) + margin)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.set_title(f"Fourier : {title} ({len(circles)} moteurs/cercles)")

    ax.plot(original_x, original_y, color="gray", alpha=0.3, linewidth=1, label="Original")

    circle_lines = [ax.plot([], [], color="blue", alpha=0.3)[0] for _ in circles]
    center_points = [ax.plot([], [], "o", color="red", markersize=2)[0] for _ in circles]
    trace, = ax.plot([], [], color="black", linewidth=2, label="Tracé")
    tip, = ax.plot([], [], "o", color="red", markersize=4)

    trace_x, trace_y = [], []

    def update(frame):
        if frame == 0:
            trace_x.clear()
            trace_y.clear()

        t = (frame / frames) * period
        center = 0j

        for i, c in enumerate(circles):
            vector = c["coef"] * np.exp(1j * c["omega"] * t)

            theta = np.linspace(0, 2 * np.pi, 50)
            circle_x = center.real + c["radius"] * np.cos(theta)
            circle_y = center.imag + c["radius"] * np.sin(theta)

            circle_lines[i].set_data(circle_x, circle_y)
            center_points[i].set_data([center.real], [center.imag])

            center += vector

        trace_x.append(center.real)
        trace_y.append(center.imag)

        trace.set_data(trace_x, trace_y)
        tip.set_data([center.real], [center.imag])

        return circle_lines + center_points + [trace, tip]

    anim = FuncAnimation(fig, update, frames=frames, interval=20, blit=True, repeat=True)
    plt.legend(loc="upper right")
    plt.show()


# ============================================================
# 4. FONCTION PRINCIPALE RENVOYANT LES DONNÉES
# ============================================================

def analyser_fourier(filename="lion.txt", n_circles=40, period=2.0, n_samples=1024, invert_y=False, exporter_txt=True, animer=True):
    """
    Calcule les harmoniques de Fourier, crée le fichier TXT, lance l'animation 
    et RETOURNE 6 valeurs :
    x_0, y_0, moteurs, barres, phi, teta = analyser_fourier(...)
    """
    points = load_points(filename)
    x, y = resample_curve(points, n_samples)
    if invert_y:
        y = -y

    z = x + 1j * y
    N = len(z)

    coefficients = np.fft.fft(z) / N
    frequencies = np.fft.fftfreq(N)
    integer_frequencies = np.round(frequencies * N).astype(int)

    indices = np.argsort(np.abs(coefficients))[::-1]
    n_circles = min(n_circles, N)
    selected = indices[:n_circles]

    moteurs = n_circles
    barres = []
    phi = []
    teta = []
    circles_struct = []

    for i in selected:
        coef = coefficients[i]
        freq = int(integer_frequencies[i])
        r = float(np.abs(coef))
        p = float(np.angle(coef))
        w = float(2 * np.pi * freq / period)

        barres.append(r)
        phi.append(p)
        teta.append(w)

        circles_struct.append({
            "coef": coef,
            "radius": r,
            "omega": w
        })

    # Position initiale X0, Y0 à t=0 (somme des composantes vectorielles)
    x_0 = float(sum(r * np.cos(p) for r, p in zip(barres, phi)))
    y_0 = float(sum(r * np.sin(p) for r, p in zip(barres, phi)))

    if exporter_txt:
        export_txt_file(filename, moteurs, barres, phi, teta, period, x_0, y_0)

    if animer:
        tracer_animation(circles_struct, x, y, period, title=filename)

    # RENVOI DES 6 VALEURS
    return x_0, y_0, moteurs, barres, phi, teta


# ============================================================
# 5. EXECUTION INTERACTIVE (Bouton Play ▶️)
# ============================================================

if __name__ == "__main__":
    files = {"1": "lion.txt", "2": "engrenages.txt", "3": "abeilles.txt", "4": "cadre.txt"}

    print("\n" + "=" * 50)
    print("   CHOIX DU FICHIER :")
    print("=" * 50)
    for k, v in files.items():
        print(f"  [{k}] {v}")
    
    choix_f = input("Entrez un numéro (1-4) [Défaut: 1] : ").strip()
    fichier_choisi = files.get(choix_f, "lion.txt")

    choix_n = input("Nombre de cercles/moteurs [Défaut: 40] : ").strip()
    nb_moteurs = int(choix_n) if choix_n.isdigit() else 40

    # RÉCUPÉRATION DES 6 VARIABLES
    x_0, y_0, moteurs, barres, phi, teta = analyser_fourier(
        filename=fichier_choisi, 
        n_circles=nb_moteurs, 
        period=2.0,
        exporter_txt=True,
        animer=True
    )

    print("\n" + "=" * 50)
    print("   VARIABLES RÉCUPÉRÉES AVEC SUCCÈS :")
    print("=" * 50)
    print(f"• Position initiale X0  = {x_0:.4f}")
    print(f"• Position initiale Y0  = {y_0:.4f}")
    print(f"• Nombre de moteurs     = {moteurs}")
    print(f"• Longueur barre 1      = {barres[0]:.4f}")
    print(f"• Phase 1 (rad)         = {phi[0]:.4f}")
    print(f"• Vitesse 1 (rad/s)     = {teta[0]:.4f}")