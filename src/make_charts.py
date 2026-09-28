"""
make_charts.py — chart PNG statis untuk README (dari marts).

Menghasilkan: sebaran kelas, peringkat provinsi, scatter IPM, top kabupaten.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import COLORS as C, DB_FILE, FIGURES

plt.rcParams.update({"figure.dpi": 130, "savefig.bbox": "tight",
                     "axes.grid": True, "grid.alpha": 0.25,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 10})

BAND = {"rendah": C["primary"], "sedang": C["accent"],
        "tinggi": "#E76F51", "sangat tinggi": C["red"]}


def q(sql: str) -> pd.DataFrame:
    con = duckdb.connect(str(DB_FILE), read_only=True)
    df = con.execute(sql).df()
    con.close()
    return df


def chart_bands() -> None:
    df = q("""SELECT poverty_band, count(*) n FROM mart_kabupaten_profile
              GROUP BY 1""")
    order = ["rendah", "sedang", "tinggi", "sangat tinggi"]
    df = df.set_index("poverty_band").reindex(order).dropna()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df.index, df["n"], color=[BAND[b] for b in df.index])
    for i, v in enumerate(df["n"]):
        ax.text(i, v + 1, int(v), ha="center", fontsize=9)
    ax.set_title("Sebaran Kelas Kemiskinan Kabupaten/Kota", fontweight="bold")
    ax.set_ylabel("jumlah kabupaten")
    fig.savefig(FIGURES / "01_poverty_bands.png")
    plt.close(fig)
    print("  ✓ 01_poverty_bands.png")


def chart_provinces() -> None:
    df = q("""SELECT nama_prov, poverty_pct_median FROM mart_province_summary
              ORDER BY poverty_pct_median DESC LIMIT 18""")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(df["nama_prov"][::-1], df["poverty_pct_median"][::-1],
            color=C["red"])
    for i, v in enumerate(df["poverty_pct_median"][::-1]):
        ax.text(v + 0.1, i, f"{v:.1f}", va="center", fontsize=8)
    ax.set_title("Median Kemiskinan per Provinsi (18 teratas)",
                 fontweight="bold")
    ax.set_xlabel("kemiskinan (%)")
    fig.savefig(FIGURES / "02_province_median.png")
    plt.close(fig)
    print("  ✓ 02_province_median.png")


def chart_top() -> None:
    df = q("""SELECT wilayah_nama, nama_prov, poverty_pct
              FROM mart_kabupaten_profile ORDER BY poverty_pct DESC LIMIT 15""")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    lbl = [f"{r.wilayah_nama} ({r.nama_prov[:10]})" for r in df.itertuples()]
    ax.barh(lbl[::-1], df["poverty_pct"][::-1], color=C["red"])
    for i, v in enumerate(df["poverty_pct"][::-1]):
        ax.text(v + 0.2, i, f"{v:.1f}", va="center", fontsize=8)
    ax.set_title("15 Kabupaten dengan Kemiskinan Tertinggi", fontweight="bold")
    ax.set_xlabel("kemiskinan (%)")
    fig.savefig(FIGURES / "03_top_poverty.png")
    plt.close(fig)
    print("  ✓ 03_top_poverty.png")


def chart_ipm() -> None:
    df = q("""SELECT wilayah_nama, ipm, poverty_pct FROM mart_kabupaten_profile
              WHERE ipm IS NOT NULL""")
    if df.empty:
        print("  (IPM tidak tersedia)"); return
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["ipm"], df["poverty_pct"], alpha=0.5,
               color=C["blue"], s=18)
    ax.set_title("IPM vs Kemiskinan per Kabupaten", fontweight="bold")
    ax.set_xlabel("IPM"); ax.set_ylabel("kemiskinan (%)")
    fig.savefig(FIGURES / "04_ipm_vs_poverty.png")
    plt.close(fig)
    print("  ✓ 04_ipm_vs_poverty.png")


def main() -> None:
    if not DB_FILE.exists():
        raise SystemExit("DB belum ada — jalankan: python src/run_pipeline.py")
    print("[charts] menghasilkan PNG untuk README:")
    chart_bands()
    chart_provinces()
    chart_top()
    chart_ipm()
    print(f"[charts] selesai → {FIGURES}")


if __name__ == "__main__":
    main()
