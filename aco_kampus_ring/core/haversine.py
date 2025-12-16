# core/haversine.py
import math

def haversine_distance(coord1, coord2):
    """
    coord1, coord2: (lat, lon)
    dönüş: km cinsinden mesafe
    """
    R = 6371.0  # Dünya yarıçapı (km)

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
