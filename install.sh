#!/bin/bash

# Versicherungsmakler Finder - Installation und Start Script
# Automatische Installation und Konfiguration der Flask Web-App

set -e  # Beende bei Fehlern

echo "🚀 Versicherungsmakler Finder - Installation & Start"
echo "=================================================="

# Farben für bessere Lesbarkeit
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Funktion: Systemvoraussetzungen prüfen
check_requirements() {
    print_header "1. Systemvoraussetzungen prüfen"
    
    # Python 3 prüfen
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 ist nicht installiert!"
        echo "Bitte installiere Python 3.8+ von: https://www.python.org/downloads/"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python $python_version gefunden"
    
    # pip prüfen
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 ist nicht installiert!"
        echo "Installiere pip mit: python3 -m ensurepip --default-pip"
        exit 1
    fi
    
    pip_version=$(pip3 --version | cut -d' ' -f2)
    print_success "pip $pip_version gefunden"
    
    # Git prüfen (optional)
    if command -v git &> /dev/null; then
        git_version=$(git --version | cut -d' ' -f3)
        print_success "Git $git_version gefunden"
    else
        print_warning "Git nicht gefunden - Download als ZIP möglich"
    fi
    
    echo ""
}

# Funktion: Projekt herunterladen oder verwenden
setup_project() {
    print_header "2. Projekt Setup"
    
    if [ -f "app.py" ] && [ -f "requirements.txt" ]; then
        print_success "Projekt bereits im aktuellen Verzeichnis vorhanden"
        PROJECT_DIR=$(pwd)
    else
        print_status "Projekt nicht gefunden - Erstelle Projektstruktur..."
        
        # Falls das Projekt nicht vorhanden ist, erstelle minimale Struktur
        if [ ! -d "versicherungsmakler-finder" ]; then
            mkdir versicherungsmakler-finder
        fi
        cd versicherungsmakler-finder
        PROJECT_DIR=$(pwd)
        
        print_warning "Bitte lade die Projektdateien in dieses Verzeichnis: $PROJECT_DIR"
        echo "Oder kopiere sie aus dem bestehenden Projekt."
        
        # Überprüfen ob Dateien nach kurzer Wartezeit vorhanden sind
        if [ ! -f "app.py" ]; then
            print_error "app.py nicht gefunden! Bitte Projektdateien in $PROJECT_DIR platzieren."
            exit 1
        fi
    fi
    
    print_success "Projektverzeichnis: $PROJECT_DIR"
    echo ""
}

# Funktion: Virtual Environment erstellen
setup_venv() {
    print_header "3. Virtual Environment Setup"
    
    if [ -d ".venv" ]; then
        print_success "Virtual Environment bereits vorhanden"
    else
        print_status "Erstelle Virtual Environment..."
        python3 -m venv .venv
        print_success "Virtual Environment erstellt"
    fi
    
    # Aktivieren
    print_status "Aktiviere Virtual Environment..."
    source .venv/bin/activate
    print_success "Virtual Environment aktiviert"
    
    # Pip upgraden
    print_status "Upgrade pip..."
    pip install --upgrade pip --quiet
    print_success "pip aktualisiert"
    
    echo ""
}

# Funktion: Dependencies installieren
install_dependencies() {
    print_header "4. Dependencies Installation"
    
    if [ -f "requirements.txt" ]; then
        print_status "Installiere Python-Pakete aus requirements.txt..."
        pip install -r requirements.txt --quiet
        print_success "Alle Dependencies installiert"
    else
        print_warning "requirements.txt nicht gefunden - installiere Basispakete..."
        pip install flask requests beautifulsoup4 googlemaps python-dotenv gunicorn --quiet
        print_success "Basispakete installiert"
    fi
    
    echo ""
}

# Funktion: Umgebungskonfiguration
setup_environment() {
    print_header "5. Umgebungskonfiguration"
    
    if [ -f ".env" ]; then
        print_success ".env Datei bereits vorhanden"
        
        # Prüfe ob Google Maps API Key konfiguriert ist
        if grep -q "your_google_maps_api_key_here\|GOOGLE_MAPS_API_KEY=$" .env; then
            print_warning "Google Maps API Key noch nicht konfiguriert!"
            configure_api_key
        else
            print_success "Google Maps API Key ist konfiguriert"
        fi
    else
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success ".env Datei aus Beispiel erstellt"
            configure_api_key
        else
            create_env_file
        fi
    fi
    
    echo ""
}

# Funktion: API Key konfigurieren
configure_api_key() {
    print_status "Google Maps API Key Konfiguration"
    echo ""
    echo "🔑 Du benötigst einen Google Maps API Key:"
    echo "1. Gehe zu: https://console.cloud.google.com/"
    echo "2. Erstelle ein Projekt und aktiviere folgende APIs:"
    echo "   - Maps JavaScript API"
    echo "   - Places API"
    echo "   - Geocoding API"
    echo "3. Erstelle einen API Key unter 'Anmeldedaten'"
    echo ""
    
    read -p "Hast du bereits einen Google Maps API Key? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        read -p "Bitte Google Maps API Key eingeben: " api_key
        
        if [ ! -z "$api_key" ]; then
            # API Key in .env eintragen
            sed -i.bak "s/GOOGLE_MAPS_API_KEY=.*/GOOGLE_MAPS_API_KEY=$api_key/" .env
            print_success "API Key in .env gespeichert"
        else
            print_warning "Kein API Key eingegeben - bitte später in .env konfigurieren"
        fi
    else
        print_warning "Bitte erstelle einen API Key und trage ihn in die .env Datei ein"
        print_status "Bearbeite: $PROJECT_DIR/.env"
    fi
}

# Funktion: .env Datei erstellen
create_env_file() {
    print_status "Erstelle .env Datei..."
    
    cat > .env << 'EOF'
# Google Maps API Key - ERFORDERLICH für die App
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Externe API für Datenweiterleitung (OPTIONAL)
# EXTERNAL_API_URL=https://webhook.site/your-unique-url
# API_SEND_FORMAT=enhanced
# EXTERNAL_API_KEY=your-api-key

# Flask Konfiguration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=versicherungsmakler-finder-secret-2025

# Optional: Datenbankverbindung
# DATABASE_URL=sqlite:///brokers.db
EOF
    
    print_success ".env Datei erstellt"
    configure_api_key
}

# Funktion: App testen
test_app() {
    print_header "6. Anwendungstest"
    
    if [ -f "test_app.py" ]; then
        print_status "Führe Anwendungstest aus..."
        python test_app.py
        
        if [ $? -eq 0 ]; then
            print_success "Alle Tests bestanden"
        else
            print_warning "Einige Tests fehlgeschlagen - App sollte trotzdem funktionieren"
        fi
    else
        print_status "Teste grundlegende Imports..."
        python -c "
import flask
import requests
import googlemaps
from bs4 import BeautifulSoup
print('✅ Alle wichtigen Module importiert')
"
        print_success "Grundlegende Funktionalität verfügbar"
    fi
    
    echo ""
}

# Funktion: Verfügbaren Port finden
find_available_port() {
    for port in 5000 5001 5002 5003 5004 5005; do
        if ! lsof -i :$port &> /dev/null; then
            echo $port
            return
        fi
    done
    echo 8080  # Fallback
}

# Funktion: App starten
start_app() {
    print_header "7. Anwendung starten"
    
    # Verfügbaren Port finden
    PORT=$(find_available_port)
    
    print_success "Starte Versicherungsmakler Finder auf Port $PORT"
    echo ""
    echo "🌐 URL: http://localhost:$PORT"
    echo "🔧 API Config: http://localhost:$PORT/api/test"
    echo ""
    print_warning "Drücke Ctrl+C um die Anwendung zu stoppen"
    echo ""
    
    # App starten
    export PORT=$PORT
    
    if command -v gunicorn &> /dev/null && [ "$1" = "--production" ]; then
        print_status "Starte mit Gunicorn (Produktion)..."
        gunicorn --workers 2 --bind 0.0.0.0:$PORT app:app
    else
        print_status "Starte Flask Entwicklungsserver..."
        python app.py
    fi
}

# Funktion: Hilfe anzeigen
show_help() {
    echo "Versicherungsmakler Finder - Installations- und Start-Script"
    echo ""
    echo "Verwendung:"
    echo "  $0                    - Vollständige Installation und Start"
    echo "  $0 --install          - Nur Installation, kein Start"
    echo "  $0 --start            - Nur App starten (Installation überspringen)"
    echo "  $0 --production       - Produktionsserver mit Gunicorn starten"
    echo "  $0 --test             - Nur Tests ausführen"
    echo "  $0 --help             - Diese Hilfe anzeigen"
    echo ""
    echo "Nach der Installation:"
    echo "  • Öffne http://localhost:PORT im Browser"
    echo "  • Konfiguriere Google Maps API Key in .env"
    echo "  • Teste externe API unter /api/test"
    echo ""
}

# Funktion: Cleanup bei Unterbrechung
cleanup() {
    print_warning "Installation/Start unterbrochen"
    if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
        deactivate 2>/dev/null || true
    fi
    exit 130
}

# Signal Handler für saubere Unterbrechung
trap cleanup SIGINT SIGTERM

# Hauptfunktion
main() {
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --install)
            check_requirements
            setup_project
            setup_venv
            install_dependencies
            setup_environment
            test_app
            print_success "Installation abgeschlossen!"
            echo "Starte die App mit: $0 --start"
            ;;
        --start)
            if [ ! -d ".venv" ]; then
                print_error "Virtual Environment nicht gefunden! Führe erst --install aus."
                exit 1
            fi
            source .venv/bin/activate
            start_app
            ;;
        --production)
            if [ ! -d ".venv" ]; then
                print_error "Virtual Environment nicht gefunden! Führe erst --install aus."
                exit 1
            fi
            source .venv/bin/activate
            start_app --production
            ;;
        --test)
            if [ ! -d ".venv" ]; then
                print_error "Virtual Environment nicht gefunden! Führe erst --install aus."
                exit 1
            fi
            source .venv/bin/activate
            test_app
            ;;
        *)
            # Vollständige Installation und Start
            check_requirements
            setup_project
            setup_venv
            install_dependencies
            setup_environment
            test_app
            
            echo ""
            print_success "🎉 Installation erfolgreich abgeschlossen!"
            echo ""
            
            read -p "Soll die Anwendung jetzt gestartet werden? (y/n): " -n 1 -r
            echo
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                start_app
            else
                echo ""
                print_success "Installation abgeschlossen!"
                echo "Starte die App später mit: $0 --start"
                echo "Oder: source .venv/bin/activate && python app.py"
            fi
            ;;
    esac
}

# Script starten
main "$@"
