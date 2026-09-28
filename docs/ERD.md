# ERD & Data Lineage

## Alur

```
 BPS WebAPI ─┐
 GADM 4.1 ───┼─► ingest_*.py ─► data/staging (Parquet + GeoJSON)
 OSM ────────┘        │
                      ▼
             load_db.py ─► DuckDB (staging + marts)
                      │
        sql/transform.sql (SQL murni) ─► marts
                      │
   ┌──────────────────┼───────────────────┐
   ▼                  ▼                   ▼
dashboard.py    make_charts.py   tests/test_data_quality.py
```

## ERD marts

```
   stg_kabupaten (495)            stg_bps (17.261)
   ╔════════════════╗             ╔══════════════════════╗
   ║ kode_bps (PK)  ║             ║ domain_id            ║
   ║ nama_kab       ║             ║ var_id / variable    ║
   ║ nama_prov      ║             ║ wilayah_kode         ║
   ║ tipe           ║             ║ level (prov|kab)     ║
   ║ area_km2       ║             ║ year, value          ║
   ║ centroid_lat   ║             ╚══════════╤═══════════╝
   ║ centroid_lon   ║                        │ kanonikalisasi
   ╚═══════╤════════╝                        │
           │ join kode_bps = wilayah_kode     ▼
           └──────────────►  mart_poverty (kode_bps, year)
                             mart_ipm     (kode_bps, year)
                                     │
                                     ▼  agregasi terbaru
                             mart_kabupaten_profile (1 baris/kabupaten)
                                     │
                                     ▼  agregasi provinsi
                             mart_province_summary
```

## Kanonikalisasi variabel (kunci)

| Konsep marts | Sumber judul BPS (LIKE) | Pengecualian |
|---|---|---|
| `poverty_pct` | `%persentase penduduk miskin%` | bukan `%klasifikasi%`, `%usia%`, `%pendidikan%` |
| `poverty_count` | `%jumlah penduduk miskin%` | bukan `%klasifikasi%`, `%usia%` |
| `ipm` | `%indeks pembangunan manusia%` + `%kabupaten%` | bukan `%komponen%`, `%jenis kelamin%` |

## Atribusi wilayah

- `kode_bps` = GADM `CC_2` = BPS `vervar` (4 digit).
- Provinsi: kode berakhiran `99` **atau** `00` (BPS memakai dua konvensi).
- Kabupaten/kota: kode lain.

## Sumber (publik)

| Sumber | URL | Peran |
|---|---|---|
| BPS WebAPI | `webapi.bps.go.id/v1/api` | kemiskinan, IPM (2020–2025) |
| GADM 4.1 | `geodata.ucdavis.edu/gadm/…/gadm41_IDN_2.json` | batas 502 kabupaten |
| OpenStreetMap | `overpass-api.de` | fasilitas (hospital, school, market) |
