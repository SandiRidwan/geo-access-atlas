-- transform.sql — STAGING → MARTS (logika analitik, SQL murni).
--
-- TANTANGAN: judul variabel BPS TIDAK SERAGAM antar provinsi
-- (mis. "[Metode Baru] Indeks Pembangunan Manusia Menurut Kabupaten/Kota",
--  "Persentase Penduduk Miskin Menurut Kabupaten/Kota", dst).
-- Solusi: KANONIKALISASI via pencocokan kata kunci judul (CASE LIKE).

-- ===========================================================================
-- 1. KEMISKINAN KANONIKAL per kabupaten-tahun
-- ===========================================================================
DELETE FROM mart_poverty;
INSERT INTO mart_poverty
WITH pov_pct AS (
    -- hanya variabel pokok (bukan sub-populasi spt 'usia 15 tahun ke atas')
    SELECT DISTINCT ON (wilayah_kode, year)
           wilayah_kode, wilayah_nama, year, value AS poverty_pct
    FROM stg_bps
    WHERE level = 'kabupaten'
      AND lower(variable) LIKE '%persentase penduduk miskin%'
      AND lower(variable) NOT LIKE '%klasifikasi%'
      AND lower(variable) NOT LIKE '%usia%'
      AND lower(variable) NOT LIKE '%pendidikan%'
    ORDER BY wilayah_kode, year, var_id
),
pov_cnt AS (
    SELECT DISTINCT ON (wilayah_kode, year)
           wilayah_kode, year, value AS poverty_count
    FROM stg_bps
    WHERE level = 'kabupaten'
      AND lower(variable) LIKE '%jumlah penduduk miskin%'
      AND lower(variable) NOT LIKE '%klasifikasi%'
      AND lower(variable) NOT LIKE '%usia%'
    ORDER BY wilayah_kode, year, var_id
),
joined AS (
    SELECT p.wilayah_kode AS kode_bps,
           p.wilayah_nama,
           p.year,
           p.poverty_pct,
           c.poverty_count
    FROM pov_pct p
    LEFT JOIN pov_cnt c
      ON p.wilayah_kode = c.wilayah_kode AND p.year = c.year
)
SELECT
    j.kode_bps,
    j.wilayah_nama,
    k.nama_prov,
    j.year,
    j.poverty_pct,
    j.poverty_count,
    k.area_km2,
    k.centroid_lat,
    k.centroid_lon
FROM joined j
INNER JOIN stg_kabupaten k ON j.kode_bps = k.kode_bps;

-- ===========================================================================
-- 2. IPM KANONIKAL per kabupaten-tahun
-- ===========================================================================
DELETE FROM mart_ipm;
INSERT INTO mart_ipm
SELECT DISTINCT ON (s.wilayah_kode, s.year)
    s.wilayah_kode AS kode_bps,
    s.wilayah_nama,
    k.nama_prov,
    s.year,
    s.value AS ipm
FROM stg_bps s
INNER JOIN stg_kabupaten k ON s.wilayah_kode = k.kode_bps
WHERE s.level = 'kabupaten'
  AND lower(s.variable) LIKE '%indeks pembangunan manusia%'
  AND lower(s.variable) LIKE '%kabupaten%'
  AND lower(s.variable) NOT LIKE '%komponen%'
  AND lower(s.variable) NOT LIKE '%jenis kelamin%'
  AND s.value IS NOT NULL
ORDER BY s.wilayah_kode, s.year, s.var_id;

-- ===========================================================================
-- 3. PROFIL KABUPATEN TERBARU (untuk peta)
-- ===========================================================================
DELETE FROM mart_kabupaten_profile;
INSERT INTO mart_kabupaten_profile
WITH latest_pov AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY kode_bps ORDER BY year DESC) rn
    FROM mart_poverty
),
latest_ipm AS (
    SELECT kode_bps, year AS ipm_year, ipm,
           ROW_NUMBER() OVER (PARTITION BY kode_bps ORDER BY year DESC) rn
    FROM mart_ipm
),
base AS (
    SELECT kode_bps, wilayah_nama, nama_prov, year, poverty_pct,
           area_km2, centroid_lat, centroid_lon
    FROM latest_pov WHERE rn = 1
)
SELECT
    b.kode_bps,
    b.wilayah_nama,
    b.nama_prov,
    b.year,
    b.poverty_pct,
    i.ipm,
    b.area_km2,
    b.centroid_lat,
    b.centroid_lon,
    RANK() OVER (ORDER BY b.poverty_pct ASC) AS rank_poverty,
    CASE
        WHEN b.poverty_pct < 5  THEN 'rendah'
        WHEN b.poverty_pct < 10 THEN 'sedang'
        WHEN b.poverty_pct < 20 THEN 'tinggi'
        ELSE 'sangat tinggi'
    END AS poverty_band
FROM base b
LEFT JOIN latest_ipm i ON b.kode_bps = i.kode_bps AND i.rn = 1;

-- ===========================================================================
-- 4. RINGKASAN PER PROVINSI
-- ===========================================================================
DELETE FROM mart_province_summary;
INSERT INTO mart_province_summary
SELECT
    nama_prov,
    count(DISTINCT kode_bps)                AS n_kabupaten,
    round(median(poverty_pct), 2)           AS poverty_pct_median,
    round(max(poverty_pct), 2)              AS poverty_pct_max,
    round(min(poverty_pct), 2)              AS poverty_pct_min,
    round(sum(area_km2), 0)                 AS total_area_km2
FROM mart_kabupaten_profile
GROUP BY nama_prov;
