# TUBES-AKA

Repository ini berisi source code Tugas Besar mata kuliah Analisis Kompleksitas Algoritma (AKA) CAK2BAB2 oleh dosen LDS. Dikerjakan oleh Kelompok AKA: Gharin Iskandar (103012400314) dan Yuriko Astiani (103012400045). Kami berharap tugas ini memenuhi spesifikasi dan tujuan pembelajaran.

# Analisis Efisiensi Algoritma Iteratif Dan Rekursif Dalam Pengecekan Bilangan Monotonik

Aplikasi Streamlit untuk membandingkan efisiensi algoritma **iteratif** dan **rekursif** dalam mengecek apakah sebuah string digit bersifat:
Tujuan aplikasi ini adalah menganalisis perbedaan efisiensi waktu dan penggunaan memori
antara pendekatan iteratif dan rekursif.

Pengecekan bilangan monotonik digunakan untuk menentukan apakah digit-digit pada suatu bilangan membentuk pola menaik, menurun, atau tidak monotonik. Studi kasus ini diterapkan pada sistem validasi keamanan data mahasiswa, khususnya dalam pemeriksaan PIN atau kode akses pada sistem akademik. Pola digit yang bersifat monotonik cenderung mudah ditebak dan berisiko terhadap keamanan data. Oleh karena itu, algoritma iteratif dan rekursif dibandingkan untuk mengevaluasi efisiensi waktu dan penggunaan memori dalam mendeteksi pola digit sederhana tersebut.

- `naik` (non-decreasing)
- `turun` (non-increasing)
- `tidak monotonik`

## Struktur Proyek

- `monotonic_app.py` - Main Streamlit application
- `monotonic_cli.py` - Implementasi algoritma + CLI demo
- `requirements.txt` - Dependencies

## Dependencies

- Python 3.8+
- `streamlit`
- `matplotlib`

Install:

```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi (Web)

```bash
streamlit run monotonic_app.py
```

Buka browser: http://localhost:8501

## Fitur Aplikasi

- Input berupa string digit (tanpa parsing ke `int`, aman untuk digit panjang)
- Menjalankan algoritma iteratif dan rekursif + rata-rata waktu eksekusi (ms)
- Menampilkan analisis kompleksitas (Big-O)
- Visualisasi:
  - Bar chart perbandingan waktu untuk input saat ini
  - Grafik "Digit vs Posisi"
  - Line chart runtime vs panjang digit (50–900, step 50) dengan skala Y logaritmik

## Catatan Rekursif

Implementasi rekursif dibatasi hingga 950 digit untuk menjaga stabilitas (menghindari `RecursionError`).
