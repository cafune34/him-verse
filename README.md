# HİM-VERSE | FET445 Veri Madenciliği

Health Profile Discovery and Multimorbidity Analysis Using BRFSS 2025

**Durum:** Proje önerisi; gerçek veri ile model sonuçları henüz üretilmedi.

## Araştırma sorusu
Demografik özellikler, yaşam tarzı ve sağlık hizmetlerine erişim bilgileri, dört seçili kronik hastalık grubundan en az ikisini bildiren bireyleri ayırt edebilir mi?

Ana rota: ikili sınıflandırma. DummyClassifier, lojistik regresyon, karar ağacı ve Random Forest karşılaştırılacak. Ortak tabakalı %80/%20 eğitim-test ayrımı, 5 katlı CV, AP ile model seçimi ve eğitim dışı kat tahminleri ile eşik seçimi kullanılacak. Test yalnızca sonunda açılacak.

## Veri doğrulaması
1. [CDC BRFSS 2025](https://www.cdc.gov/brfss/annual_data/annual_2025.html) üzerinden yıllık XPT ZIP dosyasını ve kod kitabını edin.
2. ZIP dosyasını yerelde aç. Kod kitabından hedef değişkenlerin kodlarını doğrula.
3. `python -m pip install pandas`
4. `python scripts/validate_target.py data/raw/LLCP2025.XPT` (gerçek dosya adını kullan).

Hedef dört hastalık grubunun en az ikisinin bildirilmesi; kalp krizi ve koroner kalp hastalığı tek grup. Gebelik diyabeti ve prediyabet pozitif değil. Hedefi belirsiz kayıtlar dışlanacak. Ham veri ve öğrenci bilgileri herkese açık depoya yüklenmemeli.
