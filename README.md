# Reynaldo Official - YouTube Downloader

Aplikasi download YouTube yang mendukung batch processing dengan IDM dan konversi otomatis.

## Fitur Utama

### 🚀 Batch Download dengan IDM
- **Antrian Download**: Masukkan multiple URL YouTube ke dalam antrian
- **Batch Processing**: Download semua URL dalam antrian sekaligus menggunakan IDM
- **Monitoring Otomatis**: Aplikasi memantau file yang sedang didownload oleh IDM
- **Konversi Otomatis**: File otomatis dikonversi ke MP3 jika diperlukan

### 📥 Metode Download
1. **Otomatis**: Menggunakan IDM jika tersedia, fallback ke yt-dlp
2. **IDM**: Memaksa penggunaan IDM untuk download lebih cepat
3. **Langsung**: Menggunakan yt-dlp langsung

### 🎵 Format Output
- **MP4**: Video dengan kualitas terbaik
- **MP3**: Audio saja dengan kualitas 192kbps

### 🔧 Fitur Teknis
- **Hidden Process**: FFmpeg dan IDM berjalan tanpa menampilkan jendela CMD
- **Real-time Log**: Monitoring proses download dan konversi secara real-time
- **File Tracking**: Melacak status setiap file yang sedang didownload
- **Auto Cleanup**: Menghapus file asli setelah konversi MP3

## Cara Penggunaan

### 1. Menambahkan URL ke Antrian
1. Masukkan URL YouTube di field "URL YouTube"
2. Klik tombol "📋 Masuk Antrian"
3. Ulangi untuk menambahkan lebih banyak URL

### 2. Memulai Batch Download
1. Pastikan semua URL sudah masuk antrian
2. Pilih metode download (Otomatis/IDM/Langsung)
3. Pilih format output (MP4/MP3)
4. Klik tombol "⬇️ Mulai Download"

### 3. Monitoring Proses
- **Log Aktivitas**: Melihat status setiap proses
- **Progress Bar**: Melihat progress batch processing
- **File List**: Melihat file yang sudah didownload

## Persyaratan Sistem

### Software yang Diperlukan
- **Python 3.7+** dengan package:
  - `yt-dlp`
  - `tkinter` (biasanya sudah terinstall)
- **Internet Download Manager** (opsional, untuk download lebih cepat)
- **FFmpeg** (untuk konversi MP3)

### Install Dependencies
```bash
pip install yt-dlp
```

### Install FFmpeg
1. Download FFmpeg dari https://ffmpeg.org/download.html
2. Extract ke folder (misal: `C:\ffmpeg`)
3. Tambahkan `C:\ffmpeg\bin` ke PATH environment

## Struktur File

```
Download YTALL/
├── Reynaldo Official - Youtube Downloader.py  # Aplikasi utama
├── requirements.txt                           # Dependencies
├── install.bat                               # Installer
├── run_downloader.bat                        # Runner
└── Rty.png                                   # Icon aplikasi
```

## Troubleshooting

### IDM Tidak Terdeteksi
- Pastikan IDM sudah terinstall
- Restart aplikasi setelah install IDM
- Cek path IDM di registry Windows

### FFmpeg Error
- Pastikan FFmpeg sudah terinstall dan ada di PATH
- Restart aplikasi setelah install FFmpeg
- Cek versi FFmpeg dengan command: `ffmpeg -version`

### Download Gagal
- Cek koneksi internet
- Pastikan URL YouTube valid
- Coba ganti metode download (Otomatis → Langsung)

## Changelog

### v2.0 - Batch Processing
- ✅ Batch download dengan IDM
- ✅ Monitoring file otomatis
- ✅ Konversi MP3 otomatis
- ✅ Hidden process (tanpa jendela CMD)
- ✅ Real-time log monitoring
- ✅ File tracking system

### v1.0 - Basic Download
- ✅ Download single video
- ✅ Konversi MP3/MP4
- ✅ Interface sederhana

## Support

Untuk bantuan dan pertanyaan, silakan buat issue di repository ini.

---

**Dibuat dengan ❤️ oleh Reynaldo Official**
