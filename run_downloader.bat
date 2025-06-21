@echo off
REM Mengatur direktori kerja
cd /d "%~dp0"

REM Memeriksa apakah Python sudah terinstal
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python tidak terinstal. Silakan instal Python terlebih dahulu.
    pause
    exit /b
)

REM Memeriksa apakah pip sudah terinstal
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip tidak terinstal. Silakan instal pip terlebih dahulu.
    pause
    exit /b
)

REM Menginstal dependensi yang diperlukan
echo Menginstal dependensi...
pip install -r requirements.txt

REM Menjalankan file executable
echo Menjalankan aplikasi...
start "" "dist\download_youtube_mp4_1.exe"

pause