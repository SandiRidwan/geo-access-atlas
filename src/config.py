"""
config.py — satu sumber kebenaran: path, sumber, kredensial, konstanta.

Project: Indonesia Poverty & Access Atlas
Sumber (semua resmi/terbuka):
  · BPS WebAPI      — kemiskinan & IPM per kabupaten/kota (2010–2025)
  · GADM 4.1        — batas wilayah kabupaten/kota (CC_2 = kode BPS)
  · OpenStreetMap   — fasilitas publik (rumah sakit, sekolah) via Overpass
"""

from __future__ import annotations

import os
from pathlib import Path

# ---- Path -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
STAGING = DATA / "staging"
MARTS = DATA / "marts"
DB = ROOT / "db"
SQL = ROOT / "sql"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"

for _p in (RAW, STAGING, MARTS, DB, REPORTS, FIGURES):
    _p.mkdir(parents=True, exist_ok=True)

DB_FILE = DB / "poverty.duckdb"


# ---- Kredensial (dari .env, JANGAN hardcode) -------------------------------
def _load_env() -> None:
    """Muat .env sederhana (tanpa dependensi) bila ada."""
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()
BPS_API_KEY = os.environ.get("BPS_API_KEY", "")
BPS_BASE = "https://webapi.bps.go.id/v1/api"

# ---- Sumber geospasial -----------------------------------------------------
GADM_ADM2_URL = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IDN_2.json"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# ---- BPS: indikator yang ditarik -------------------------------------------
# sub_id BPS:
#   23 = Kemiskinan dan Ketimpangan
#   26 = Indeks Pembangunan Manusia
BPS_SUBJECTS = {
    23: "Kemiskinan dan Ketimpangan",
    26: "Indeks Pembangunan Manusia",
}

# Tahun BPS (kode th → label). 125 = 2025 (terbaru).
BPS_YEARS = {120: 2020, 121: 2021, 122: 2022, 123: 2023, 124: 2024, 125: 2025}

# Judul variabel yang ingin ditarik (dicocokkan per-domain karena var_id
# BERBEDA tiap provinsi — temuan penting saat verifikasi).
TARGET_VARS = [
    "Persentase Penduduk Miskin",
    "Jumlah Penduduk Miskin",
    "Indeks Pembangunan Manusia",
    "Garis Kemiskinan",
    "Umur Harapan Hidup",
    "Rata-rata Lama Sekolah",
]

# ---- Fasilitas OSM ---------------------------------------------------------
FACILITIES = {
    "hospital": ("amenity", "hospital"),
    "school": ("amenity", "school"),
    "market": ("amenity", "marketplace"),
}

# ---- Palet warna -----------------------------------------------------------
COLORS = {
    "primary": "#1F5C3D", "accent": "#E4A11B", "dark": "#1B2A33",
    "grey": "#8B9AA6", "red": "#C0392B", "blue": "#2E6F95",
    "purple": "#6A4C93", "teal": "#2A9D8F",
}
SERIES = ["#1F5C3D", "#2E6F95", "#E4A11B", "#C0392B", "#6A4C93",
          "#2A9D8F", "#E76F51", "#264653"]
