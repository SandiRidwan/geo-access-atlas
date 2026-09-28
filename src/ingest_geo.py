"""
ingest_geo.py — INGEST batas wilayah kabupaten/kota (GADM 4.1 ADM2).

Output:
  data/staging/kabupaten.geojson    — geometri 502 kabupaten (untuk peta)
  data/staging/kabupaten.parquet    — atribut + luas + centroid (+ CC_2 = kode BPS)

CATATAN JUJUR: GADM 4.1 (2022) punya 502 kabupaten; BPS 2025 punya 514 (ada
pemekaran di Papua 2022+). Selisih ini dilaporkan di data quality test —
tidak dipaksa cocok.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

from config import GADM_ADM2_URL, STAGING

H = {"User-Agent": "geo-access-atlas/1.0"}


def main() -> None:
    print("[geo] unduh GADM ADM2 (kabupaten/kota)...")
    raw = urllib.request.urlopen(
        urllib.request.Request(GADM_ADM2_URL, headers=H), timeout=180).read()
    gj = json.loads(raw)
    print(f"  → {len(gj['features'])} fitur")

    rows = []
    for f in gj["features"]:
        p = f["properties"]
        rows.append({
            "kode_bps": p.get("CC_2"),          # kode BPS (join key!)
            "nama_kab": p.get("NAME_2"),
            "nama_prov": p.get("NAME_1"),
            "tipe": p.get("TYPE_2"),
            "gid": p.get("GID_2"),
            "geometry": shape(f["geometry"]),
        })
    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")

    # PEMBERSIHAN (temuan data GADM 4.1 — jujur, dicatat):
    #  · kode_bps 'NA' → wilayah baru tanpa kode BPS (Kaltara, Lake Toba)
    #  · kode_bps duplikat (7502 muncul utk Kab. & Kota Gorontalo)
    # Kita buang 'NA' dan dedup kode_bps (simpan yang bukan "Kabupaten" bila
    # bentrok, karena BPS sering menyatukan keduanya).
    gdf = gdf[gdf["kode_bps"].notna() & (gdf["kode_bps"] != "NA")].copy()
    gdf = gdf.sort_values("tipe").drop_duplicates(subset=["kode_bps"], keep="last")
    print(f"  → setelah pembersihan: {len(gdf)} kabupaten (buang NA & duplikat)")

    gdf.to_file(STAGING / "kabupaten.geojson", driver="GeoJSON")

    # atribut + luas + centroid (reproject ke mercator meter dulu)
    gdf_m = gdf.to_crs("EPSG:3857")
    cent = gdf_m.geometry.centroid.to_crs("EPSG:4326")
    attrs = pd.DataFrame({
        "kode_bps": gdf["kode_bps"],
        "nama_kab": gdf["nama_kab"],
        "nama_prov": gdf["nama_prov"],
        "tipe": gdf["tipe"],
        "area_km2": (gdf_m.area / 1e6).round(1),
        "centroid_lat": cent.y.round(5),
        "centroid_lon": cent.x.round(5),
    })
    attrs.to_parquet(STAGING / "kabupaten.parquet", index=False)
    print(f"  → kabupaten.parquet ({len(attrs)} baris)")
    print(f"  → kode_bps contoh: {attrs['kode_bps'].head(5).tolist()}")
    n_null = attrs["kode_bps"].isna().sum()
    print(f"  → null kode_bps: {n_null}")


if __name__ == "__main__":
    main()
