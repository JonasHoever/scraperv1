@echo off
echo 🚀 Starte HTTPS-Server für Geolocation-Unterstützung
echo.

REM Prüfe ob pyOpenSSL installiert ist
python -c "import OpenSSL" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installiere pyOpenSSL für automatische SSL-Zertifikate...
    pip install pyopenssl
    echo.
)

REM Prüfe ob cryptography installiert ist
python -c "import cryptography" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installiere cryptography für SSL-Unterstützung...
    pip install cryptography
    echo.
)

echo 🌐 Starte HTTPS-Server...
echo 📍 URL: https://127.0.0.1:5000
echo ⚠️  Akzeptieren Sie das SSL-Zertifikat im Browser
echo 🎯 Geolocation funktioniert jetzt!
echo.

python app_https.py

pause
