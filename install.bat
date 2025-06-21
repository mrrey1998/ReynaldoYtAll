@echo off
echo Reynaldo YouTube MP4 Downloader - Installer
echo ==========================================
echo.

echo Mengecek Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python tidak terdeteksi!
    echo Silakan unduh dan instal Python dari: https://www.python.org/downloads/
    echo Pastikan untuk mencentang "Add Python to PATH" saat instalasi
    pause
    exit /b 1
)

echo Python terdeteksi ✓
echo.

echo Menginstal dependensi...
pip install yt-dlp
if errorlevel 1 (
    echo Gagal menginstal yt-dlp
    pause
    exit /b 1
)

echo ✓ Dependensi berhasil diinstal
echo.

echo Mengecek IDM...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\IDMan.exe" >nul 2>&1
if errorlevel 1 (
    reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\App Paths\IDMan.exe" >nul 2>&1
    if errorlevel 1 (
        echo IDM tidak terdeteksi. Aplikasi akan menggunakan download langsung.
        echo Untuk kecepatan optimal, disarankan menginstal IDM.
    ) else (
        echo IDM terdeteksi ✓
    )
) else (
    echo IDM terdeteksi ✓
)

echo.
echo ✅ Instalasi selesai!
echo Anda dapat menjalankan aplikasi dengan mengklik download_youtube_mp4.exe
pause
