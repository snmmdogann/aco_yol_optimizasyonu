# data/coordinates.py
"""
Koordinatlar + Geocoding yardımcıları
- CAMPUS_CONFIG: durak isimleri ve Google sorguları
- fetch_and_store_coordinates(api_key) -> CAMPUS_CONFIG içine lat/lng ekler (hata korumalı)
- parse_coordinates() -> kesinlikle None dönmez, mantıklı default kullanır
- get_location_names() -> isim listesi
"""

import os
import requests


CAMPUS_CONFIG= [
    {"name": "29 Ekim Yüzme Havuzu", "query": "29 Ekim Yüzme Havuzu, Isparta, Türkiye"},
    {"name": "Süleyman Demirel Üniversitesi Araştırma Ve Uygulama Hastanesi", "query": "Süleyman Demirel Üniversitesi Araştırma Ve Uygulama Hastanesi"},
    {"name": "Bilgi Merkezi", "query": "SDÜ Bilgi Merkezi, Isparta"},
    {"name": "SDÜ Spor Tesisleri", "query": "SDÜ Spor Tesisleri, Isparta"},
    {"name": "ISUBÜ Orman Fakültesi", "query": "ISUBÜ Orman Fakültesi"},
    {"name": "Lütfü Çakmakçı Kültür Merkezi", "query": "SDÜ Lütfü Çakmakçı Kültür Merkezi"},
    {"name": "Fen Edebiyat Fakültesi", "query": "SDÜ Fen Edebiyat Fakültesi"},
    {"name": "İktisadi ve İdari Bilimler Fakültesi", "query": "SDÜ İİBF"},
    {"name": "KYK Öğrenci Yurdu", "query": "KYK Öğrenci Yurdu, Isparta"},
    {"name": "SDÜ Doğu Kampüs Girişi", "query": "SDÜ Doğu Kampüs Girişi"},
]

# Mantıklı default koordinat (Isparta merkezi)
DEFAULT_COORD = (37.7641, 30.5566)


def get_location_names():
    return [item["name"] for item in CAMPUS_CONFIG]


def get_location_queries():
    return [item["query"] for item in CAMPUS_CONFIG]


def geocode_place(query: str, api_key: str, language: str = "tr"):
    """Google Geocoding ile tek sorgunun lat,lng'sini döndürür. Hata durumunda default döner."""
    if not api_key:
        # API yoksa default döndür
        return DEFAULT_COORD

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": query, "key": api_key, "language": language}

    try:
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
    except Exception:
        return DEFAULT_COORD

    if data.get("status") != "OK" or not data.get("results"):
        return DEFAULT_COORD

    loc = data["results"][0]["geometry"]["location"]
    return float(loc.get("lat", DEFAULT_COORD[0])), float(loc.get("lng", DEFAULT_COORD[1]))


def fetch_and_store_coordinates(api_key: str = None, force: bool = False):
    """
    CAMPUS_CONFIG içine 'lat' ve 'lng' ekler.
    - api_key varsa Geocoding kullanır,
    - yoksa veya hata olursa DEFAULT_COORD atar.
    - force=True ise var olan lat/lng değerlerini yeniden yazar.
    """
    for item in CAMPUS_CONFIG:
        if not force and ("lat" in item and "lng" in item and item["lat"] is not None and item["lng"] is not None):
            continue
        lat, lng = geocode_place(item["query"], api_key)
        item["lat"] = lat
        item["lng"] = lng


def parse_coordinates():
    """
    CAMPUS_CONFIG'ten (lat,lng) tuple listesi döndürür.
    Kesinlikle None içermez; eksik durumda DEFAULT_COORD kullanır.
    """
    coords = []
    for item in CAMPUS_CONFIG:
        lat = item.get("lat")
        lng = item.get("lng")
        if lat is None or lng is None:
            coords.append(DEFAULT_COORD)
        else:
            coords.append((float(lat), float(lng)))
    return coords
