<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00C6FF,50:3F51B5,100:F7971E&height=180&section=header&text=Hackhaton&fontSize=54&fontColor=FFFFFF&animation=twinkling" />
  <h3>Su, iklim ve baraj analitigi calisma alani</h3>
  <p>Arastirma, modelleme ve karar destek panelleri bir arada.</p>
  <p><strong>Not:</strong> Bu calisma Kandilli Rasathanesi ve Bogazici Universitesi Bilgisayar Hackhatonu icin yapilmistir.</p>
  <p>
    <img src="https://img.shields.io/badge/Odak-Climate%20%26%20Water-00BCD4" />
    <img src="https://img.shields.io/badge/Stack-Python%20%2B%20JS-1E88E5" />
    <img src="https://img.shields.io/badge/Ciktilar-Reports%20%26%20Charts-F4511E" />
    <img src="https://img.shields.io/badge/Data-Ignored%20in%20Git-8E24AA" />
  </p>
</div>

---

## Hizli harita
```text
Hackhaton/
|-- dashboard/                      # Paneller icin frontend + server
|-- scripts/                        # Modelleme, veri hazirlama ve analiz akislari
|-- research/                       # Arastirma hub, loglar ve template'ler
|-- baraj_web/                      # Statik web sunumu
|-- external/ArtikongrafConverter/  # Harici arac (entegre)
|-- index.html                      # Legacy web sunumu (kok)
|-- assets/                         # Legacy web sunumu asset'leri
|-- styles.css                      # Legacy web sunumu stil dosyasi
|-- netlify.toml                    # Legacy web sunumu deploy ayari
|-- hackhaton_model_kartlari_2026_03_18/  # Model kartlari (gorsel)
|-- hackhaton_projection_2040_2026_03_18/ # Projeksiyon gorselleri
|-- ADVERSARIAL_TEST/               # Test goruntuleri (git disi)
|-- DESKTOP_PROCESSING/             # Yerel isleme ciktilari (git disi)
|-- DATA/                           # Yerel veri setleri (git disi)
|-- new data/                       # Yerel veri setleri (git disi)
|-- output/                         # Uretilen ciktilar (git disi)
|-- tmp/                            # Gecici dosyalar (git disi)
|-- baraj_web/assets/data/          # Uretilen veri (git disi)
```

## Icerik ozeti
- Baraj doluluk, ET0 ve iklim sinyalleri icin uctan uca modelleme scriptleri
- Karar destek dashboard'lari ve anomaly news gorunumleri
- Log, template ve sentez notlari ile arastirma hub yapisi
- Model kartlari ve projeksiyon gorselleri

## Web sunumu
- Tercih edilen sunum: `baraj_web/index.html`
- Legacy sunum (kok dizin): `index.html`
- Basit statik sunucu icin:
```bash
cd baraj_web
python -m http.server 8000
```
Sonra `http://localhost:8000`.

## Rapor ve ET0 yeniden uretim
### PDF raporlar
```bash
python scripts/build_istanbul_current_status_pdf.py
python scripts/build_istanbul_current_status_detailed_pdf.py
python scripts/build_hackathon_final_pdf_report.py
```

### ET0 paket (gercek radyasyon)
```bash
python scripts/build_es_ea_newdata_csv.py \
  --temp-xlsx "<TEMP_XLSX>" \
  --humidity-xlsx "<HUMIDITY_XLSX>" \
  --auto-table1 "<AUTO_TABLE1>" \
  --auto-table2 "<AUTO_TABLE2>"

python scripts/build_complete_solar_dataset.py
python scripts/build_tarim_et0_real_radiation_package.py
python scripts/build_et0_formula_card.py
python scripts/build_one_year_explained_et0_charts.py --year 2004
python scripts/build_et0_trend_robust_chart.py
python scripts/build_et0_multiscale_charts.py
```

## Veri notu
Veri setleri bilerek git disinda tutulur. Yerel verileri su dizinlere koy:
- `DATA/`
- `new data/`
- `baraj_web/assets/data/`

Yaygin veri formatlari (ornegin `*.csv`, `*.parquet`, `*.xlsx`, `*.pkl`) `.gitignore` ile disarida tutulur.

## Veri kaynaklari (ozet)
- IBB/ISKI baraj doluluk ve havza yagisi
- IBB tuketim verileri
- Kandilli uzun donem iklim serileri
- Iklim projeksiyonlari (2026-2040)

## Repo notu
- Onceki alt repolar birlestirildi. Eski git metadata yedekleri yerel olarak `.git_backup/` altinda saklanir ve git disindadir.

## Konvansiyonlar
- Buyuk binary ve uretilen ciktilari git disinda tut
- Yeni pipeline'lar icin `scripts/` altina kisa not ekle

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:3F51B5,100:00C6FF&height=16&section=footer" />
</div>
