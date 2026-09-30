
# ---------------------------------------------------------------------------
# KONTEN INSIGHT — Indonesia Poverty & Access Atlas
# Ditulis dari sudut pandang PEMERINTAH / LEMBAGA yang merancang kebijakan
# pengentasan kemiskinan berbasis data.
#
# Format rekomendasi: KAYA (aksi + langkah + metrik + pemilik).
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
        {
            "aksi": "Prioritaskan anggaran pengentasan ke 36 kabupaten kelas 'sangat tinggi'",
            "langkah": [
                "Tarik daftar 36 kabupaten kelas 'sangat tinggi' (≥20%) dari data BPS kemiskinan 2020–2025 yang sudah dipetakan ke 270 kabupaten.",
                "Susun matriks prioritas 2 sumbu: (1) tingkat kemiskinan, (2) jumlah penduduk miskin — agar anggaran menargetkan kabupaten dengan beban absolut terbesar.",
                "Kunci alokasi berbasis bobot kebutuhan (bukan per-provinsi rata) dan validasi dengan GADM 4.1 untuk memastikan batas administrasi kabupaten penerima tepat.",
            ],
            "metrik": "Jumlah kabupaten ≥20% yang menerima pos anggaran khusus; 100% dari 36 kabupaten terdaftar dengan nilai alokasi terverifikasi.",
            "pemilik": "Direktorat Perencanaan Anggaran (Bappenas) bersama DJPK Kemenkeu",
        },
        {
            "aksi": "Bentuk program khusus Papua dengan pendekatan kontekstual",
            "langkah": [
                "Kelompokkan kabupaten Papua berdasarkan klaster kemiskinan (data menunjukkan klaster Papua hingga ~40%) dan tandai mana yang punya akses jalan/pelabuhan terbatas via layer OpenStreetMap.",
                "Rancang paket intervensi per-klaster: kombinasi bantuan pangan, konektivitas, dan layanan dasar — bukan satu template nasional.",
                "Kawal implementasi lintas kementerian dengan unit koordinasi khusus Papua dan laporan triwulanan berbasis data kabupaten (bukan agregat provinsi).",
            ],
            "metrik": "Persentase kabupaten Papua dengan paket intervensi kontekstual aktif; penurunan rata-rata kemiskinan klaster Papua ≥2 poin persen dalam 2 tahun.",
            "pemilik": "Kementerian Koordinator PMK / Badan Pengarah Percepatan Papua",
        },
        {
            "aksi": "Pasang target terukur penurunan kabupaten 'sangat tinggi' dari 36 ke bawah 20",
            "langkah": [
                "Tetapkan baseline resmi: 36 kabupaten ≥20% pada siklus anggaran berjalan (bersumber dari 270 kabupaten terpetakan).",
                "Buat dashboard pemantauan yang menghitung otomatis perpindahan kelas (sangat tinggi → tinggi → sedang) setiap rilis data BPS.",
                "Jalankan 14 uji kualitas data sebelum setiap pelaporan target agar angka perpindahan kelas terbebas dari anomali/outlier.",
            ],
            "metrik": "Jumlah kabupaten 'sangat tinggi' turun dari 36 menjadi <20 dalam satu siklus anggaran berikutnya.",
            "pemilik": "Bappenas (kedeputian pengentasan kemiskinan) + BPS sebagai penyedia data",
        },
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
        {
            "aksi": "Rancang intervensi BERBASIS WILAYAH per klaster",
            "langkah": [
                "Overlay peta kemiskinan (BPS, 270 kabupaten) dengan batas GADM 4.1 untuk membentuk klaster spasial: klaster Papua, klaster NTT, klaster Maluku.",
                "Susun profil kebutuhan tiap klaster — karena sama-sama 'miskin tinggi' namun akar masalahnya berbeda (isolasi geografis vs keterbatasan lahan vs tata kelola).",
                "Siapkan paket kebijakan berbeda per klaster dan uji kesesuaiannya dengan tipologi wilayah sebelum dieksekusi.",
            ],
            "metrik": "Tersedianya dokumen intervensi per-klaster (Papua/NTT/Maluku) dengan indikator kebutuhan spesifik; 0 program nasional seragam untuk klaster ini.",
            "pemilik": "Direktorat Kawasan & Pengembangan Wilayah (Bappenas) bersama Pemprov terkait",
        },
        {
            "aksi": "Investasi infrastruktur konektivitas di kantong geografis",
            "langkah": [
                "Petakan lokasi kantong kemiskinan ekstrem dan silangkan dengan data fasilitas OpenStreetMap (jalan, pelabuhan, sekolah, puskesmas) untuk menemukan kesenjangan akses.",
                "Prioritaskan ruas jalan & pelabuhan yang menghubungkan kabupaten ≥20% ke pasar/pusat layanan terdekat.",
                "Integrasikan proyek dengan target penurunan biaya logistik daerah dan pastikan batas proyek memakai GADM 4.1 (mencatat jujur kabupaten pemekaran 2022+ yang belum termuat).",
            ],
            "metrik": "Panjang jalan/pelabuhan baru yang tersambung ke kantong miskin; penurunan indeks biaya logistik daerah tertinggal dalam 3 tahun.",
            "pemilik": "Kementerian PUPR + Kementerian Perhubungan",
        },
        {
            "aksi": "Gunakan peta sebagai alat alokasi anggaran (warna merah = prioritas)",
            "langkah": [
                "Standarkan skala warna peta pada kelas kemiskinan (merah = ≥20%) agar konsisten dengan daftar 36 kabupaten prioritas.",
                "Jadikan layer merah sebagai input wajib dalam rapat alokasi anggaran tahun depan, bukan sekadar visualisasi.",
                "Publikasikan peta prioritas secara berkala sebagai alat transparansi dan akuntabilitas alokasi.",
            ],
            "metrik": "Persentase keputusan alokasi yang merujuk langsung ke layer prioritas peta; jumlah kabupaten merah yang mendapat kenaikan anggaran.",
            "pemilik": "Sekretariat Kabinet / Tim Anggaran Pemerintah Pusat",
        },
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
        {
            "aksi": "Fokuskan program pilot di 20 kabupaten terbawah",
            "langkah": [
                "Ambil peringkat 20 kabupaten termiskin dari hasil ranking atas 270 kabupaten terpetakan (data BPS 2020–2025).",
                "Hitung dampak potensial per rupiah (efisiensi intervensi) untuk memilih urutan eksekusi pilot.",
                "Jalankan pilot bertahap 3 tahun dan evaluasi tahunan berbasis data kabupaten, bukan provinsi.",
            ],
            "metrik": "Dampak penurunan kemiskinan per Rp1 miliar di 20 kabupaten terbawah; jumlah kabupaten pilot yang turun kelas.",
            "pemilik": "Bappenas (unit pilot) + pemerintah kabupaten penerima",
        },
        {
            "aksi": "Pelajari & replikasi praktik 20 kabupaten terbaik (Jawa-Bali)",
            "langkah": [
                "Dokumentasikan faktor keberhasilan 20 kabupaten kemiskinan terendah (<2%) — dari konektivitas, tata kelola, hingga program ketenagakerjaan.",
                "Uji kesesuaian dan adaptasi konteks lokal sebelum replikasi (hindari copy-paste kebijakan).",
                "Replikasi bertahap ke kabupaten dengan karakteristik serupa, dengan pendampingan teknis dari kabupaten percontohan.",
            ],
            "metrik": "Jumlah praktik terbaik terdokumentasi & direplikasi; selisih kemiskinan antara kabupaten replikasi dan percontohan menyempit.",
            "pemilik": "Kementerian Dalam Negeri + Bappenas",
        },
        {
            "aksi": "Hindari kebijakan 'rata' provinsi — sasaran level kabupaten",
            "langkah": [
                "Hitung selisih kabupaten terburuk vs terbaik DALAM satu provinsi (mis. Papua) untuk menampilkan ketimpangan internal.",
                "Tetapkan alokasi berbasis kabupaten, bukan rata provinsi, khusus untuk provinsi dengan sebaran ekstrem.",
                "Sosialisasikan profil ketimpangan internal ke pemprov sebagai dasar perencanaan.",
            ],
            "metrik": "Persentase alokasi yang turun ke level kabupaten; rasio kemiskinan maks/min dalam provinsi membaik per tahun.",
            "pemilik": "Pemerintah Provinsi (Bappeda) + DJPK Kemenkeu",
        },
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
        {
            "aksi": "Ubah strategi dari 'pengentasan massal' ke 'penanganan kantong ekstrem'",
            "langkah": [
                "Kelompokkan 270 kabupaten ke band kemiskinan (rendah/sedang/tinggi/sangat tinggi) dan fokuskan sumber daya pada band sangat tinggi (≥20%).",
                "Realokasi sebagian dana program massal ke kantong ekstrem tanpa meniadakan program preventif untuk band sedang.",
                "Tetapkan protokol 'penanganan kantong' dengan sasaran presisi kabupaten, bukan agregat provinsi.",
            ],
            "metrik": "Persentase dana yang dialihkan ke kantong ekstrem; jumlah kabupaten band sangat tinggi yang turun kelas per tahun.",
            "pemilik": "Kementerian Sosial + Bappenas",
        },
        {
            "aksi": "Jaga momentum kelas 'sedang' dengan program preventif",
            "langkah": [
                "Identifikasi kabupaten band sedang (5–10%) yang berisiko naik kelas berdasarkan tren BPS 2020–2025.",
                "Jalankan program preventif: perluasan lapangan kerja dan stabilisasi harga pangan di kabupaten rawan.",
                "Pantau kuartalan agar kabupaten tidak 'tergelincir' ke band tinggi sebelum terdeteksi.",
            ],
            "metrik": "Jumlah kabupaten band sedang yang tetap/turun kelas; tidak ada kenaikan kelas ke atas pada kabupaten rawan.",
            "pemilik": "Kementerian Ketenagakerjaan + Bulog/Bapanas (pangan)",
        },
        {
            "aksi": "Gunakan kelas kemiskinan sebagai KPI migrasi antar-band",
            "langkah": [
                "Definisikan matriks migrasi band (sangat tinggi → tinggi → sedang) sebagai indikator keberhasilan tahunan.",
                "Bangun pemantauan otomatis perpindahan band setiap rilis data BPS.",
                "Terapkan 14 uji kualitas data sebelum migrasi band diakui valid (cegah klaim semu).",
            ],
            "metrik": "Jumlah kabupaten yang naik band (membaik) per tahun; indeks migrasi band agregat nasional.",
            "pemilik": "BPS (data) + Bappenas (monitoring KPI)",
        },
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
        {
            "aksi": "Alokasikan dana provinsi dengan mempertimbangkan KETIMPANGAN INTERNAL",
            "langkah": [
                "Hitung untuk setiap provinsi: median, min, dan max kemiskinan kabupaten (dari 270 kabupaten terpetakan).",
                "Tambahkan bobot ketimpangan (selisih min–max) ke dalam formula alokasi, bukan hanya rata-rata provinsi.",
                "Validasi batas provinsi/kabupaten dengan GADM 4.1 sebelum finalisasi alokasi.",
            ],
            "metrik": "Formula alokasi memasukkan komponen ketimpangan internal; rasio min–max provinsi prioritas menyempit.",
            "pemilik": "DJPK Kemenkeu + Bappenas",
        },
        {
            "aksi": "Jalankan program khusus kabupaten untuk provinsi berselisih min–max besar",
            "langkah": [
                "Urutkan provinsi berdasarkan lebar selisih min–max dan tandai yang terbesar sebagai fokus.",
                "Untuk provinsi tersebut, rancang program level kabupaten (bukan seragam provinsi) yang menyasar kabupaten tertinggal.",
                "Sinergikan antara dana provinsi, kabupaten, dan pusat untuk kabupaten sasaran.",
            ],
            "metrik": "Jumlah provinsi dengan program kabupaten khusus; penurunan kemiskinan kabupaten tertinggal di provinsi sasaran.",
            "pemilik": "Bappeda Provinsi + Kementerian Dalam Negeri",
        },
        {
            "aksi": "Audit penyebab kabupaten tertinggal jauh dari tetangganya",
            "langkah": [
                "Pilih kabupaten dengan deviasi besar dari median provinsi dan lakukan diagnosis: akses (data OSM), tata kelola, atau kualitas data.",
                "Bandingkan indikator fasilitas (jalan, sekolah, puskesmas) dengan kabupaten tetangga yang lebih baik.",
                "Rumuskan rencana perbaikan spesifik berdasarkan penyebab yang terverifikasi.",
            ],
            "metrik": "Jumlah kabupaten teraudit dengan rencana perbaikan; penurunan deviasi terhadap median provinsi.",
            "pemilik": "Inspektorat/BPKP + Bappeda Provinsi",
        },
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
        {
            "aksi": "Untuk IPM tinggi TAPI miskin: fokus penciptaan pendapatan",
            "langkah": [
                "Identifikasi kabupaten pada kuadran IPM tinggi–kemiskinan tinggi dari scatter (data BPS kemiskinan & IPM 2020–2025).",
                "Diagnosis akar masalah: akses ekonomi, lapangan kerja, dan rantai pasar (silangkan dengan fasilitas OSM).",
                "Rancang program penciptaan pendapatan (UMKM, padat karya, akses pasar) untuk kuadran ini.",
            ],
            "metrik": "Jumlah kabupaten kuadran ini yang mendapat program pendapatan; penurunan kemiskinan tanpa penurunan IPM.",
            "pemilik": "Kementerian Koperasi & UKM + Dinas Tenaga Kerja setempat",
        },
        {
            "aksi": "Untuk IPM rendah TAPI kemiskinan sedang: fokus kesehatan & pendidikan dasar",
            "langkah": [
                "Identifikasi kabupaten kuadran IPM rendah–kemiskinan sedang dari scatter.",
                "Petakan kesenjangan layanan dasar (sekolah, puskesmas) menggunakan data OpenStreetMap.",
                "Prioritaskan intervensi kesehatan & pendidikan dasar di kabupaten tersebut.",
            ],
            "metrik": "Kenaikan indeks IPM kabupaten sasaran; perbaikan rasio layanan dasar per penduduk.",
            "pemilik": "Kementerian Kesehatan + Kementerian Pendidikan (Kemendikdasmen)",
        },
        {
            "aksi": "Jadikan analisis titik menyimpang dasar program DIFERENSIAL",
            "langkah": [
                "Kelompokkan kabupaten miskin menjadi dua tipe berdasarkan posisinya terhadap garis tren IPM–kemiskinan.",
                "Susun dua paket intervensi (ekonomi vs kesehatan/pendidikan dasar) yang dipilih berdasarkan tipe kabupaten.",
                "Hindari satu jenis intervensi untuk semua kabupaten miskin; sesuaikan dengan tipe.",
            ],
            "metrik": "Setiap kabupaten miskin memiliki klasifikasi tipe & paket intervensi; tidak ada program tunggal seragam.",
            "pemilik": "Bappenas (desain program) + kementerian teknis pelaksana",
        },
    ],
    risiko=(
        "Menyamakan semua kabupaten miskin dengan program ekonomi mengabaikan "
        "kabupaten yang sebenarnya butuh intervensi kesehatan/pendidikan. Dana "
        "salah sasaran → pembangunan manusia stagnan meski ekonomi 'terlihat' naik."),
    tingkat="sedang",
)


# --------------------------------------------------------------------------
# Chart ECharts (v2) — insight & rekomendasi.
# --------------------------------------------------------------------------

register(
    "echarts_boxplot",
    kesimpulan=(
        "Boxplot kemiskinan per provinsi menunjukkan MEDIAN, SEBARAN, dan "
        "KABUPATEN PENCILAN. Provinsi dengan kotak tinggi = ketimpangan internal "
        "besar (ada kabupaten sangat miskin sekaligus sangat kaya dalam satu "
        "provinsi). Provinsi dengan median tinggi & kotak sempit = kemiskinan "
        "merata — tantangan berbeda, penanganan berbeda."),
    rekomendasi=[
        {
            "aksi": "Bedakan dua pola: (a) median tinggi & merata vs (b) median rendah tapi kotak tinggi",
            "langkah": [
                "Klasifikasi setiap provinsi ke pola (a) atau (b) berdasarkan median dan lebar kotak (IQR) dari boxplot.",
                "Untuk pola (a): rancang intervensi provinsi-lebar karena masalahnya merata.",
                "Untuk pola (b): sasaran kabupaten spesifik (bukan provinsi) karena masalah terkonsentrasi.",
            ],
            "metrik": "Setiap provinsi terklasifikasi ke pola (a)/(b) dengan rencana intervensi berbeda; 0 provinsi tanpa klasifikasi.",
            "pemilik": "Bappenas + Bappeda Provinsi",
        },
        {
            "aksi": "Prioritaskan kabupaten pencilan (titik di atas whisker) untuk intervensi darurat",
            "langkah": [
                "Deteksi kabupaten pencilan di atas whisker (>< median + 1.5×IQR per provinsi).",
                "Klasifikasikan sebagai kasus darurat dan alokasikan respons cepat (bantuan langsung + layanan dasar).",
                "Pantau penurunan kemiskinan kabupaten pencilan secara bulanan/triwulanan.",
            ],
            "metrik": "Jumlah kabupaten pencilan yang menerima intervensi darurat; penurunan kemiskinan pencilan ke bawah ambang whisker.",
            "pemilik": "BNPB/ Kemensos (respons darurat) + Pemkab",
        },
        {
            "aksi": "Bandingkan pola antar-tahun untuk mengukur penyempitan ketimpangan",
            "langkah": [
                "Susun boxplot per provinsi untuk setiap tahun data BPS 2020–2025.",
                "Identifikasi provinsi yang lebar kotak/ketimpangannya menyempit vs memburuk.",
                "Jadikan tren ini input evaluasi kebijakan tahunan.",
            ],
            "metrik": "Tren lebar IQR per provinsi antar-tahun; jumlah provinsi dengan ketimpangan menyempit.",
            "pemilik": "BPS (data) + Bappenas (evaluasi)",
        },
    ],
    risiko=(
        "Program berbasis rata-rata provinsi bisa melewatkan kabupaten paling "
        "miskin di provinsi 'berpendapatan sedang'. Sumber daya salah alokasi, "
        "dan kantong kemiskinan tetap tersembunyi dalam agregat."),
    tingkat="tinggi",
)

register(
    "echarts_parallel",
    kesimpulan=(
        "Parallel coordinates menampilkan profil multi-indikator tiap provinsi "
        "(kemiskinan median/maks, IPM, jumlah kabupaten, luas) dalam satu "
        "pandangan. Garis menyilang tajam = kombinasi tak biasa, mis. kemiskinan "
        "median rendah tetapi kemiskinan MAKSIMUM tinggi (ada kantong ekstrem), "
        "atau IPM tinggi namun luas wilayah raksasa (tantangan jangkauan layanan)."),
    rekomendasi=[
        {
            "aksi": "Sorot provinsi dengan jurang besar antara kemiskinan median dan maksimum",
            "langkah": [
                "Hitung selisih kemiskinan maksimum − median untuk setiap provinsi dari data BPS 2020–2025.",
                "Tandai provinsi dengan jurang terbesar sebagai prioritas perhatian khusus (indikator ketimpangan).",
                "Sasarankan program pada kabupaten penyumbang nilai maksimum di provinsi tersebut.",
            ],
            "metrik": "Daftar provinsi jurang median–maks terbesar; penurunan nilai kemiskinan maksimum di sana per tahun.",
            "pemilik": "Bappenas + Bappeda Provinsi prioritas",
        },
        {
            "aksi": "Untuk provinsi luas + IPM rendah: prioritaskan strategi jangkauan",
            "langkah": [
                "Identifikasi provinsi pada kuadran luas wilayah besar & IPM rendah dari parallel coordinates.",
                "Rancang strategi jangkauan (infrastruktur/distribusi) daripada sekadar program ekonomi.",
                "Petakan titik layanan via OpenStreetMap untuk menutup kesenjangan jangkauan.",
            ],
            "metrik": "Jumlah provinsi luas–IPM rendah dengan rencana jangkauan; peningkatan cakupan layanan & IPM di provinsi sasaran.",
            "pemilik": "Kementerian PUPR/Perhubungan + Kemendagri",
        },
        {
            "aksi": "Gunakan profil multi-indikator untuk menyusun tipologi provinsi sebelum alokasi",
            "langkah": [
                "Susun tipologi provinsi berdasarkan pola parallel coordinates (jurang kemiskinan, IPM, luas, jumlah kabupaten).",
                "Kaitkan tiap tipe dengan paket kebijakan yang sesuai sebelum alokasi anggaran.",
                "Validasi batas wilayah dengan GADM 4.1 (catat jujur kabupaten pemekaran 2022+ yang belum termuat).",
            ],
            "metrik": "Dokumen tipologi provinsi selesai & dipakai sebagai dasar alokasi; kesesuaian paket kebijakan per tipe.",
            "pemilik": "Bappenas (perencanaan) + Kemenkeu (alokasi)",
        },
    ],
    risiko=(
        "Kebijakan seragam nasional mengabaikan bahwa provinsi punya 'bentuk' "
        "masalah berbeda. Intervensi yang tepat di satu provinsi bisa tidak "
        "relevan di provinsi lain dengan profil menyilang."),
    tingkat="sedang",
)
