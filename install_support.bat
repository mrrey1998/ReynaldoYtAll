@echo off
setlocal

:: 1. Download dan install IDM (silent)
echo Downloading IDM...
powershell -Command "Invoke-WebRequest -Uri 'https://mirror2.internetdownloadmanager.com/idman643build25.exe' -OutFile '%TEMP%\\idman_setup.exe'"
if not exist "%TEMP%\idman_setup.exe" (
    echo Gagal download IDM. Silakan pilih file idman_setup.exe secara manual.
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f=[System.Windows.Forms.OpenFileDialog]::new(); $f.Filter='EXE Files (*.exe)|*.exe'; $f.Title='Pilih file IDM setup (idman_setup.exe)'; [void]$f.ShowDialog(); Write-Output $f.FileName" > "%TEMP%\idm_path.txt"
    set /p IDM_MANUAL_PATH=<"%TEMP%\idm_path.txt"
    if not exist "%IDM_MANUAL_PATH%" (
        echo File tidak ditemukan. Proses install IDM dilewati.
    ) else (
        echo Installing IDM dari path: %IDM_MANUAL_PATH%
        start /wait "%IDM_MANUAL_PATH%" /silent
    )
) else (
    echo Installing IDM...
    start /wait %TEMP%\idman_setup.exe /silent
)

:: 2. Download dan install Python (silent)
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile '%TEMP%\\python_setup.exe'"
if not exist "%TEMP%\python_setup.exe" (
    echo Gagal download Python. Cek koneksi internet atau link download.
    pause
    exit /b 1
)
echo Installing Python...
start /wait %TEMP%\python_setup.exe /quiet InstallAllUsers=1 PrependPath=1

:: 3. Install yt-dlp via pip
echo Installing yt-dlp...
pip install yt-dlp

:: 4. Download dan extract ffmpeg
set FFMPEG_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
set FFMPEG_ZIP=%TEMP%\ffmpeg.zip
set FFMPEG_DIR=%ProgramFiles%\ffmpeg

echo Downloading ffmpeg...
powershell -Command "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%FFMPEG_ZIP%'"
if not exist "%FFMPEG_ZIP%" (
    echo Gagal download ffmpeg. Cek koneksi internet atau link download.
    pause
    exit /b 1
)
echo Extracting ffmpeg...
powershell -Command "Expand-Archive -Path '%FFMPEG_ZIP%' -DestinationPath '%FFMPEG_DIR%'"

endlocal
echo All done!
pause 