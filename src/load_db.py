"""
load_db.py — muat staging (Parquet) ke DuckDB. Idempoten.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb

from config import DB_FILE, SQL, STAGING


def main() -> None:
    con = duckdb.connect(str(DB_FILE))
    print(f"[load] database → {DB_FILE}")
    con.execute((SQL / "schema.sql").read_text(encoding="utf-8"))

    bps = STAGING / "bps_indicators.parquet"
    kab = STAGING / "kabupaten.parquet"

    n_bps = 0
    if bps.exists():
        con.execute("DELETE FROM stg_bps")
        con.execute(f"""
            INSERT INTO stg_bps
            SELECT domain_id, domain_name, var_id, variable, unit,
                   wilayah_kode, wilayah_nama, year, value, level
            FROM read_parquet('{bps.as_posix()}')
        """)
        n_bps = con.execute("SELECT count(*) FROM stg_bps").fetchone()[0]
    else:
        print("[load] staging BPS tidak ada — dilewati (opsional; butuh BPS_API_KEY)")

    n_kab = 0
    if kab.exists():
        con.execute("DELETE FROM stg_kabupaten")
        con.execute(f"""
            INSERT INTO stg_kabupaten
            SELECT kode_bps, nama_kab, nama_prov, tipe, area_km2,
                   centroid_lat, centroid_lon
            FROM read_parquet('{kab.as_posix()}')
        """)
        n_kab = con.execute("SELECT count(*) FROM stg_kabupaten").fetchone()[0]

    print(f"[load] stg_bps       : {n_bps} baris")
    print(f"[load] stg_kabupaten : {n_kab} baris")

    if n_bps:
        rows = con.execute("""
            SELECT level, count(DISTINCT wilayah_kode) AS wilayah,
                   min(year) AS y0, max(year) AS y1
            FROM stg_bps GROUP BY level ORDER BY level
        """).fetchall()
        print("[load] cakupan:")
        for r in rows:
            print(f"   {r[0]:10} {r[1]:4} wilayah  {r[2]}–{r[3]}")
    con.close()


if __name__ == "__main__":
    main()
