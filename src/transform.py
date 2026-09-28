"""
transform.py — TRANSFORM: jalankan SQL marts & ekspor.

Staging (DuckDB) → marts (DuckDB) → Parquet/CSV.
Semua logika analitik di sql/transform.sql (SQL murni, dapat diaudit).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb

from config import DB_FILE, MARTS, SQL

MARTS_TABLES = [
    "mart_poverty",
    "mart_ipm",
    "mart_kabupaten_profile",
    "mart_province_summary",
]


def main() -> None:
    con = duckdb.connect(str(DB_FILE))
    print("[transform] menjalankan sql/transform.sql")
    con.execute((SQL / "transform.sql").read_text(encoding="utf-8"))

    print("[transform] marts:")
    for t in MARTS_TABLES:
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"   {t:28} {n:5} baris")
        con.execute(f"""COPY {t} TO '{(MARTS / (t + '.parquet')).as_posix()}'
                        (FORMAT PARQUET)""")

    print("\n[transform] 5 kabupaten termiskin (terbaru):")
    rows = con.execute("""
        SELECT wilayah_nama, nama_prov, year, ROUND(poverty_pct,2)
        FROM mart_kabupaten_profile ORDER BY poverty_pct DESC LIMIT 5
    """).fetchall()
    for r in rows:
        print(f"   {str(r[0])[:22]:22} {str(r[1])[:16]:16} {r[2]}  {r[3]}%")

    print("\n[transform] 5 provinsi termiskin (median kabupaten):")
    rows = con.execute("""
        SELECT nama_prov, n_kabupaten, poverty_pct_median
        FROM mart_province_summary ORDER BY poverty_pct_median DESC LIMIT 5
    """).fetchall()
    for r in rows:
        print(f"   {str(r[0])[:24]:24} {r[1]:3} kab  median {r[2]}%")

    cov = con.execute("""
        SELECT count(*) FROM mart_kabupaten_profile WHERE ipm IS NOT NULL
    """).fetchone()[0]
    print(f"\n[transform] kabupaten dengan IPM: {cov}")
    con.close()


if __name__ == "__main__":
    main()
