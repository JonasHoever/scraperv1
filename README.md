# Versicherungsmakler Finder

Eine Flask-Webapp zum Finden von Versicherungsmaklern in einem bestimmten Umkreis mit Web-Scraping und API-Integration.

## Features

- **Standortbasierte Suche**: Eingabe von Postleitzahl oder Ortsnamen mit Radius in km
- **Makler-Informationen**: Name, Ansprechperson, Telefon, E-Mail, Website
- **Web-Scraping**: Automatisches Extrahieren von Details von Makler-Webseiten
- **JSON API**: Weiterleitung der Daten an externe APIs
- **Deutsche Lokalisierung**: Optimiert für deutsche Standorte und Versicherungsmakler

## 🚀 Schnellstart (Automatische Installation)

### Windows
```batch
# Vollständige Installation und Start
install.bat

# Nur Installation
install.bat --install

# Nur App starten
start.bat
```

### macOS/Linux
```bash
# Vollständige Installation und Start
./install.sh

# Nur Installation
./install.sh --install

# Nur App starten
./start.sh
```

## 📋 Manuelle Installation

1. Python 3.8+ installieren
2. Repository klonen oder herunterladen
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Umgebungsvariablen konfigurieren:
   ```bash
   cp .env.example .env
   # .env Datei mit Google Maps API Key bearbeiten
   ```

## Konfiguration

Erstelle eine `.env` Datei mit folgenden Variablen:

```bash
# Google Maps API Key (ERFORDERLICH)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Externe API Konfiguration (OPTIONAL)
EXTERNAL_API_URL=https://your-external-api.com/endpoint
API_SEND_FORMAT=enhanced
EXTERNAL_API_KEY=your-api-key
# ODER
EXTERNAL_API_TOKEN=Bearer your-jwt-token

# Flask Konfiguration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
```

### API Test URLs (kostenlos)

Für Tests der externen API-Integration:
- **Webhook.site**: https://webhook.site/
- **RequestBin**: https://requestbin.com/
- **Pipedream**: https://pipedream.com/

## Verwendung

### Entwicklungsserver starten:
```bash
python app.py
```

### Produktionsserver:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

## API Endpoints

- `GET /` - Hauptseite mit Suchformular
- `POST /search` - Suche nach Versicherungsmaklern
- `POST /api/forward` - Weiterleitung von Makler-Daten an externe API
- `GET /api/brokers` - JSON-Liste aller gefundenen Makler
- `GET /api/test` - API-Konfiguration und Test-Interface
- `POST /api/test` - Test der externen API-Verbindung
- `GET /api/config` - Aktuelle API-Konfiguration anzeigen

## API Integration & JSON Formate

### Unterstützte Formate (API_SEND_FORMAT)

#### 1. **Basic Format** (`API_SEND_FORMAT=basic`)
```json
{
  "name": "Makler Name",
  "phone": "+49 30 12345678",
  "website": "https://example.com",
  "address": "Straße 123, Berlin",
  "rating": 4.8
}
```

#### 2. **Enhanced Format** (`API_SEND_FORMAT=enhanced`) - Standard
```json
{
  "broker_info": {
    "name": "Makler Name",
    "contact_person": "Max Mustermann",
    "address": "Straße 123, Berlin",
    "phone": "+49 30 12345678",
    "email": "info@makler.de",
    "website": "https://makler.de",
    "rating": 4.8,
    "total_reviews": 96,
    "google_place_id": "ChIJ..."
  },
  "scraped_data": {
    "contact_person": "Max Mustermann",
    "email": "info@makler.de",
    "scraped_successfully": true
  },
  "metadata": {
    "source": "Versicherungsmakler-Finder",
    "scraped_at": "2025-08-13T10:57:00Z",
    "data_quality": "high"
  }
}
```

#### 3. **Custom Format** (`API_SEND_FORMAT=custom`)
```json
{
  "companyName": "Makler Name",
  "contactPerson": "Max Mustermann",
  "phoneNumber": "+49 30 12345678",
  "emailAddress": "info@makler.de",
  "industry": "Versicherungsmakler",
  "lastUpdated": "2025-08-13T10:57:00Z"
}
```

## 📁 Verfügbare Scripts

### Installation Scripts

| Script | Plattform | Beschreibung |
|--------|-----------|--------------|
| `install.sh` | macOS/Linux | Vollständige automatische Installation und Start |
| `install.bat` | Windows | Vollständige automatische Installation und Start |

**Verfügbare Optionen:**
- `--install` - Nur Installation, kein automatischer Start
- `--start` - Nur App starten (Installation überspringen)
- `--production` - Produktionsserver mit Gunicorn starten
- `--test` - Nur Tests ausführen
- `--help` - Hilfe anzeigen

### Start Scripts (nach Installation)

| Script | Plattform | Beschreibung |
|--------|-----------|--------------|
| `start.sh` | macOS/Linux | Schneller App-Start ohne Installation |
| `start.bat` | Windows | Schneller App-Start ohne Installation |

**Verfügbare Optionen:**
- Standard: Entwicklungsserver starten
- `--production` - Produktionsserver mit Gunicorn starten
- `--help` - Hilfe anzeigen

### Beispiel-Verwendung

```bash
# Erste Installation (automatisch)
./install.sh

# App später starten
./start.sh

# Produktionsstart
./start.sh --production
```

```batch
rem Windows Erste Installation
install.bat

rem App später starten
start.bat

rem Produktionsstart  
start.bat --production
```

## Projektstruktur

```
scrum/
├── app.py                 # Haupt-Flask-Anwendung
├── requirements.txt       # Python-Abhängigkeiten
├── .env.example          # Beispiel-Umgebungsvariablen
├── install.sh            # Linux/macOS Installation Script
├── install.bat           # Windows Installation Script
├── start.sh              # Linux/macOS Start Script
├── start.bat             # Windows Start Script
├── static/               # Statische Dateien (CSS, JS)
├── templates/            # HTML-Templates
└── utils/                # Hilfsfunktionen
    ├── scraper.py        # Web-Scraping-Funktionen
    ├── geocoding.py      # Standort-Funktionen
    └── api_client.py     # Externe API-Integration
```

## Lizenz

MIT License
