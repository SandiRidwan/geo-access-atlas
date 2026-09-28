"""
explanations.py — narasi Kenapa · Tujuan · Dampak untuk setiap elemen.

STANDAR WAJIB (portofolio): setiap metrik/peta/tabel menjelaskan
  · KENAPA   — masalah & konteks
  · TUJUAN   — pertanyaan yang dijawab
  · DAMPAK  — implikasi & keputusan
  · CARA BACA (opsional)
"""

from __future__ import annotations

EXPLAIN: dict[str, dict] = {
    "kpi": {
        "judul": "Metrik Ringkas (KPI)",
        "kenapa": "Sebelum menelusuri peta, pembaca butuh angka tunggal: "
                  "seberapa luas kemiskinan, di mana yang terburuk.",
        "tujuan": "Menjawab: berapa banyak kabupaten terpetakan, dan seberapa "
                  "ekstrem ujung sebarannya?",
        "dampak": "Kabupaten termiskin >30% menunjukkan kantong kemiskinan "
                  "yang butuh intervensi terarah, bukan kebijakan seragam.",
        "baca": "Nilai dari tahun terbaru yang tersedia per kabupaten.",
    },
    "map": {
        "judul": "Peta Kemiskinan per Kabupaten",
        "kenapa": "Kemiskinan tidak tersebar merata — ia mengelompok secara "
                  "geografis. Angka nasional menyembunyikan kantong-kantong ini.",
        "tujuan": "Melihat POLA SPASIAL: apakah kemiskinan terkonsentrasi di "
                  "wilayah tertentu (mis. Papua, NTT) atau tersebar?",
        "dampak": "Klaster geografis → alokasi anggaran & program diarahkan ke "
                  "wilayah, bukan per orang. Warna gelap = prioritas intervensi.",
        "baca": "Warna makin merah = kemiskinan makin tinggi. "
                "Arahkan kursor ke kabupaten untuk detail.",
    },
    "ranking": {
        "judul": "Peringkat Kabupaten",
        "kenapa": "Peta menunjukkan pola; peringkat menunjukkan urutan konkret "
                  "yang bisa ditindaklanjuti.",
        "tujuan": "Menemukan kabupaten dengan kemiskinan tertinggi & terendah "
                  "secara eksplisit.",
        "dampak": "Daftar prioritas untuk verifikasi lapangan & intervensi. "
                  "Kabupaten terbaik jadi benchmark praktik.",
        "baca": "Peringkat 1 = kemiskinan terendah (terbaik).",
    },
    "province": {
        "judul": "Ringkasan per Provinsi",
        "kenapa": "Provinsi adalah unit administratif anggaran. Melihat median "
                  "kabupaten per provinsi menghindari distorsi oleh outlier.",
        "tujuan": "Menilai kesenjangan DALAM provinsi (selisih kabupaten "
                  "terkaya vs termiskin).",
        "dampak": "Selisih besar dalam satu provinsi → ketimpangan internal "
                  "yang butuh perhatian khusus; median stabil → pembangunan merata.",
        "baca": "Median lebih tahan pencilan. min–max menunjukkan rentang.",
    },
    "band": {
        "judul": "Sebaran Kelas Kemiskinan",
        "kenapa": "Kategorisasi (rendah/sedang/tinggi/sangat tinggi) membuat "
                  "situasi mudah dicerna tanpa membaca ratusan angka.",
        "tujuan": "Menjawab: berapa banyak kabupaten di tiap tingkat keparahan?",
        "dampak": "Jika mayoritas 'tinggi/sangat tinggi', masalahnya struktural; "
                  "jika hanya segelintir, masalahnya lokal.",
        "baca": "Ambang: <5% rendah, 5–10% sedang, 10–20% tinggi, ≥20% sangat tinggi.",
    },
    "ipm": {
        "judul": "IPM vs Kemiskinan",
        "kenapa": "Kemiskinan (pendapatan) dan IPM (kesehatan+pendidikan) "
                  "mengukur pembangunan dari sisi berbeda.",
        "tujuan": "Menguji apakah kabupaten miskin SELALU ber-IPM rendah — "
                  "atau ada pengecualian penting.",
        "dampak": "Jika keduanya bergerak searah, intervensi ekonomi cukup. "
                  "Jika menyimpang, butuh program kesehatan/pendidikan khusus.",
        "baca": "Tiap titik = satu kabupaten. Titik menyimpang dari garis tren "
                "layak diselidiki.",
    },
    "coverage": {
        "judul": "Cakupan Data (jujur)",
        "kenapa": "Analisis hanya sekuat datanya. Pembaca harus tahu apa yang "
                  "TERCAKUP dan apa yang TIDAK.",
        "tujuan": "Menampilkan jumlah kabupaten terpetakan vs total, dan "
                  "wilayah yang datanya tidak tersedia.",
        "dampak": "Menjaga kesimpulan dalam batas data. Kabupaten tanpa data "
                  "bukan berarti 'tidak miskin' — bisa berarti belum dilaporkan.",
        "baca": "Selisih cakupan berasal dari ketersediaan variabel BPS "
                "per domain & batas wilayah GADM.",
    },
    "method": {
        "judul": "Metodologi & Sumber",
        "kenapa": "Hasil harus dapat ditelusuri & direproduksi. Transparansi "
                  "sumber adalah bagian dari kualitas.",
        "tujuan": "Menjelaskan dari mana data berasal & bagaimana diolah.",
        "dampak": "Pemangku kepentingan dapat memverifikasi & menjalankan ulang.",
        "baca": "Lihat docs/ADR.md & docs/ERD.md untuk detail lengkap.",
    },
}


def text(key: str) -> str:
    e = EXPLAIN.get(key)
    if not e:
        return ""
    parts = [f"**{e['judul']}**",
             f"- **Kenapa:** {e['kenapa']}",
             f"- **Tujuan:** {e['tujuan']}",
             f"- **Dampak:** {e['dampak']}"]
    if e.get("baca"):
        parts.append(f"- **Cara baca:** {e['baca']}")
    return "\n".join(parts)


def render(key: str, expanded: bool = False, st=None) -> None:
    if st is None:
        import streamlit as st  # noqa
    e = EXPLAIN.get(key)
    if not e:
        return
    with st.expander(f"💡 {e['judul']} — Kenapa · Tujuan · Dampak",
                     expanded=expanded):
        st.markdown(
            f"**🔎 Kenapa** — {e['kenapa']}\n\n"
            f"**🎯 Tujuan** — {e['tujuan']}\n\n"
            f"**📈 Dampak** — {e['dampak']}")
        if e.get("baca"):
            st.caption(f"👁️ Cara baca: {e['baca']}")


def audit(verbose: bool = True) -> bool:
    ok = True
    for k, v in EXPLAIN.items():
        miss = [f for f in ("kenapa", "tujuan", "dampak") if not v.get(f)]
        if miss:
            ok = False
            if verbose:
                print(f"  MISSING {k}: {miss}")
    if verbose:
        print(f"Penjelasan: {len(EXPLAIN)} | "
              f"{'SEMUA LENGKAP' if ok else 'ADA YANG KURANG'}")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if audit() else 1)
