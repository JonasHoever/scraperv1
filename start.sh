#!/bin/bash

# Versicherungsmakler Finder - Start Script
# Schneller Start der Flask Web-App ohne Installation

set -e  # Beende bei Fehlern

echo "🚀 Versicherungsmakler Finder - Start"
echo "===================================="

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

# Prüfe ob Virtual Environment vorhanden ist
if [ ! -d ".venv" ]; then
    print_error "Virtual Environment nicht gefunden!"
    echo "Führe zuerst das Installations-Script aus: ./install.sh --install"
    echo "Oder verwende: ./install.sh für vollständige Installation"
    exit 1
fi

# Prüfe ob app.py vorhanden ist
if [ ! -f "app.py" ]; then
    print_error "app.py nicht gefunden!"
    echo "Stelle sicher, dass du im richtigen Projektverzeichnis bist."
    exit 1
fi

# Aktiviere Virtual Environment
print_status "Aktiviere Virtual Environment..."
source .venv/bin/activate
print_success "Virtual Environment aktiviert"

# Prüfe ob .env vorhanden ist
if [ ! -f ".env" ]; then
    print_warning ".env Datei nicht gefunden!"
    print_warning "Google Maps API Key möglicherweise nicht konfiguriert."
    echo ""
fi

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

# App starten
start_app() {
    print_header "Anwendung starten"
    echo ""
    
    # Verfügbaren Port finden
    PORT=$(find_available_port)
    
    print_success "Starte Versicherungsmakler Finder auf Port $PORT"
    echo ""
    echo "🌐 URL: http://localhost:$PORT"
    echo "🔧 API Config: http://localhost:$PORT/api/test"
    echo "📊 Broker Suche: http://localhost:$PORT/"
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
    echo "Versicherungsmakler Finder - Start-Script"
    echo ""
    echo "Verwendung:"
    echo "  $0                    - App im Entwicklungsmodus starten"
    echo "  $0 --production       - App im Produktionsmodus mit Gunicorn starten"
    echo "  $0 --help             - Diese Hilfe anzeigen"
    echo ""
    echo "Voraussetzungen:"
    echo "  • Virtual Environment muss installiert sein (.venv/)"
    echo "  • app.py muss im aktuellen Verzeichnis vorhanden sein"
    echo "  • .env Datei sollte konfiguriert sein (Google Maps API Key)"
    echo ""
    echo "Erste Installation:"
    echo "  • Verwende ./install.sh für vollständige Installation"
    echo "  • Oder ./install.sh --install für nur Installation ohne Start"
    echo ""
}

# Funktion: Cleanup bei Unterbrechung
cleanup() {
    print_warning "Anwendung unterbrochen"
    echo ""
    print_status "Anwendung beendet."
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
        --production)
            start_app --production
            ;;
        *)
            start_app
            ;;
    esac
}

# Script starten
main "$@"
