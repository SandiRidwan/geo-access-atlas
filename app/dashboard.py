"""
dashboard.py — Streamlit: Peta Kemiskinan & Akses Indonesia.

Menyajikan peta choropleth interaktif (Folium), peringkat, ringkasan provinsi,
sebaran kelas, dan scatter IPM vs kemiskinan. Setiap elemen disertai narasi
Kenapa · Tujuan · Dampak.

Data dari DuckDB (marts). Jalankan: streamlit run app/dashboard.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import duckdb
import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from config import COLORS as C, DB_FILE, MARTS, STAGING  # noqa: E402
import explanations as X  # noqa: E402

st.set_page_config(page_title="Indonesia Poverty & Access Atlas",
                   page_icon="🗺️", layout="wide")

BAND_COLOR = {"rendah": "#1F5C3D", "sedang": "#E4A11B",
              "tinggi": "#E76F51", "sangat tinggi": "#C0392B"}


def _data_source() -> str:
    """
    Pilih sumber data:
      · 'db'    → DuckDB (hasil pipeline lokal)
      · 'marts' → Parquet marts + GeoJSON (fallback untuk cloud tanpa kredensial)
    Fallback penting: di Streamlit Cloud, pipeline ingest butuh BPS_API_KEY yang
    mungkin tidak diset. Agar app TETAP jalan, marts Parquet (yg kecil, di-commit)
    dibaca langsung.
    """
    if DB_FILE.exists():
        return "db"
    if (MARTS / "mart_kabupaten_profile.parquet").exists():
        return "marts"
    return "none"


_SRC = _data_source()


def _ensure_data() -> None:
    """
    Bootstrap HANYA jika tak ada DB maupun marts. Di cloud, marts sudah
    di-commit → tak perlu ingest (yang butuh kredensial BPS).
    """
    if _SRC != "none":
        return
    with st.spinner("Membangun database dari sumber (butuh kredensial BPS)... "
                    "mungkin 1–2 menit"):
        subprocess.run([sys.executable, str(ROOT / "src" / "run_pipeline.py")],
                       cwd=str(ROOT), capture_output=True, text=True)


_ensure_data()


def _read_marts(name: str) -> pd.DataFrame:
    """Baca satu mart dari Parquet (fallback tanpa DuckDB)."""
    p = MARTS / f"{name}.parquet"
    return pd.read_parquet(p) if p.exists() else pd.DataFrame()


@st.cache_data(show_spinner="Membaca data...")
def q(sql: str) -> pd.DataFrame:
    """
    Jalankan query. Bila DB ada → DuckDB. Bila tidak → petakan query umum
    ke pembacaan Parquet langsung (fallback cloud).
    """
    if _SRC == "db":
        con = duckdb.connect(str(DB_FILE), read_only=True)
        df = con.execute(sql).df()
        con.close()
        return df
    # fallback: kenali query yang dipakai dashboard
    s = sql.lower()
    if "mart_kabupaten_profile" in s:
        return _read_marts("mart_kabupaten_profile")
    if "mart_province_summary" in s:
        return _read_marts("mart_province_summary").sort_values(
            "poverty_pct_median", ascending=False)
    return pd.DataFrame()


@st.cache_data(show_spinner="Memuat geometri...")
def load_geo() -> dict:
    for p in (STAGING / "kabupaten.geojson", ROOT / "kabupaten.geojson",
              ROOT / "data" / "kabupaten.geojson"):
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return {"type": "FeatureCollection", "features": []}


def style(fig, h=430):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=54, b=10),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#D5DBE1"),
                      title=dict(font=dict(size=16, color="#fff")),
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(gridcolor="#2A3038", zeroline=False)
    fig.update_yaxes(gridcolor="#2A3038", zeroline=False)
    return fig


def kpi(col, label, value, sub, color):
    col.markdown(
        f"""<div style="background:#1A1F2B;border-left:4px solid {color};
        padding:14px 16px;border-radius:10px;height:120px;">
        <div style="color:#9AA7B4;font-size:.76rem;text-transform:uppercase;
        letter-spacing:.06em;">{label}</div>
        <div style="color:{color};font-size:1.5rem;font-weight:700;
        margin-top:6px;">{value}</div>
        <div style="color:#6B7885;font-size:.75rem;">{sub}</div></div>""",
        unsafe_allow_html=True)


prof = q("SELECT * FROM mart_kabupaten_profile")
prov = q("SELECT * FROM mart_province_summary ORDER BY poverty_pct_median DESC")

# ---- header --------------------------------------------------------------
st.markdown(
    f"""<div style="background:linear-gradient(100deg,{C['primary']},{C['blue']});
    padding:22px 26px;border-radius:14px;margin-bottom:18px;">
    <div style="font-size:1.7rem;font-weight:800;color:white;">
    🗺️ Indonesia Poverty & Access Atlas</div>
    <div style="color:#D7E4DC;font-size:.9rem;margin-top:4px;">
    Kemiskinan & IPM per kabupaten/kota · BPS + GADM + OpenStreetMap ·
    pipeline DuckDB · by <b>Sandi Ridwan</b></div></div>""",
    unsafe_allow_html=True)

# ---- sidebar -------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Filter")
bands = sorted(prof["poverty_band"].dropna().unique())
sel_band = st.sidebar.multiselect("Kelas kemiskinan", bands, default=bands)
only_ipm = st.sidebar.checkbox("Hanya yang punya IPM", value=False)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Sumber: **BPS WebAPI** (kemiskinan & IPM, 2020–2025), **GADM 4.1** (batas "
    "wilayah), **OpenStreetMap** (fasilitas). Pipeline: ingest → DuckDB → "
    "SQL marts → peta. Uji kualitas data di `tests/`.")

d = prof[prof["poverty_band"].isin(sel_band)] if sel_band else prof
if only_ipm:
    d = d[d["ipm"].notna()]

# ---- KPI -----------------------------------------------------------------
X.render("kpi", st=st)
k1, k2, k3, k4 = st.columns(4)
n_kab = len(prof)
worst = prof.loc[prof["poverty_pct"].idxmax()]
kpi(k1, "Kabupaten terpetakan", f"{n_kab}", "dari 277 tersedia di BPS",
    C["primary"])
kpi(k2, "Kemiskinan tertinggi",
    f"{worst['poverty_pct']:.1f}%",
    f"{str(worst['wilayah_nama'])[:18]}", C["red"])
kpi(k3, "Median nasional", f"{prof['poverty_pct'].median():.1f}%",
    "seluruh kabupaten", C["accent"])
kpi(k4, "Sangat tinggi (≥20%)",
    f"{(prof['poverty_pct']>=20).sum()}",
    "kabupaten", C["purple"])
st.write("")

t1, t2, t3, t4 = st.tabs(["🗺️ Peta", "🏆 Peringkat", "📊 Provinsi & Kelas",
                          "🔬 Metodologi"])

with t1:
    X.render("map", st=st)
    geo = load_geo()
    # gabung nilai ke geojson
    geo_vals = {f["properties"].get("kode_bps"): f
                for f in geo.get("features", [])}
    col = st.selectbox("Warnai peta berdasarkan",
                       ["poverty_pct", "ipm"], index=0)
    basemap = st.radio("Latar peta", ["Polos (andal)", "OpenStreetMap"],
                       horizontal=True, index=0)
    if basemap == "OpenStreetMap":
        m = folium.Map(location=[-2.5, 118], zoom_start=4,
                       tiles="OpenStreetMap",
                       attr="&copy; OpenStreetMap contributors")
    else:
        # Tanpa tile eksternal: latar solid, hanya batas & warna kabupaten.
        # Andal di lingkungan yang memblok tile (mis. jaringan terbatas).
        m = folium.Map(location=[-2.5, 118], zoom_start=4,
                       tiles=None, zoom_control=True)
    folium.Choropleth(
        geo_data=geo,
        data=d,
        columns=["kode_bps", col],
        key_on="feature.properties.kode_bps",
        fill_color="YlOrRd" if col == "poverty_pct" else "YlGnBu",
        fill_opacity=0.75,
        line_opacity=0.2,
        nan_fill_color="#333",
        legend_name="Kemiskinan (%)" if col == "poverty_pct" else "IPM",
    ).add_to(m)
    # tooltip
    lookup = d.set_index("kode_bps")[["wilayah_nama", "nama_prov",
                                      "poverty_pct", "ipm"]].to_dict("index")
    folium.GeoJson(
        geo,
        style_function=lambda x: {"fillOpacity": 0, "weight": 0},
        tooltip=folium.GeoJsonTooltip(
            fields=["kode_bps"], aliases=["Kode:"],
            labels=True, sticky=False),
    ).add_to(m)
    st_folium(m, height=560, use_container_width=True, returned_objects=[])
    st.caption("Warna gelap = nilai ekstrem. Kabupaten tanpa data berwarna abu.")

with t2:
    X.render("ranking", st=st)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**20 termiskin**")
        w = d.nlargest(20, "poverty_pct")[
            ["wilayah_nama", "nama_prov", "poverty_pct"]]
        fig = px.bar(w.iloc[::-1], x="poverty_pct", y="wilayah_nama",
                     orientation="h", color_discrete_sequence=[C["red"]])
        style(fig, 620).update_layout(title="", xaxis_title="%",
                                      yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("**20 terkaya (kemiskinan terendah)**")
        b = d.nsmallest(20, "poverty_pct")[
            ["wilayah_nama", "nama_prov", "poverty_pct"]]
        fig = px.bar(b.iloc[::-1], x="poverty_pct", y="wilayah_nama",
                     orientation="h", color_discrete_sequence=[C["primary"]])
        style(fig, 620).update_layout(title="", xaxis_title="%",
                                      yaxis_title="", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with t3:
    X.render("band", st=st)
    bc = d["poverty_band"].value_counts().reindex(
        ["rendah", "sedang", "tinggi", "sangat tinggi"]).dropna()
    fig = px.bar(x=bc.index, y=bc.values,
                 color=bc.index, color_discrete_map=BAND_COLOR,
                 text=bc.values)
    fig.update_traces(textposition="outside")
    style(fig, 380).update_layout(title="Sebaran Kelas Kemiskinan",
                                  xaxis_title="", yaxis_title="kabupaten",
                                  showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    X.render("province", st=st)
    fig = px.bar(prov, x="poverty_pct_median", y="nama_prov",
                 orientation="h", color="poverty_pct_median",
                 color_continuous_scale="YlOrRd",
                 text=prov["poverty_pct_median"].round(1))
    style(fig, 620).update_layout(coloraxis_showscale=False,
                                  title="Median Kemiskinan per Provinsi",
                                  xaxis_title="%", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(prov, use_container_width=True, hide_index=True)

    if d["ipm"].notna().any():
        X.render("ipm", st=st)
        sc = d[d["ipm"].notna()]
        fig = px.scatter(sc, x="ipm", y="poverty_pct", color="nama_prov",
                         hover_name="wilayah_nama", size="area_km2",
                         size_max=22)
        fig.update_traces(marker=dict(line=dict(width=0.5, color="#222")))
        style(fig, 480).update_layout(title="IPM vs Kemiskinan per Kabupaten",
                                      xaxis_title="IPM",
                                      yaxis_title="Kemiskinan (%)")
        st.plotly_chart(fig, use_container_width=True)

with t4:
    X.render("method", st=st)
    st.markdown("#### Arsitektur pipeline")
    st.code("""
 BPS WebAPI ─┐
 GADM 4.1 ───┼─► ingest_bps.py + ingest_geo.py ─► data/staging (Parquet)
 OSM ────────┘                  │
                                ▼
                       load_db.py ─► DuckDB (staging)
                                │
                                ▼
                  sql/transform.sql ─► marts (kanonikalisasi + join)
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
       dashboard.py       make_charts.py   tests/test_data_quality.py
    """, language="text")

    X.render("coverage", st=st)
    n_mapped = len(prof)
    # 'tersedia di BPS' dari meta ingest bila ada; jika tidak, pakai jumlah yg dipetakan
    bps_avail = None
    meta_p = STAGING / "_bps_meta.json"
    if meta_p.exists():
        try:
            bps_avail = len(prof)  # konservatif: sama dgn yg terpetakan
        except Exception:
            bps_avail = None
    cov = pd.DataFrame([{
        "terpetakan": n_mapped,
        "total_kabupaten_indonesia": 514,
        "sumber_data": _SRC,
    }])
    st.dataframe(cov, use_container_width=True, hide_index=True)
    st.markdown(
        "- **Kenapa < 514?** BPS hanya mempublikasikan variabel kemiskinan di "
        "sebagian domain provinsi (DKI, Bali, Kep. Babel, Kaltara tidak "
        "menyediakannya di WebAPI). Jadi ini **fakta ketersediaan data**, "
        "bukan kelemahan analisis. Dari ~277 yang tersedia, sebagian besar "
        "berhasil dipetakan.\n"
        "- **Kanikalisasi judul.** Judul variabel BPS berbeda antar provinsi "
        "(mis. '[Metode Baru]', 'SP2010') — disatukan lewat pencocokan kata kunci "
        "di `sql/transform.sql`.\n"
        "- **Sumber fallback.** Bila `BPS_API_KEY` tidak diset (mis. di cloud), "
        "dashboard membaca marts Parquet yang di-commit — sehingga app tetap "
        "jalan tanpa kredensial.\n"
        "- Sumber & keputusan lengkap: `docs/ADR.md`.")

st.markdown(
    f"""<hr style="border-color:#2A3038;">
    <div style="color:#8B9AA6;font-size:.8rem;text-align:center;">
    🗺️ Indonesia Poverty & Access Atlas · BPS + GADM + OSM ·
    pipeline DuckDB + SQL · oleh <b>Sandi Ridwan</b><br>
    Analisis edukasional. Data © BPS, GADM, OpenStreetMap (ODbL).</div>""",
    unsafe_allow_html=True)
