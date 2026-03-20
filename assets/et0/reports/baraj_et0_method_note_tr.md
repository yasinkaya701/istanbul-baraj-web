# Baraj ET0 Calismasi - Yontem ve Veri Kaynagi

## 1. Bu calismada ne yaptik?

Bu calismada baraj sistemi icin `referans evapotranspirasyon (ET0)` serisini iklim panelinden alip ozetledik. Bu rapor ET0 degerlerini yeniden hesaplamaz; amacimiz, simulasiyonlarda tek ve tutarli bir ET0 kaynagi kullanmaktir.

## 2. ET0 nedir?

ET0, iyi sulanmis referans bir yuzey icin atmosferik buharlasma talebini temsil eder. Acik su yuzeyi buharlasmayla ayni degildir; baraj su dengesi icin ET0 genellikle bir katsayi ile olceklenir.

## 3. Veri kaynagi ve kapsama

- Veri dosyasi: `assets/data/climate_baseline.js`
- Gozlem donemi: `2010-01` -> `2024-12`
- Projeksiyon donemi: `2026-01` -> `2040-12`
- Not: 2025 yili panelde bulunmuyor; projeksiyon 2026'dan basliyor.

## 4. Hesaplama adimlari

1. Aylik ET0 degerleri panelden dogrudan alindi.
2. Yillik toplam ET0, 12 aylik degerlerin toplami ile hesaplandi.
3. Trend, 2010-2024 yillik toplamlar uzerinde basit dogrusal regresyonla hesaplandi.
4. Baz donem ortalamasi `2015-2024`, karsilastirma ortalamasi `2031-2035` olarak alindi.

## 5. Neden bu yaklasim?

- Repoda surekli, gunluk meteoroloji ve radyasyon serisi bulunmuyor.
- Iklim paneli aylik ET0'yu zaten tutarli bir sekilde sagliyor.
- Simulasyon ve raporlama icin tek kaynak kullanmak modeli daha savunulabilir yapiyor.

## 6. Sinirlar

- Aylik zaman adimi kullaniliyor; gunluk ET0 ayrinti seviyesi yok.
- Projeksiyonlar panelin varsayimlarina bagli.
- ET0, acik su buharlasma miktarini dogrudan vermez.

## 7. Bu paketin sayisal ozeti

- Gozlem yillari: `2010-2024` (15 yil)
- Ortalama yillik ET0: `1097.6 mm/yil`
- Trend: `+24.5 mm / 10 yil`
- Baz donem (2015-2024) ortalamasi: `1099.6 mm/yil`
- 2031-2035 ortalamasi: `1155.7 mm/yil`
- Beklenen fark: `+56.1 mm/yil`

## 8. Bir sonraki mantikli adimlar

1. Ham meteoroloji verisi gelirse FAO-56 ile ET0'yu yeniden hesaplamak
2. Acik su buharlasma katsayisini (E = K * ET0) kalibre etmek
3. Belirsizlik ve duyarlilik analizini rapora eklemek
