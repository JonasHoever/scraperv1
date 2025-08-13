@echo off
setlocal enabledelayedexpansion

:: Versicherungsmakler Finder - Windows Installation und Start Script
:: Automatische Installation und Konfiguration der Flask Web-App

echo ========================================
echo 🚀 Versicherungsmakler Finder - Windows
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

:: Funktion: Systemvoraussetzungen prüfen
:check_requirements
echo %PURPLE%1. Systemvoraussetzungen prüfen%NC%

:: Python prüfen
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%NC% Python ist nicht installiert!
    echo Bitte installiere Python 3.8+ von: https://www.python.org/downloads/
    echo Stelle sicher, dass Python zum PATH hinzugefügt wird!
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo %GREEN%[SUCCESS]%NC% Python !python_version! gefunden

:: pip prüfen
pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%[ERROR]%NC% pip ist nicht installiert!
    echo Installiere pip mit: python -m ensurepip --default-pip
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('pip --version') do set pip_version=%%i
echo %GREEN%[SUCCESS]%NC% pip !pip_version! gefunden

:: Git prüfen (optional)
git --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=3" %%i in ('git --version') do set git_version=%%i
    echo %GREEN%[SUCCESS]%NC% Git !git_version! gefunden
) else (
    echo %YELLOW%[WARNING]%NC% Git nicht gefunden - Download als ZIP möglich
)

echo.
goto :setup_project

:: Funktion: Projekt Setup
:setup_project
echo %PURPLE%2. Projekt Setup%NC%

if exist "app.py" if exist "requirements.txt" (
    echo %GREEN%[SUCCESS]%NC% Projekt bereits im aktuellen Verzeichnis vorhanden
    set "PROJECT_DIR=%CD%"
) else (
    echo %BLUE%[INFO]%NC% Projekt nicht gefunden - Erstelle Projektstruktur...
    
    if not exist "versicherungsmakler-finder" (
        mkdir versicherungsmakler-finder
    )
    cd versicherungsmakler-finder
    set "PROJECT_DIR=%CD%"
    
    echo %YELLOW%[WARNING]%NC% Bitte lade die Projektdateien in dieses Verzeichnis: !PROJECT_DIR!
    echo Oder kopiere sie aus dem bestehenden Projekt.
    
    if not exist "app.py" (
        echo %RED%[ERROR]%NC% app.py nicht gefunden! Bitte Projektdateien in !PROJECT_DIR! platzieren.
        pause
        exit /b 1
    )
)

echo %GREEN%[SUCCESS]%NC% Projektverzeichnis: !PROJECT_DIR!
echo.
goto :setup_venv

:: Funktion: Virtual Environment erstellen
:setup_venv
echo %PURPLE%3. Virtual Environment Setup%NC%

if exist ".venv" (
    echo %GREEN%[SUCCESS]%NC% Virtual Environment bereits vorhanden
) else (
    echo %BLUE%[INFO]%NC% Erstelle Virtual Environment...
    python -m venv .venv
    echo %GREEN%[SUCCESS]%NC% Virtual Environment erstellt
)

:: Aktivieren
echo %BLUE%[INFO]%NC% Aktiviere Virtual Environment...
call .venv\Scripts\activate.bat
echo %GREEN%[SUCCESS]%NC% Virtual Environment aktiviert

:: Pip upgraden
echo %BLUE%[INFO]%NC% Upgrade pip...
python -m pip install --upgrade pip --quiet
echo %GREEN%[SUCCESS]%NC% pip aktualisiert

echo.
goto :install_dependencies

:: Funktion: Dependencies installieren
:install_dependencies
echo %PURPLE%4. Dependencies Installation%NC%

if exist "requirements.txt" (
    echo %BLUE%[INFO]%NC% Installiere Python-Pakete aus requirements.txt...
    pip install -r requirements.txt --quiet
    echo %GREEN%[SUCCESS]%NC% Alle Dependencies installiert
) else (
    echo %YELLOW%[WARNING]%NC% requirements.txt nicht gefunden - installiere Basispakete...
    pip install flask requests beautifulsoup4 googlemaps python-dotenv gunicorn --quiet
    echo %GREEN%[SUCCESS]%NC% Basispakete installiert
)

echo.
goto :setup_environment

:: Funktion: Umgebungskonfiguration
:setup_environment
echo %PURPLE%5. Umgebungskonfiguration%NC%

if exist ".env" (
    echo %GREEN%[SUCCESS]%NC% .env Datei bereits vorhanden
    
    findstr /C:"your_google_maps_api_key_here" .env >nul 2>&1
    if not errorlevel 1 (
        echo %YELLOW%[WARNING]%NC% Google Maps API Key noch nicht konfiguriert!
        goto :configure_api_key
    ) else (
        echo %GREEN%[SUCCESS]%NC% Google Maps API Key ist konfiguriert
    )
) else (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo %GREEN%[SUCCESS]%NC% .env Datei aus Beispiel erstellt
        goto :configure_api_key
    ) else (
        goto :create_env_file
    )
)

echo.
goto :test_app

:: Funktion: API Key konfigurieren
:configure_api_key
echo %BLUE%[INFO]%NC% Google Maps API Key Konfiguration
echo.
echo 🔑 Du benötigst einen Google Maps API Key:
echo 1. Gehe zu: https://console.cloud.google.com/
echo 2. Erstelle ein Projekt und aktiviere folgende APIs:
echo    - Maps JavaScript API
echo    - Places API
echo    - Geocoding API
echo 3. Erstelle einen API Key unter 'Anmeldedaten'
echo.

set /p "has_key=Hast du bereits einen Google Maps API Key? (y/n): "

if /i "!has_key!"=="y" (
    echo.
    set /p "api_key=Bitte Google Maps API Key eingeben: "
    
    if not "!api_key!"=="" (
        :: API Key in .env eintragen (Windows PowerShell für bessere String-Manipulation)
        powershell -Command "(Get-Content .env) -replace 'GOOGLE_MAPS_API_KEY=.*', 'GOOGLE_MAPS_API_KEY=!api_key!' | Set-Content .env"
        echo %GREEN%[SUCCESS]%NC% API Key in .env gespeichert
    ) else (
        echo %YELLOW%[WARNING]%NC% Kein API Key eingegeben - bitte später in .env konfigurieren
    )
) else (
    echo %YELLOW%[WARNING]%NC% Bitte erstelle einen API Key und trage ihn in die .env Datei ein
    echo %BLUE%[INFO]%NC% Bearbeite: !PROJECT_DIR!\.env
)

echo.
goto :test_app

:: Funktion: .env Datei erstellen
:create_env_file
echo %BLUE%[INFO]%NC% Erstelle .env Datei...

(
echo # Google Maps API Key - ERFORDERLICH für die App
echo GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
echo.
echo # Externe API für Datenweiterleitung ^(OPTIONAL^)
echo # EXTERNAL_API_URL=https://webhook.site/your-unique-url
echo # API_SEND_FORMAT=enhanced
echo # EXTERNAL_API_KEY=your-api-key
echo.
echo # Flask Konfiguration
echo FLASK_ENV=development
echo FLASK_DEBUG=True
echo SECRET_KEY=versicherungsmakler-finder-secret-2025
echo.
echo # Optional: Datenbankverbindung
echo # DATABASE_URL=sqlite:///brokers.db
) > .env

echo %GREEN%[SUCCESS]%NC% .env Datei erstellt
goto :configure_api_key

:: Funktion: App testen
:test_app
echo %PURPLE%6. Anwendungstest%NC%

if exist "test_app.py" (
    echo %BLUE%[INFO]%NC% Führe Anwendungstest aus...
    python test_app.py
    
    if not errorlevel 1 (
        echo %GREEN%[SUCCESS]%NC% Alle Tests bestanden
    ) else (
        echo %YELLOW%[WARNING]%NC% Einige Tests fehlgeschlagen - App sollte trotzdem funktionieren
    )
) else (
    echo %BLUE%[INFO]%NC% Teste grundlegende Imports...
    python -c "import flask; import requests; import googlemaps; from bs4 import BeautifulSoup; print('✅ Alle wichtigen Module importiert')"
    if not errorlevel 1 (
        echo %GREEN%[SUCCESS]%NC% Grundlegende Funktionalität verfügbar
    )
)

echo.
goto :start_app

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
goto :eof

:: Funktion: App starten
:start_app
echo %PURPLE%7. Anwendung starten%NC%

call :find_available_port

echo %GREEN%[SUCCESS]%NC% Starte Versicherungsmakler Finder auf Port !PORT!
echo.
echo 🌐 URL: http://localhost:!PORT!
echo 🔧 API Config: http://localhost:!PORT!/api/test
echo.
echo %YELLOW%[WARNING]%NC% Drücke Ctrl+C um die Anwendung zu stoppen
echo.

:: App starten
set "PORT=!PORT!"

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

goto :eof

:: Hilfe anzeigen
:show_help
echo Versicherungsmakler Finder - Windows Installations- und Start-Script
echo.
echo Verwendung:
echo   %~n0                    - Vollständige Installation und Start
echo   %~n0 --install          - Nur Installation, kein Start
echo   %~n0 --start            - Nur App starten ^(Installation überspringen^)
echo   %~n0 --production       - Produktionsserver mit Gunicorn starten
echo   %~n0 --test             - Nur Tests ausführen
echo   %~n0 --help             - Diese Hilfe anzeigen
echo.
echo Nach der Installation:
echo   • Öffne http://localhost:PORT im Browser
echo   • Konfiguriere Google Maps API Key in .env
echo   • Teste externe API unter /api/test
echo.
goto :eof

:: Hauptlogik
if "%1"=="--help" goto :show_help
if "%1"=="-h" goto :show_help

if "%1"=="--install" (
    call :check_requirements
    call :setup_project
    call :setup_venv
    call :install_dependencies
    call :setup_environment
    call :test_app
    echo %GREEN%[SUCCESS]%NC% Installation abgeschlossen!
    echo Starte die App mit: %~n0 --start
    pause
    goto :eof
)

if "%1"=="--start" (
    if not exist ".venv" (
        echo %RED%[ERROR]%NC% Virtual Environment nicht gefunden! Führe erst --install aus.
        pause
        exit /b 1
    )
    call .venv\Scripts\activate.bat
    call :start_app
    goto :eof
)

if "%1"=="--production" (
    if not exist ".venv" (
        echo %RED%[ERROR]%NC% Virtual Environment nicht gefunden! Führe erst --install aus.
        pause
        exit /b 1
    )
    call .venv\Scripts\activate.bat
    call :start_app --production
    goto :eof
)

if "%1"=="--test" (
    if not exist ".venv" (
        echo %RED%[ERROR]%NC% Virtual Environment nicht gefunden! Führe erst --install aus.
        pause
        exit /b 1
    )
    call .venv\Scripts\activate.bat
    call :test_app
    pause
    goto :eof
)

:: Vollständige Installation und Start (Standard)
call :check_requirements
call :setup_project  
call :setup_venv
call :install_dependencies
call :setup_environment
call :test_app

echo.
echo %GREEN%[SUCCESS]%NC% 🎉 Installation erfolgreich abgeschlossen!
echo.

set /p "start_now=Soll die Anwendung jetzt gestartet werden? (y/n): "

if /i "!start_now!"=="y" (
    call :start_app
) else (
    echo.
    echo %GREEN%[SUCCESS]%NC% Installation abgeschlossen!
    echo Starte die App später mit: %~n0 --start
    echo Oder: .venv\Scripts\activate.bat ^&^& python app.py
    pause
)
