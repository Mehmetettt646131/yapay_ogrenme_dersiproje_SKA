# yapay_ogrenme_dersiproje_SKA
Yapay Öğrenme ile Sürdürülebilir Kalkınma Planlaması
🌍 Yapay Öğrenme ile Türkiye Karbon Emisyon (CO2) Tahmini
Ders: Yapay Öğrenmenin Temelleri
Konu: BM Sürdürülebilir Kalkınma Amaçları (SKA 13 - İklim Eylemi)
Model Başarısı (R^2): %98.53

📌 Proje Hakkında
Bu proje, Birleşmiş Milletler Sürdürülebilir Kalkınma Amaçları (SDG) kapsamında belirlenen "İklim Eylemi" hedefini temel alarak, Türkiye'nin karbon emisyonlarını (CO2) etkileyen faktörleri analiz etmek ve geleceğe yönelik tahminlerde bulunmak amacıyla geliştirilmiştir.

Projede, Türkiye'nin 1990-2023 yılları arasındaki makroekonomik verileri kullanılarak, ekonomik büyüme ve enerji tüketiminin çevresel etkileri Makine Öğrenmesi (Linear Regression) yöntemiyle modellenmiştir.

 Veri Seti ve Kaynaklar
 Veriler Dünya Bankası (World Bank Open Data) portalından çekilmiş ve proje kapsamında temizlenerek kullanılmıştır.Bağımlı Değişken ($y$): Kişi Başına Karbon Emisyonu (Metric tons per capita) - co2_data.csvBağımsız Değişken 1 (X_1): Kişi Başına GSYİH (GDP - Current US$) - gdp_data.csvBağımsız Değişken 2(X_2): Kişi Başına Enerji Kullanımı (kg of oil equivalent) - energy_data.csv

 ⚙️ Kurulum ve Çalıştırma
 Gerekli Kütüphaneleri Yükleyin:pip install pandas numpy matplotlib seaborn scikit-learn

 🚀 Kullanılan Yöntem ve Algoritma
Projede Denetimli Öğrenme (Supervised Learning) tekniklerinden Çoklu Doğrusal Regresyon (Multiple Linear Regression) algoritması kullanılmıştır.

Eğitim/Test Ayrımı: Verisetinin %80'i eğitim, %20'si test olarak ayrılmıştır.

Kütüphaneler: Pandas (Veri İşleme), Scikit-Learn (Modelleme), Matplotlib/Seaborn (Görselleştirme).
