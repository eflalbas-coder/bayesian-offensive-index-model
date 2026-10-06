import pandas as pd
import numpy as np
import soccerdata as sd

print("Gerçek futbol verileri FBref üzerinden soccerdata ile çekiliyor...")

# 1. VERİ ÇEKME
fbref = sd.FBref(leagues='ENG-Premier League', seasons='2025')

df_standard = fbref.read_player_season_stats(stat_type='standard')
df_shooting = fbref.read_player_season_stats(stat_type='shooting')

# İndeksleri sıfırlayalım
df_standard = df_standard.reset_index()
df_shooting = df_shooting.reset_index()

# SÜTUN TEMİZLEME VE BENZERSİZ YAPma FONKSİYONU
def clean_columns(df):
    # Eğer MultiIndex ise katmanları birleştir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(c).strip() for c in col if str(c).strip() and 'unnamed' not in str(c).lower()]).strip() for col in df.columns]
    
    # Tüm sütunları küçük harfe çevir, boş olanları etiketle
    new_cols = []
    for i, col in enumerate(df.columns):
        c_str = str(col).lower().strip()
        if c_str == '' or c_str == 'nan':
            c_str = f'unnamed_{i}'
        new_cols.append(c_str)
    
    # Çakışan/Aynı olan sütun isimlerini benzersiz hale getir (ValueError önleyici)
    seen = {}
    unique_cols = []
    for c in new_cols:
        if c in seen:
            seen[c] += 1
            unique_cols.append(f"{c}_{seen[c]}")
        else:
            seen[c] = 0
            unique_cols.append(c)
            
    df.columns = unique_cols
    return df

df_standard = clean_columns(df_standard)
df_shooting = clean_columns(df_shooting)

# Oyuncu ve takım sütunlarını esnek bir şekilde bulalım
player_col = next((c for c in df_standard.columns if 'player' in c), df_standard.columns[0])
team_col = next((c for c in df_standard.columns if 'team' in c or 'squad' in c), 'team')

# İki tabloyu birleştirelim
df = pd.merge(df_standard, df_shooting, on=[player_col, team_col], how='inner', suffixes=('', '_shoot'))

# 2. SÜTUN İSİMLERİNİ KENDİ MODELİMİZE Uydurma
# Olası sütun adlarını esnek yakalamak için arama yapıyoruz
dakika_col = next((c for c in df.columns if 'min' in c and 'minus' not in c), None)
gol_col = next((c for c in df.columns if c == 'gls' or c == 'goals' or '_gls' in c), None)
asist_col = next((c for c in df.columns if c == 'ast' or c == 'assists' or '_ast' in c), None)
toplam_sut_col = next((c for c in df.columns if 'shots_standard' in c or 'sh_' in c or 'shots' in c), None)
isabetli_sut_col = next((c for c in df.columns if 'sot_standard' in c or 'sot' in c), None)

rename_dict = {
    player_col: 'oyuncu',
    team_col: 'team',
    dakika_col: 'dakika',
    gol_col: 'gol',
    asist_col: 'asist',
    toplam_sut_col: 'toplam_sut',
    isabetli_sut_col: 'isabetli_sut'
}
# Sadece veri çerçevesinde var olanları yeniden adlandıralım
df = df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns})

# Sayısal sütunların tip dönüşümleri ve güvenlik kontrolleri
for col in ['dakika', 'gol', 'asist', 'toplam_sut', 'isabetli_sut']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        df[col] = 0

# Çok az süre almış oyuncuları eleyelim (Örn: 300 dakika altı)
df = df[df['dakika'] > 300].copy()

# Mantıksal hata kontrolü
df["isabetli_sut"] = np.minimum(df["isabetli_sut"], df["toplam_sut"])

# 3. PER 90 (MAÇ BAŞI) DÖNÜŞÜMLERİ
df["sut_isabet_orani"] = np.where(df["toplam_sut"] > 0, df["isabetli_sut"] / df["toplam_sut"], 0)
df["gol_p90"] = (df["gol"] / df["dakika"]) * 90
df["asist_p90"] = (df["asist"] / df["dakika"]) * 90

# 4. BAYESCI KÜÇÜLTME (BAYESIAN SHRINKAGE)
K = 900
df["guven_agirligi"] = df["dakika"] / (df["dakika"] + K)

ham_metrikler = ["sut_isabet_orani", "gol_p90", "asist_p90"]

for m in ham_metrikler:
    lig_ortalamasi = df[m].mean()
    df[m + "_shrunk"] = (df["guven_agirligi"] * df[m]) + ((1 - df["guven_agirligi"]) * lig_ortalamasi)

# 5. Z-SKORU İLE STANDARTLAŞTIRMA
z_metrikler = [m + "_shrunk" for m in ham_metrikler]

for m in z_metrikler:
    mean_val = df[m].mean()
    std_val = df[m].std()
    if std_val > 0:
        df[m + "_z"] = (df[m] - mean_val) / std_val
    else:
        df[m + "_z"] = 0

# 6. ENDEKSİN HESAPLANMASI VE SIRALAMA
df["hucum_uretim_endeksi"] = (
    df["sut_isabet_orani_shrunk_z"] + 
    df["gol_p90_shrunk_z"] + 
    df["asist_p90_shrunk_z"]
)

sonuc = df[["oyuncu", "team", "dakika", "gol", "asist", "hucum_uretim_endeksi"]].sort_values(by="hucum_uretim_endeksi", ascending=False)

print("\n--- SOCCERDATA İLE GERÇEK PREMIER LİG HÜCUM İNDEKSİ ---")
print(sonuc.head(15).to_string(index=False))