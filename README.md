# bayesian-offensive-index-model
Premier League offensive index model using Bayesian Shrinkage and Z-Score normalization.
# Bayesian Offensive Index Model (Bayesci Hücum Üretim Endeksi)

## 🇬🇧 Project Overview
This project is a mathematical modeling study designed to solve the "Small Sample Size Bias" frequently encountered in football analytics. Standard Per-90 metrics can unfairly reward players with limited playing time. This model regresses player data to the league average using Bayesian Shrinkage and standardizes it with Z-Scores to create a fair and robust "Offensive Production Index."

## 🇹🇷 Proje Özeti
Bu proje, futbol analitiğinde sıkça karşılaşılan "Küçük Örneklem Sapması" problemini çözmek amacıyla geliştirilmiş matematiksel bir modelleme çalışmasıdır. Standart Per-90 metrikleri, az süre alan oyuncuları haksız yere ödüllendirebilmektedir. Bu model; oyuncu verilerini Bayesci Küçültme (Bayesian Shrinkage) yöntemiyle lig ortalamasına regrese eder (çeker) ve Z-Skoru ile standartlaştırarak adil bir "Hücum Üretim Endeksi" oluşturur.

---

## 🇬🇧 Methodology / 🇹🇷 Metodoloji

* **Data Wrangling (Veri Temizleme ve Düzenleme):** 
  * *EN:* Hierarchical (MultiIndex) data fetched via `soccerdata` from FBref was flattened, and logical data cleaning was applied. 
  * *TR:* FBref üzerinden `soccerdata` ile çekilen karmaşık (MultiIndex) veriler düzleştirilmiş ve mantıksal veri temizliği yapılmıştır.

* **Bayesian Shrinkage (Bayesci Daraltma/Küçültme):** 
  * *EN:* The algorithm uses a confidence parameter of K=900 minutes (prior) to verify the statistical validity of players. 
  * *TR:* Algoritma, K=900 dakikalık bir güven parametresi kurgulayarak az süre alan oyuncuların istatistiksel sapmalarını dengeler.

* **Z-Score Normalization (Z-Skoru Standartlaştırması):** 
  * *EN:* Metrics in different units (e.g., shot accuracy percentage vs. goals per 90) were brought to the same scale (Z-Score) to be aggregated into an equally weighted index. 
  * *TR:* Farklı birimlerdeki veriler (şut isabet yüzdesi ve maç başı gol oranları gibi) aynı düzleme (Z-Skoru) çekilerek eşit ağırlıklı bir endekste toplanmıştır.

---
> **Note / Not:** 
> *EN:* The mathematical architecture, logical boundaries, and statistical filtering of the model belong entirely to me; AI was utilized strictly as a coding assistant for the Python pipeline setup.
> *TR:* Modelin matematiksel kurgusu, mantıksal sınırlandırmaları ve istatistiksel filtrelemesi tamamen şahsıma aittir; Python kodlama aşamasında süreci hızlandırmak için yapay zekadan asistan olarak faydalanılmıştır.
