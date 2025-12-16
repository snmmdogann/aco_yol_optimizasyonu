# Kampüs Ring Otobüsü Optimizasyonu (ACO)

## Senaryo 7 – Üniversite Kampüsünde Ring Seferi Optimizasyonu

Bu projede, üniversite kampüsü içinde ring seferi yapan bir otobüsün;
fakülteler, öğrenci yurtları ve spor tesisleri gibi **10 duraktan**
geçerek **en kısa mesafe ile tur atması** hedeflenmiştir.

Problem, **Gezgin Satıcı Problemi (TSP)** olarak modellenmiş ve
**Karınca Kolonisi Optimizasyonu (Ant Colony Optimization – ACO)**
algoritması kullanılarak çözülmüştür.

---

## Kullanılan Teknolojiler

- Python
- Google Maps Geocoding API
- Haversine mesafe formülü
- Ant Colony Optimization (ACO)
- Streamlit
- Folium (harita görselleştirme)
- Matplotlib (grafikler)

---

## Yöntem

### 1. Durakların Belirlenmesi
Kampüs içindeki 10 farklı durak (fakülteler, yurtlar ve sosyal alanlar)
adres bilgileriyle tanımlanmıştır.

### 2. Koordinatların Alınması
Durakların enlem-boylam bilgileri **Google Geocoding API**
kullanılarak dinamik olarak elde edilmiştir.

> Not: Statik (elle girilmiş) koordinat kullanılmamıştır.

### 3. Mesafe Matrisi
Duraklar arası mesafeler, **Haversine formülü** kullanılarak
hesaplanmıştır. Bu yöntem, Google Distance Matrix API’nin
kota ve hız sınırlamalarından etkilenmemek amacıyla tercih edilmiştir.

### 4. Karınca Kolonisi Optimizasyonu
ACO algoritması kullanılarak en kısa ring rotası bulunmuştur.
Algoritmada aşağıdaki parametreler kullanılmıştır:
- Karınca sayısı
- İterasyon sayısı
- Alpha (feromon etkisi)
- Beta (mesafe etkisi)
- Buharlaşma oranı

### 5. Görselleştirme
- En kısa rota, **Folium** kullanılarak harita üzerinde gösterilmiştir.
- Algoritmanın yakınsama davranışı, iterasyonlara göre mesafe grafiği ile sunulmuştur.

---

## Çalıştırma

Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
timizasyonu
