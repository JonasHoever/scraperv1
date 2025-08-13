@echo off
setlocal enabledelayedexpansion

:: Versicherungsmakler Finder - Windows Start Script
:: Schneller Start der Flask Web-App ohne Installation

echo ========================================
echo 🚀 Versicherungsmakler Finder - Start
echo ========================================
echo.

:: Farbdefinitionen für bessere Lesbarkeit (Windows 10+)
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "RED=%ESC%[31m"
set "GREEN=%ESC%[32m"
set "YELLOW=%ESC%[33m"
set "BLUE=%ESC%[34m"
set "PURPLE=%ESC%[35m"
set "NC=%ESC%[0m"

:: Prüfe ob Virtual Environment vorhanden ist
if not exist ".venv" (
    echo %RED%[ERROR]%NC% Virtual Environment nicht gefunden!
    echo Führe zuerst install.bat aus oder verwende: install.bat --install
    echo.
    pause
    exit /b 1
)

:: Prüfe ob app.py vorhanden ist
if not exist "app.py" (
    echo %RED%[ERROR]%NC% app.py nicht gefunden!
    echo Stelle sicher, dass du im richtigen Projektverzeichnis bist.
    echo.
    pause
    exit /b 1
)

:: Aktiviere Virtual Environment
echo %BLUE%[INFO]%NC% Aktiviere Virtual Environment...
call .venv\Scripts\activate.bat

:: Prüfe ob .env vorhanden ist
if not exist ".env" (
    echo %YELLOW%[WARNING]%NC% .env Datei nicht gefunden!
    echo Google Maps API Key möglicherweise nicht konfiguriert.
    echo.
)

:: Funktion: Verfügbaren Port finden
:find_available_port
set "PORT=5000"
for %%p in (5000 5001 5002 5003 5004 5005 8080) do (
    netstat -an | findstr ":%%p " >nul 2>&1
    if errorlevel 1 (
        set "PORT=%%p"
        goto :port_found
    )
)
:port_found

:: App starten
echo %PURPLE%Anwendung starten%NC%
echo.
echo %GREEN%[SUCCESS]%NC% Starte Versicherungsmakler Finder auf Port !PORT!
echo.
echo 🌐 URL: http://localhost:!PORT!
echo 🔧 API Config: http://localhost:!PORT!/api/test
echo 📊 Broker Suche: http://localhost:!PORT!/
echo.
echo %YELLOW%[INFO]%NC% Drücke Ctrl+C um die Anwendung zu stoppen
echo.

:: Port als Umgebungsvariable setzen
set "PORT=!PORT!"

:: Prüfe ob Gunicorn verfügbar ist für Produktionsstart
if "%1"=="--production" (
    where gunicorn >nul 2>&1
    if not errorlevel 1 (
        echo %BLUE%[INFO]%NC% Starte mit Gunicorn ^(Produktion^)...
        gunicorn --workers 2 --bind 0.0.0.0:!PORT! app:app
    ) else (
        echo %YELLOW%[WARNING]%NC% Gunicorn nicht gefunden - starte Flask Entwicklungsserver...
        python app.py
    )
) else (
    echo %BLUE%[INFO]%NC% Starte Flask Entwicklungsserver...
    python app.py
)

:: Wenn wir hier ankommen, wurde die App beendet
echo.
echo %GREEN%[INFO]%NC% Anwendung beendet.
pause
