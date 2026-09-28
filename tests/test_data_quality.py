"""
test_data_quality.py — uji kualitas data (CI-friendly, exit != 0 bila gagal).

Kelompok uji:
  · Keunikan  · Kelengkapan  · Rentang  · Konsistensi  · Kesegaran  · Cakupan
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import duckdb

from config import DB_FILE

FAILS: list[str] = []
PASSES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSES.append(name)
        print(f"  PASS  {name}")
    else:
        FAILS.append(f"{name} — {detail}")
        print(f"  FAIL  {name}  {detail}")


def main() -> int:
    con = duckdb.connect(str(DB_FILE), read_only=True)
    print("[dq] uji kualitas data\n")

    # ---- Keunikan --------------------------------------------------------
    n = con.execute("SELECT count(*) FROM stg_kabupaten").fetchone()[0]
    u = con.execute("SELECT count(DISTINCT kode_bps) FROM stg_kabupaten").fetchone()[0]
    check("stg_kabupaten kode_bps unik", n == u, f"{n} vs {u}")

    n = con.execute("SELECT count(*) FROM mart_kabupaten_profile").fetchone()[0]
    u = con.execute("SELECT count(DISTINCT kode_bps) FROM mart_kabupaten_profile").fetchone()[0]
    check("profil kabupaten unik", n == u, f"{n} vs {u}")

    n = con.execute("SELECT count(*) FROM mart_poverty").fetchone()[0]
    u = con.execute("""SELECT count(*) FROM (SELECT DISTINCT kode_bps, year
                      FROM mart_poverty)""").fetchone()[0]
    check("mart_poverty PK unik", n == u, f"{n} vs {u}")

    # ---- Kelengkapan -----------------------------------------------------
    null_geo = con.execute("SELECT count(*) FROM stg_kabupaten WHERE kode_bps IS NULL").fetchone()[0]
    check("kode_bps tidak null", null_geo == 0, f"{null_geo} null")

    null_pov = con.execute("SELECT count(*) FROM mart_kabupaten_profile WHERE poverty_pct IS NULL").fetchone()[0]
    check("kemiskinan terisi di profil", null_pov == 0, f"{null_pov} null")

    # ---- Rentang ---------------------------------------------------------
    bad = con.execute("""SELECT count(*) FROM mart_kabupaten_profile
        WHERE poverty_pct < 0 OR poverty_pct > 100""").fetchone()[0]
    check("kemiskinan 0–100%", bad == 0, f"{bad} di luar rentang")

    bad = con.execute("""SELECT count(*) FROM mart_ipm
        WHERE ipm < 0 OR ipm > 100""").fetchone()[0]
    check("IPM 0–100", bad == 0, f"{bad} di luar rentang")

    bad = con.execute("""SELECT count(*) FROM stg_kabupaten
        WHERE area_km2 IS NOT NULL AND area_km2 <= 0""").fetchone()[0]
    check("luas area > 0", bad == 0, f"{bad} non-positif")

    # ---- Konsistensi -----------------------------------------------------
    bad = con.execute("""SELECT count(*) FROM mart_kabupaten_profile
        WHERE rank_poverty IS NULL OR poverty_band IS NULL""").fetchone()[0]
    check("peringkat & band terisi", bad == 0, f"{bad} kosong")

    bad = con.execute("""SELECT count(*) FROM mart_kabupaten_profile
        WHERE (poverty_pct < 5 AND poverty_band <> 'rendah')
           OR (poverty_pct >= 5 AND poverty_pct < 10 AND poverty_band <> 'sedang')
           OR (poverty_pct >= 10 AND poverty_pct < 20 AND poverty_band <> 'tinggi')
           OR (poverty_pct >= 20 AND poverty_band <> 'sangat tinggi')""").fetchone()[0]
    check("band konsisten dgn ambang", bad == 0, f"{bad} salah band")

    orphan = con.execute("""SELECT count(*) FROM mart_poverty p
        LEFT JOIN stg_kabupaten k ON p.kode_bps = k.kode_bps
        WHERE k.kode_bps IS NULL""").fetchone()[0]
    check("poverty referensial ke geometri", orphan == 0, f"{orphan} orphan")

    # ---- Kesegaran -------------------------------------------------------
    maxy = con.execute("SELECT max(year) FROM mart_kabupaten_profile").fetchone()[0]
    check("data segar (>= 2023)", maxy is not None and maxy >= 2023,
          f"tahun max = {maxy}")

    # ---- Cakupan (dilaporkan, ambang longgar & jujur) --------------------
    n_kab = con.execute("SELECT count(*) FROM mart_kabupaten_profile").fetchone()[0]
    check("cakupan kabupaten wajar (>= 200)", n_kab >= 200, f"hanya {n_kab}")
    print(f"  INFO  cakupan profil: {n_kab} kabupaten "
          f"(BPS tahun-terbaru yg tersedia; bukan seluruh 514)")

    prov = con.execute("SELECT count(*) FROM mart_province_summary").fetchone()[0]
    check("provinsi terwakili (>= 10)", prov >= 10, f"hanya {prov}")
    print(f"  INFO  provinsi terwakili: {prov}")

    con.close()
    print(f"\n[dq] {len(PASSES)} lulus, {len(FAILS)} gagal")
    if FAILS:
        print("\nGAGAL:")
        for f in FAILS:
            print("  -", f)
        return 1
    print("[dq] SEMUA UJI LULUS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
