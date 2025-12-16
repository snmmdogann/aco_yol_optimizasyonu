import os
import folium
from folium.plugins import AntPath
import matplotlib.pyplot as plt


FIGURE_DIR = "figure"


def _ensure_figure_dir():
    if not os.path.exists(FIGURE_DIR):
        os.makedirs(FIGURE_DIR)


# =============================
# Harita
# =============================
def create_route_map(coords, names, best_path, best_length, save=True):
    _ensure_figure_dir()

    # Harita merkezi
    center_lat = sum(c[0] for c in coords) / len(coords)
    center_lon = sum(c[1] for c in coords) / len(coords)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15
    )

    # Başlangıç durağı indexi
    start_idx = best_path[0] if best_path else 0

    # === DURAKLAR ===
    for i, (lat, lon) in enumerate(coords):
        if i == start_idx:
            # 🚩 Başlangıç durağı
            folium.Marker(
                location=[lat, lon],
                popup=f"🚩 Başlangıç: {names[i]}",
                icon=folium.Icon(color="green", icon="play")
            ).add_to(m)
        else:
            # Diğer duraklar
            folium.Marker(
                location=[lat, lon],
                popup=names[i],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    # === ROTA (AntPath) ===
    if best_path and len(best_path) > 1:
        route = [coords[i] for i in best_path] + [coords[start_idx]]

        AntPath(
            locations=route,
            color="blue",
            weight=5
        ).add_to(m)

    # 📌 HTML olarak kaydet
    if save:
        m.save(os.path.join(FIGURE_DIR, "rota.html"))

    return m


# =============================
# Yakınsama Grafiği
# =============================
def plot_convergence(history, save=True):
    _ensure_figure_dir()

    if not history:
        history = [0]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(history)
    ax.set_title("ACO Yakınsama Grafiği")
    ax.set_xlabel("İterasyon")
    ax.set_ylabel("En İyi Mesafe (km)")
    ax.grid(True)

    # 📌 PNG olarak kaydet
    if save:
        fig.savefig(
            os.path.join(FIGURE_DIR, "convergence.png"),
            dpi=300,
            bbox_inches="tight"
        )

    return fig
