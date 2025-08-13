#!/bin/bash

# Deployment Script für Versicherungsmakler Finder
# Führt alle notwendigen Schritte für die Produktionsbereitstellung aus

set -e  # Beende bei Fehlern

echo "🚀 Deploying Versicherungsmakler Finder"
echo "======================================"

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# 1. Umgebung prüfen
print_status "Prüfe Umgebung..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 ist nicht installiert!"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    print_error "pip3 ist nicht installiert!"
    exit 1
fi

print_success "Python und pip sind verfügbar"

# 2. Virtual Environment erstellen/aktivieren
print_status "Konfiguriere Virtual Environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "Virtual Environment erstellt"
else
    print_success "Virtual Environment bereits vorhanden"
fi

source .venv/bin/activate
print_success "Virtual Environment aktiviert"

# 3. Dependencies installieren
print_status "Installiere Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installiert"

# 4. Umgebungskonfiguration
print_status "Prüfe Umgebungskonfiguration..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning ".env Datei aus Beispiel erstellt - bitte API Keys eintragen!"
    else
        print_error ".env.example Datei nicht gefunden!"
        exit 1
    fi
else
    print_success ".env Datei vorhanden"
fi

# 5. Überprüfe kritische Konfigurationen
if ! grep -q "your_google_maps_api_key_here" .env; then
    print_success "Google Maps API Key scheint konfiguriert zu sein"
else
    print_warning "Google Maps API Key noch nicht konfiguriert!"
    echo "Bitte trage deinen Google Maps API Key in die .env Datei ein:"
    echo "GOOGLE_MAPS_API_KEY=your_actual_api_key"
fi

# 6. Teste die Anwendung
print_status "Teste Anwendung..."
python test_app.py

if [ $? -eq 0 ]; then
    print_success "Alle Tests bestanden"
else
    print_error "Tests fehlgeschlagen!"
    exit 1
fi

# 7. Erstelle Produktionsordner (optional)
PROD_DIR="production"
if [ "$1" = "production" ]; then
    print_status "Erstelle Produktionsumgebung..."
    
    mkdir -p $PROD_DIR
    
    # Kopiere notwendige Dateien
    cp -r app.py utils/ templates/ static/ requirements.txt .env.example $PROD_DIR/
    cp .env $PROD_DIR/ 2>/dev/null || print_warning ".env nicht kopiert - bitte manuell erstellen"
    
    print_success "Produktionsumgebung in '$PROD_DIR' erstellt"
fi

# 8. Starte Entwicklungsserver oder Produktionsserver
if [ "$1" = "production" ]; then
    print_status "Starte Produktionsserver mit Gunicorn..."
    echo "gunicorn --workers 4 --bind 0.0.0.0:5000 app:app"
    print_warning "Führe den obigen Befehl aus, um den Produktionsserver zu starten"
else
    print_status "Starte Entwicklungsserver..."
    echo ""
    echo "Die Anwendung ist bereit!"
    echo ""
    echo "🌐 Starte mit: python app.py"
    echo "📱 Öffne: http://localhost:5000"
    echo ""
    echo "Für Produktionsdeployment:"
    echo "./deploy.sh production"
    echo ""
    
    # Optional: Server automatisch starten
    read -p "Soll der Entwicklungsserver jetzt gestartet werden? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Starte Flask Entwicklungsserver..."
        python app.py
    fi
fi

print_success "Deployment abgeschlossen!"

# 9. Zeige nützliche Informationen
echo ""
echo "📋 Nützliche Befehle:"
echo "====================="
echo "Entwicklungsserver starten:    python app.py"
echo "Tests ausführen:               python test_app.py"
echo "Produktionsserver starten:     gunicorn --workers 4 --bind 0.0.0.0:5000 app:app"
echo "Dependencies aktualisieren:    pip install -r requirements.txt"
echo "Virtual Environment aktivieren: source .venv/bin/activate"
echo ""
echo "📚 Dokumentation:"
echo "=================="
echo "README.md       - Vollständige Dokumentation"
echo ".env.example    - Umgebungsvariablen Beispiel"
echo "test_app.py     - Test und Demo Script"
echo ""

exit 0
