# core/matrix_utils.py
import numpy as np
from core.haversine import haversine_distance

# =============================
# Haversine ile Mesafe Matrisi
# =============================
def create_distance_matrix(coords):
    """
    coords: [(lat, lon), ...]
    dönüş: numpy mesafe matrisi (km)
    """
    if not coords:
        raise ValueError("coords listesi boş olamaz.")

    n = len(coords)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0.0
            else:
                matrix[i][j] = haversine_distance(coords[i], coords[j])

    return matrix
