-- schema.sql — Skema database (DuckDB).
-- Lapisan: staging (mentah) → marts (analitik siap-pakai).

-- ===========================================================================
-- STAGING
-- ===========================================================================
CREATE TABLE IF NOT EXISTS stg_bps (
    domain_id     VARCHAR NOT NULL,
    domain_name   VARCHAR NOT NULL,
    var_id        INTEGER NOT NULL,
    variable      VARCHAR NOT NULL,
    unit          VARCHAR,
    wilayah_kode  VARCHAR NOT NULL,      -- kode BPS (4 digit = kab, *99 = prov)
    wilayah_nama  VARCHAR NOT NULL,
    year          INTEGER NOT NULL,
    value         DOUBLE,
    level         VARCHAR NOT NULL       -- 'provinsi' | 'kabupaten'
);

CREATE TABLE IF NOT EXISTS stg_kabupaten (
    kode_bps     VARCHAR NOT NULL,       -- CC_2 dari GADM (kode BPS)
    nama_kab     VARCHAR NOT NULL,
    nama_prov    VARCHAR NOT NULL,
    tipe         VARCHAR,
    area_km2     DOUBLE,
    centroid_lat DOUBLE,
    centroid_lon DOUBLE,
    PRIMARY KEY (kode_bps)
);

-- ===========================================================================
-- MARTS
-- ===========================================================================

-- Kemiskinan per kabupaten per tahun (kanonikal).
CREATE TABLE IF NOT EXISTS mart_poverty (
    kode_bps       VARCHAR,
    wilayah_nama   VARCHAR,
    nama_prov      VARCHAR,
    year           INTEGER,
    poverty_pct    DOUBLE,               -- persentase penduduk miskin (P0)
    poverty_count  DOUBLE,               -- jumlah penduduk miskin (ribu jiwa)
    area_km2       DOUBLE,
    centroid_lat   DOUBLE,
    centroid_lon   DOUBLE,
    PRIMARY KEY (kode_bps, year)
);

-- IPM per kabupaten per tahun (bila tersedia).
CREATE TABLE IF NOT EXISTS mart_ipm (
    kode_bps     VARCHAR,
    wilayah_nama VARCHAR,
    nama_prov    VARCHAR,
    year         INTEGER,
    ipm          DOUBLE,
    PRIMARY KEY (kode_bps, year)
);

-- Profil kabupaten terbaru (satu baris per kabupaten) — untuk peta.
CREATE TABLE IF NOT EXISTS mart_kabupaten_profile (
    kode_bps      VARCHAR PRIMARY KEY,
    wilayah_nama  VARCHAR,
    nama_prov     VARCHAR,
    year          INTEGER,
    poverty_pct   DOUBLE,
    ipm           DOUBLE,
    area_km2      DOUBLE,
    centroid_lat  DOUBLE,
    centroid_lon  DOUBLE,
    rank_poverty  INTEGER,               -- 1 = kemiskinan terendah (terbaik)
    poverty_band  VARCHAR                -- 'rendah' | 'sedang' | 'tinggi' | 'sangat tinggi'
);

-- Ringkasan per provinsi (agregat dari kabupaten).
CREATE TABLE IF NOT EXISTS mart_province_summary (
    nama_prov          VARCHAR PRIMARY KEY,
    n_kabupaten        INTEGER,
    poverty_pct_median DOUBLE,
    poverty_pct_max    DOUBLE,
    poverty_pct_min    DOUBLE,
    total_area_km2     DOUBLE
);
