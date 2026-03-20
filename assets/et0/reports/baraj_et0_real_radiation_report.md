# Baraj ET0 - Iklim Paneli Aylik Seri Paketi

## Veri Kaynagi

- Dosya: `assets/data/climate_baseline.js`
- Seri: `et0_mm_month` (aylik)
- Gozlem kapsami: `2010-01` -> `2024-12`
- Projeksiyon kapsami: `2026-01` -> `2040-12`
- Not: 2025 yili panelde yok; projeksiyon 2026'dan baslar.

## Kabuller

1. ET0 degerleri iklim panelinden hazir alindi; bu rapor ET0'yu yeniden hesaplamaz.
2. Yillik ET0, ilgili yildaki 12 ayin toplami olarak hesaplandi.
3. Trend, 2010-2024 yillik toplamlar uzerinde basit dogrusal regresyonla hesaplandi.

## Temel Bulgular

- Ortalama yillik ET0 (2010-2024): `1097.6 mm/yil`
- Yillik ET0 trendi (2010-2024): `+24.5 mm/10y`
- Min/Max yillik ET0 (2010-2024): `1044.1` - `1160.9 mm/yil`
- Baz donem (2015-2024) ortalama yillik ET0: `1099.6 mm/yil`
- 2031-2035 tahmin ortalamasi: `1155.7 mm/yil`
- Beklenen fark (2031-2035 - baz): `+56.1 mm/yil`

## Uretilen Ciktilar

- Ozet: `assets/et0/reports/baraj_et0_real_radiation_summary.json`
- Trend istatistikleri: `assets/et0/reports/baraj_et0_yearly_trend_stats.json`
- Grafikler: `assets/et0/*.png`
