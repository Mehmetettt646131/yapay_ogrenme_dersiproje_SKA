# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# --- AYARLAR ---
# Dosya isimlerini buraya yaz (indirdiginiz isimlerle ayni olsun)
DOSYA_CO2 = 'co2_data.csv'
DOSYA_GDP = 'gdp_data.csv'
DOSYA_ENERGY = 'energy_data.csv'
ULKE_KODU = 'TUR' # Turkiye'nin Dünya Bankasi kodu

def veriyi_hazirla():
    print("--- Veriler Yukleniyor ve Birlestiriliyor ---")
    
    # 1. Verileri Oku (Ilk 4 satir genelde aciklama olur, atliyoruz)
    try:
        df_co2 = pd.read_csv(DOSYA_CO2, skiprows=4)
        df_gdp = pd.read_csv(DOSYA_GDP, skiprows=4)
        df_energy = pd.read_csv(DOSYA_ENERGY, skiprows=4)
    except FileNotFoundError:
        print("HATA: CSV dosyalari bulunamadi! Dosya isimlerini kontrol et.")
        return None

    # 2. Sadece Turkiye Verisini Sec ve Gereksiz Sutunlari At
    def temizle(df, isim):
        df = df[df['Country Code'] == ULKE_KODU] # Sadece Turkiye
        # Yillar sutun (1960'tan 2023'e kadar olan sutunlar)
        df = df.melt(id_vars=['Country Name', 'Country Code'], 
                     var_name='Yil', value_name=isim)
        # Sadece sayisal yil ve veriyi al
        df['Yil'] = pd.to_numeric(df['Yil'], errors='coerce')
        df = df.dropna(subset=['Yil']) # Yil olmayanlari at
        return df[['Yil', isim]]

    co2_clean = temizle(df_co2, 'CO2_Emisyonu')
    gdp_clean = temizle(df_gdp, 'GDP_KisiBasi')
    energy_clean = temizle(df_energy, 'Enerji_Kullanimi')

    # 3. Hepsini Yil bazinda birlestir (Merge)
    ana_veri = pd.merge(gdp_clean, energy_clean, on='Yil', how='inner')
    ana_veri = pd.merge(ana_veri, co2_clean, on='Yil', how='inner')

    # 4. Eksik verileri temizle (Bos satir varsa atalım)
    print(f"Bilesen Veri Boyutu (Temizlemeden Once): {ana_veri.shape}")
    ana_veri = ana_veri.dropna()
    print(f"Son Veri Boyutu: {ana_veri.shape}")
    print(ana_veri.tail()) # Son 5 satiri goster
    
    return ana_veri

def model_egit(df):
    print("\n--- Model Egitiliyor ---")
    
    # Hedef (y) ve Nedenler (X)
    X = df[['GDP_KisiBasi', 'Enerji_Kullanimi']]
    y = df['CO2_Emisyonu']
    
    # Egitim - Test Ayrimi (%80 Egitim, %20 Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model 1: Lineer Regresyon (Basit, Anlasilir)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Tahminler
    tahminler = model.predict(X_test)
    
    # Basari Metrikleri
    r2 = r2_score(y_test, tahminler)
    rmse = np.sqrt(mean_squared_error(y_test, tahminler))
    
    print(f"Model Basarisi (R2): {r2:.4f} (1'e ne kadar yakinsa o kadar iyi)")
    print(f"Ortalama Hata (RMSE): {rmse:.4f}")
    
    # Gercek vs Tahmin Tablosu
    sonuc_df = pd.DataFrame({'Gercek': y_test, 'Tahmin': tahminler})
    print("\nOrnek Tahminler:")
    print(sonuc_df.head())
    
    return model

def gorsellestir(df, model):
    # 1. Yillara Gore Degisim Grafigi
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    sns.lineplot(x='Yil', y='CO2_Emisyonu', data=df, label='CO2', color='red')
    sns.lineplot(x='Yil', y='Enerji_Kullanimi', data=df, label='Enerji (Normalize)', color='blue') # Olcek farki olabilir dikkat
    plt.title('Yillara Gore CO2 Degisimi')
    plt.legend()

    # 2. Tahmin Grafigi (Gercek vs Tahmin)
    # Tum veri icin tahmin yaptiralim gorsel icin
    X_all = df[['GDP_KisiBasi', 'Enerji_Kullanimi']]
    df['Tahmin_CO2'] = model.predict(X_all)

    plt.subplot(1, 2, 2)
    plt.scatter(df['CO2_Emisyonu'], df['Tahmin_CO2'], color='green', alpha=0.6)
    plt.plot([df['CO2_Emisyonu'].min(), df['CO2_Emisyonu'].max()], 
             [df['CO2_Emisyonu'].min(), df['CO2_Emisyonu'].max()], 'k--', lw=2)
    plt.xlabel('Gercek Degerler')
    plt.ylabel('Tahmin Edilen')
    plt.title('Dogruluk Analizi')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    veri = veriyi_hazirla()
    if veri is not None:
        egitilen_model = model_egit(veri)
        gorsellestir(veri, egitilen_model)
        
        # Ekstra: Gelecek Tahmini Denemesi
        print("\n--- Senaryo Analizi ---")
        yeni_gdp = 15000 # Ornek: Kisi basi gelir 15000 dolar olursa
        yeni_enerji = 2000 # Enerji kullanimi artarsa
        tahmin = egitilen_model.predict([[yeni_gdp, yeni_enerji]])
        print(f"Senaryo: GDP={yeni_gdp}$, Enerji={yeni_enerji} -> Tahmini CO2: {tahmin[0]:.2f}")