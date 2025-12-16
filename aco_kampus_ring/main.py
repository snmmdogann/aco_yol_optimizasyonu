# main.py
import os
import streamlit as st

from data.coordinates import (
    get_location_names,
    fetch_and_store_coordinates,
    parse_coordinates
)
from core.matrix_utils import create_distance_matrix
from core.ant_algorithm import AntColony
from visual.plotting import create_route_map, plot_convergence

# Folium kontrolü
try:
    from streamlit_folium import st_folium
    FOLIUM_AVAILABLE = True
except Exception:
    FOLIUM_AVAILABLE = False


# =============================
# Streamlit Ayarları
# =============================
st.set_page_config(page_title="Kampüs Ring Optimizasyonu", layout="wide")
st.title("🚍 Karınca Kolonisi ile Kampüs Ring Optimizasyonu")


# =============================
# Sidebar
# =============================
st.sidebar.header("🔧 Ayarlar")

default_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
api_key = st.sidebar.text_input(
    "Google Maps API anahtarı (sadece koordinatlar için)",
    value=default_key,
    type="password"
)

st.sidebar.markdown("---")
st.sidebar.header("🐜 ACO Parametreleri")

n_ants = st.sidebar.slider("Karınca sayısı", 5, 100, 20)
n_iter = st.sidebar.slider("İterasyon sayısı", 10, 500, 100)
alpha = st.sidebar.slider("Alpha (feromon)", 0.1, 5.0, 1.0)
beta = st.sidebar.slider("Beta (mesafe ağırlığı)", 0.1, 10.0, 5.0)
rho = st.sidebar.slider("Buharlaşma (rho)", 0.01, 0.95, 0.5)
Q = st.sidebar.slider("Q (feromon sabiti)", 10.0, 500.0, 100.0)

st.sidebar.markdown("---")
st.sidebar.header("📍 Duraklar")
names = get_location_names()
for i, nm in enumerate(names):
    st.sidebar.write(f"{i+1}. {nm}")

st.markdown("---")


# =============================
# Koordinatları Hazırla
# =============================
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("📥 Koordinatları Hazırla (Google Geocoding)"):
        if not api_key:
            st.error("📌 Lütfen Google Maps API anahtarınızı girin.")
        else:
            try:
                fetch_and_store_coordinates(api_key, force=True)
                coords = parse_coordinates()
                st.session_state["coordinates"] = coords
                st.success("✅ Koordinatlar başarıyla alındı.")
            except Exception as e:
                st.error(f"Koordinatlar alınamadı: {e}")


# =============================
# Mesafe Matrisi (Haversine)
# =============================
with col2:
    if st.button("📊 Mesafe Matrisini Hesapla"):
        if "coordinates" not in st.session_state:
            st.error("Önce koordinatları hazırlayın.")
        else:
            coords = st.session_state["coordinates"]
            dm = create_distance_matrix(coords)
            st.session_state["distance_matrix"] = dm
            st.success("✅ Mesafe matrisi oluşturuldu (Haversine).")
            st.dataframe(dm, use_container_width=True, height=300)

st.markdown("---")


# =============================
# Optimizasyonu Başlat
# =============================
if st.button("🚀 Optimizasyonu Başlat"):
    if "distance_matrix" not in st.session_state:
        st.error("Önce mesafe matrisini hesaplayın.")
    else:
        dm = st.session_state["distance_matrix"]
        coords = st.session_state["coordinates"]

        progress = st.progress(0)
        info = st.empty()
        info.info("🐜 Optimizasyon başlatıldı...")

        colony = AntColony(
            distance_matrix=dm,
            n_ants=n_ants,
            n_iterations=n_iter,
            alpha=alpha,
            beta=beta,
            evaporation_rate=rho,
            Q=Q
        )

        best_path, best_length, history = colony.run()

        progress.progress(100)
        info.success("✅ Optimizasyon tamamlandı.")

        readable_path = [names[i] for i in best_path] + [names[best_path[0]]]

        st.session_state.update({
            "best_path": best_path,
            "best_length": best_length,
            "history": history,
            "readable_path": readable_path
        })


# =============================
# Sonuçlar
# =============================
if "best_path" in st.session_state:
    st.markdown("---")
    st.header("📊 Sonuçlar")

    st.metric(
        "En iyi toplam mesafe",
        f"{st.session_state['best_length']:.4f} km"
    )

    history = st.session_state["history"]
    if history:
        initial = history[0]
        best = st.session_state["best_length"]
        improvement = ((initial - best) / initial) * 100 if initial > 0 else 0
        st.metric("İyileşme oranı", f"%{improvement:.2f}")

    st.write("🛣️ **Rota:** " + " → ".join(st.session_state["readable_path"]))

    col1, col2 = st.columns([3, 2])

    # Harita
    with col1:
        st.subheader("🗺️ Harita (En Kısa Rota)")
        if FOLIUM_AVAILABLE:
            m = create_route_map(
                st.session_state["coordinates"],
                names,
                st.session_state["best_path"],
                st.session_state["best_length"]
            )
            st_folium(m, width=700, height=500)
        else:
            st.warning("Harita için folium gerekli.")

    # Yakınsama Grafiği
    with col2:
        st.subheader("📈 Yakınsama Grafiği")
        fig = plot_convergence(history)
        st.pyplot(fig)

    # Detaylı tablo
    st.subheader("📋 Detaylı Rota Tablosu")
    rows = []
    for i, idx in enumerate(st.session_state["best_path"]):
        next_idx = st.session_state["best_path"][(i + 1) % len(st.session_state["best_path"])]
        dist = st.session_state["distance_matrix"][idx, next_idx]
        rows.append({
            "Sıra": i + 1,
            "Durak": names[idx],
            "Sonraki Durak": names[next_idx],
            "Mesafe (km)": f"{dist:.4f}"
        })

    st.dataframe(rows, use_container_width=True)

st.markdown("---")
st.caption("🎓 Kampüs Ring Optimizasyonu | ACO + Haversine")
