
# ---------------------------------------------------------------------------
# KONTEN INSIGHT — Indonesia Poverty & Access Atlas
# Ditulis dari sudut pandang PEMERINTAH / LEMBAGA yang merancang kebijakan
# pengentasan kemiskinan berbasis data.
# ---------------------------------------------------------------------------
from insight import register

register(
    "kpi",
    kesimpulan=(
        "Dari 270 kabupaten terpetakan, kemiskinan median nasional 8.4%, dengan "
        "36 kabupaten masuk kelas 'sangat tinggi' (≥20%). Yang tertinggi — Intan "
        "Jaya (Papua) 40.0% — hampir 5× median nasional. Ini menunjukkan "
        "kemiskinan TIDAK tersebar rata: ada kantong-kantong ekstrem."),
    rekomendasi=[
        "Prioritaskan anggaran pengentasan ke 36 kabupaten kelas 'sangat tinggi', "
        "bukan dibagi rata per provinsi.",
        "Bentuk program khusus Papua (di mana hampir semua kabupaten terburuk "
        "berada) dengan pendekatan kontekstual — bukan template nasional.",
        "Pasang target terukur: turunkan kabupaten 'sangat tinggi' dari 36 ke "
        "bawah 20 dalam siklus anggaran berikutnya.",
    ],
    risiko=(
        "Kebijakan berbasis angka nasional (median 8.4%) akan mengabaikan 36 "
        "kabupaten ekstrem. Dana tersebar rata → tidak menyentuh inti masalah, "
        "kemiskinan Papua stagnan, dan kesenjangan melebar."),
    tingkat="kritis",
)

register(
    "map",
    kesimpulan=(
        "Peta mengungkap POLA SPASIAL: kemiskinan tinggi mengelompok di Indonesia "
        "timur (Papua, NTT, Maluku), sementara Jawa & Bali mayoritas rendah. Ini "
        "bukan sebaran acak — ada faktor geografis struktural (akses, infrastruktur, "
        "biaya logistik)."),
    rekomendasi=[
        "Rancang intervensi BERBASIS WILAYAH: klaster Papua butuh solusi berbeda "
        "dari klaster NTT, meski keduanya 'miskin tinggi'.",
        "Investasi infrastruktur konektivitas (jalan, pelabuhan) di kantong "
        "geografis — akar dari biaya tinggi & akses pasar rendah.",
        "Gunakan peta sebagai alat alokasi: warna merah = prioritas anggaran tahun depan.",
    ],
    risiko=(
        "Mengabaikan dimensi ruang berarti mengulang program 'satu ukuran untuk "
        "semua' yang gagal di daerah terpencil. Wilayah dengan biaya logistik tinggi "
        "akan terus tertinggal meski dana ditambah tanpa perbaikan konektivitas."),
    tingkat="tinggi",
)

register(
    "ranking",
    kesimpulan=(
        "Daftar 20 kabupaten termiskin didominasi Papua, sedangkan 20 terkaya "
        "(kemiskinan terendah) tersebar di Jawa-Bali. Jarak antara kabupaten "
        "terburuk (40%) dan terbaik (<2%) mencapai >20× — ketimpangan antardaerah "
        "sangat tajam."),
    rekomendasi=[
        "Fokuskan program pilot di 20 kabupaten terbawah — dampak per rupiah "
        "paling besar di sana.",
        "Pelajari praktik dari 20 kabupaten terbaik (Jawa-Bali) dan adaptasi "
        "konteks lokalnya untuk direplikasi bertahap.",
        "Hindari kebijakan 'rata' provinsi: dalam satu provinsi pun (mis. Papua) "
        "selisih kabupaten bisa sangat besar.",
    ],
    risiko=(
        "Tanpa daftar prioritas eksplisit, anggaran cenderung mengalir ke daerah "
        "yang mudah dijangkau (bukan yang paling butuh). Kabupaten ekstrem tetap "
        "tertinggal, dan target nasional pengentasan kemiskinan meleset."),
    tingkat="tinggi",
)

register(
    "band",
    kesimpulan=(
        "Sebaran kelas kemiskinan menunjukkan bahwa mayoritas kabupaten berada di "
        "kelas 'sedang' (5–10%), namun ada minoritas signifikan di kelas 'sangat "
        "tinggi'. Artinya, masalah kemiskinan Indonesia kini lebih BERSIFAT LOKAL "
        "dan ekstrem ketimbang merata nasional."),
    rekomendasi=[
        "Ubah strategi dari 'pengentasan massal' ke 'penanganan kantong ekstrem' — "
        "sasaran presisi pada kelas sangat tinggi.",
        "Untuk kelas 'sedang', jaga momentum agar tidak naik kelas: program "
        "preventif (lapangan kerja, harga pangan stabil).",
        "Gunakan kelas sebagai KPI: targetkan migrasi kabupaten antar-kelas "
        "(sangat tinggi → tinggi → sedang) per tahun.",
    ],
    risiko=(
        "Jika fokus hanya pada rata-rata, kabupaten di ujung ekstrem bisa "
        "memburuk tanpa terdeteksi. Distribusi 'satu ekor panjang' adalah tanda "
        "bahaya yang tidak terlihat di angka agregat."),
    tingkat="sedang",
)

register(
    "province",
    kesimpulan=(
        "Median kemiskinan per provinsi menunjukkan provinsi dengan kabupaten "
        "paling merata bermasalah (median tinggi) sekaligus adanya provinsi yang "
        "mediannya rendah TAPI menyimpan kabupaten ekstrem. Selisih min–max dalam "
        "satu provinsi menunjukkan ketimpangan internal yang nyata."),
    rekomendasi=[
        "Alokasikan dana provinsi dengan mempertimbangkan KETIMPANGAN INTERNAL, "
        "bukan hanya rata-rata provinsi.",
        "Untuk provinsi dengan selisih min–max besar, jalankan program khusus "
        "kabupaten — jangan seragam provinsi.",
        "Audit mengapa kabupaten tertentu tertinggal jauh dari tetangganya "
        "(akses, tata kelola, atau data).",
    ],
    risiko=(
        "Dana provinsi yang dialokasikan rata akan terserap kabupaten 'mampu' "
        "yang lebih siap secara administratif. Kabupaten paling miskin justru "
        "kalah dalam penyerapan — memperparah ketimpangan internal."),
    tingkat="tinggi",
)

register(
    "ipm",
    kesimpulan=(
        "Scatter IPM vs kemiskinan menunjukkan korelasi negatif kuat: kabupaten "
        "dengan IPM rendah cenderung miskin. Namun ada titik MENYIMPANG — kabupaten "
        "dengan IPM relatif baik tapi kemiskinan tinggi, atau sebaliknya. Titik "
        "menyimpang inilah yang paling informatif."),
    rekomendasi=[
        "Untuk kabupaten dengan IPM tinggi TAPI miskin: masalahnya kemungkinan "
        "akses ekonomi/lapangan kerja — fokus pada penciptaan pendapatan.",
        "Untuk kabupaten dengan IPM rendah TAPI kemiskinan sedang: fokus pada "
        "kesehatan & pendidikan dasar.",
        "Jadikan analisis menyimpang ini dasar program DIFERENSIAL (bukan satu "
        "jenis intervensi untuk semua kabupaten miskin).",
    ],
    risiko=(
        "Menyamakan semua kabupaten miskin dengan program ekonomi mengabaikan "
        "kabupaten yang sebenarnya butuh intervensi kesehatan/pendidikan. Dana "
        "salah sasaran → pembangunan manusia stagnan meski ekonomi 'terlihat' naik."),
    tingkat="sedang",
)
