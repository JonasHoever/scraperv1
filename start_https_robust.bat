@echo off
echo 🚀 Starte robusten HTTPS-Server
echo.
echo 💡 Diese Version versucht verschiedene SSL-Strategien:
echo    1. mkcert (vertrauenswürdige Zertifikate)
echo    2. OpenSSL (selbstsignierte Zertifikate)  
echo    3. Flask adhoc SSL (Fallback)
echo    4. HTTP (Notfall-Fallback)
echo.

REM Prüfe und installiere benötigte Pakete
python -c "import ssl" 2>nul || (
    echo 📦 SSL-Modul nicht verfügbar, aber weiter versuchen...
)

echo 🌐 Starte Server...
python app_https_robust.py

pause
