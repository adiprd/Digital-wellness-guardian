# Digital Wellness Guardian

## Gambaran Umum
Aplikasi AI untuk analisis kebiasaan digital dan intervensi kesehatan mental yang membantu pengguna mengambil kendali atas penggunaan teknologi mereka.

## Fitur Utama
- **Analisis Penggunaan**: Pelacakan screen time, penggunaan media sosial, dan frekuensi unlock ponsel
- **Intervensi AI**: Sistem intervensi otomatis berdasarkan pola penggunaan
- **Pelacakan Mood**: Analisis korelasi antara penggunaan digital dan kondisi mental
- **Aktivitas Offline**: Rekomendasi aktivitas offline yang dipersonalisasi
- **Challenge Minimalisme Digital**: Program 7-hari dengan sistem poin

## Teknologi yang Digunakan
- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Analisis Data**: Pandas, NumPy, Scikit-learn
- **Visualisasi**: Matplotlib, Seaborn, Plotly
- **Generasi Data**: Faker

## Struktur Proyek
```
digital_wellness_guardian/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependencies Python
├── data/
│   ├── digital_usage.csv  # Data penggunaan digital
│   ├── mood_tracking.csv  # Data pelacakan mood
│   └── interventions.csv  # Strategi intervensi
└── templates/
    ├── index.html        # Halaman utama
    └── dashboard.html    # Dashboard utama
```

## Instalasi & Setup

### Persyaratan
- Python 3.8 atau lebih tinggi
- Package manager pip

### Langkah Instalasi
```bash
# Jalankan script pembuatan aplikasi
python create_digital_wellness_app.py

# Masuk ke direktori proyek
cd digital_wellness_guardian

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

Aplikasi akan tersedia di `http://localhost:5000`

## Fitur Analisis Data

### Skoring Kecanduan Digital
- **Analisis Screen Time**: Rata-rata penggunaan harian dan pola
- **Monitoring Media Sosial**: Waktu yang dihabiskan di platform sosial
- **Metrik Penggunaan Ponsel**: Frekuensi unlock dan jumlah sesi
- **Penilaian Risiko**: Algoritma komprehensif untuk skor kecanduan

### Analisis Korelasi Mood
- Korelasi real-time antara screen time dan skor mood
- Pengenalan pola dampak terhadap kesehatan mental
- Analisis tren mingguan

### Intervensi Berbasis AI
- Rekomendasi yang dipersonalisasi berdasarkan pola penggunaan
- Sistem intervensi berbasis prioritas
- Langkah-langkah praktis untuk kesehatan digital

## Panduan Penggunaan

### 1. Assesmen Awal
- Sistem menganalisis data sample 30 hari
- Menghitung skor kecanduan digital
- Mengidentifikasi pola penggunaan dan faktor risiko

### 2. Ringkasan Dashboard
- Analisis visual tren screen time
- Chart korelasi mood
- Indikator level risiko

### 3. Sistem Intervensi
- **Prioritas Tinggi**: Tindakan segera untuk penggunaan berat
- **Prioritas Menengah**: Strategi pemecah kebiasaan
- **Prioritas Rendah**: Tips pemeliharaan kesehatan

### 4. Challenge Kesehatan
- Program minimalisme digital 7-hari
- Sistem reward berbasis poin
- Level kesulitan progresif

## Struktur Data Sample

### Data Penggunaan Digital
- Menit screen time harian
- Penggunaan media sosial
- Penggunaan aplikasi produktif
- Jumlah unlock ponsel
- Kategori aplikasi

### Data Pelacakan Mood
- Skor mood harian (1-10)
- Level energi
- Metrik kualitas tidur
- Indikator stres

### Database Intervensi
- Kondisi trigger
- Rekomendasi aksi
- Rating efektivitas

## Opsi Kustomisasi

### Menambah Metrik Baru
Modifikasi generasi data di fungsi `generate_sample_data()` untuk menambah parameter tracking tambahan.

### Intervensi Kustom
Edit method `generate_interventions()` di class `DigitalWellnessAnalyzer` untuk menambah strategi intervensi baru.

### Update Visualisasi
Kustomisasi chart dan grafik di method `generate_visualizations()` menggunakan Matplotlib dan Plotly.

## API Endpoints

- `GET /` - Halaman utama
- `GET /dashboard` - Dashboard analisis utama
- `GET /api/usage_data` - Data penggunaan JSON
- `POST /api/add_intervention` - Tambah intervensi kustom
- `POST /api/start_challenge` - Mulai challenge kesehatan

## Troubleshooting

### Masalah Umum
- **Port sudah digunakan**: Ubah port di `app.run(port=5001)`
- **Dependencies hilang**: Jalankan `pip install -r requirements.txt`
- **Error loading data**: Periksa file CSV di direktori data

### Persistensi Data
Untuk penggunaan production, pertimbangkan:
- Integrasi database (SQLite/PostgreSQL)
- Sistem autentikasi pengguna
- Enkripsi data untuk privasi

## Privasi & Keamanan
- Pemrosesan data lokal
- Tidak ada berbagi data eksternal
- Analisis transparan
- Data dikontrol pengguna

## Pengembangan Selanjutnya
- Integrasi aplikasi mobile
- Pelacakan penggunaan device real-time
- Challenge komunitas
- Integrasi konseling profesional
- Model machine learning lanjutan

## Dukungan
