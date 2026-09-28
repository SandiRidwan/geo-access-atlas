# ADR — Architecture Decision Records

Catatan keputusan + **alasan jujur** (termasuk jalan buntu).

---

## ADR-001: Sumber data — BPS WebAPI (dengan kunci) + GADM + OSM

**Status:** Diputuskan
**Konteks:** Project geospasial butuh (a) batas wilayah, (b) indikator sosial,
(c) data fasilitas.

**Investigasi (fakta lapangan):**

| Sumber | Hasil uji | Status |
|---|---|---|
| BPS `webapi.bps.go.id` | **200** dgn `key` (user mendaftar) | ✅ dipakai |
| BPS halaman tabel biasa | 403 WAF | ❌ |
| GADM 4.1 ADM2 | 200, 502 kabupaten, ada `CC_2` (kode BPS) | ✅ dipakai |
| geoBoundaries ADM2 | 200 (2020, BPS) | alternatif |
| Overpass (OSM) | 200 (GET), live | ✅ dipakai (sebagian) |
| PIHPS Bank Indonesia (harga) | koneksi diputus | ❌ |
| data.go.id (portal) | 404 | ❌ |

**Keputusan:** BPS WebAPI (kunci dari `.env`), GADM 4.1, Overpass.
**Alasan:** resmi, terbaru (BPS sampai 2025), dan `CC_2` memungkinkan join.
**Konsekuensi:** butuh API key → **tidak 100% reproducible tanpa kredensial**.
Diminimalkan dengan: kunci di `.env` (tidak di-commit), dan `--no-ingest` agar
pipeline lain tetap jalan tanpa key.

> ⚠️ **Catatan keamanan:** kunci API **tidak pernah** ditulis di kode atau
> README. Ia dibaca dari `.env` yang di-`.gitignore`.

---

## ADR-002: Kanonikalisasi judul variabel BPS (temuan penting)

**Status:** Diputuskan
**Konteks:** `var_id` **BERBEDA antar provinsi** untuk konsep yang sama
(Temuan: "Persentase Penduduk Miskin" = `var_id 42` di Aceh, `36` di Lampung).
Judul pun bervariasi: `[Metode Baru] …`, `… SP2010`, `… SP2020`.

**Keputusan:** Tarik SEMUA variabel target per domain, lalu **kanonikalisasi
via pencocokan kata kunci** di SQL (`lower(variable) LIKE '%...%'`), dengan
pengecualian (buang `%klasifikasi%`, `%usia%`, `%pendidikan%`).
**Alasan:** tidak ada kode variabel universal di BPS; pencocokan judul adalah
satu-satunya cara menyatukan lintas 34 domain.
**Konsekuensi:** rentan bila BPS mengubah judul; uji data quality memverifikasi
hasilnya. Dicatat sebagai risiko.

---

## ADR-003: Cakupan tidak 100% — dilaporkan, bukan dipaksa

**Status:** Diputuskan
**Konteks:** (a) BPS tidak punya variabel kemiskinan di semua domain
(DKI, Bali, Kep. Babel = kosong). (b) GADM 4.1 (2022) belum memuat kabupaten
pemekaran 2022+. (c) `CC_2` GADM punya nilai `NA` untuk wilayah baru.

**Keputusan:** Laporkan cakupan apa adanya (mis. "270 kabupaten terpetakan dari
514"). Baris tanpa geometri **dibuang**, bukan diisi nol.
**Alasan:** nol ≠ tidak ada data. Menyembunyikan gap = analisis menyesatkan.
**Konsekuensi:** peta bolong; ini **fakta**, ditampilkan jujur di dashboard.

---

## ADR-004: DuckDB (embedded OLAP)

**Status:** Diputuskan
**Konteks:** Butuh database untuk join spasial-tabular & SQL analitik.
**Keputusan:** DuckDB (file tunggal, nol infra).
**Alasan:** portabel, SQL penuh (window, CTE), bisa dibaca pandas/geopandas.
**Konsekuensi:** tidak menunjukkan skill admin server; SQL transferable ke
PostgreSQL/BigQuery.

---

## ADR-005: Peta Folium di dalam Streamlit

**Status:** Diputuskan
**Konteks:** Butuh peta choropleth interaktif.
**Keputusan:** `folium` + `streamlit-folium` (Leaflet/OSM tiles).
**Alasan:** interaktif, gratis, tanpa token (bedakan dgn Mapbox/Google yang
butuh kunci). zoom/tooltip bawaan.
**Konsekuensi:** butuh `streamlit-folium`; jika bermasalah, alternatif
Plotly choropleth (tanpa peta dasar).
