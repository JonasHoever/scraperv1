# 🚀 Versicherungsmakler Finder - Script Übersicht

Dieses Verzeichnis enthält verschiedene Scripts für die einfache Installation und den Start der Versicherungsmakler Finder Webapp.

## 📋 Verfügbare Scripts

### 1. Installation Scripts (vollständig)

#### `install.sh` (macOS/Linux)
```bash
# Vollständige Installation und Start
./install.sh

# Nur Installation ohne Start
./install.sh --install

# Nur starten (Virtual Environment muss existieren)
./install.sh --start

# Produktionsserver starten
./install.sh --production

# Tests ausführen
./install.sh --test

# Hilfe anzeigen
./install.sh --help
```

#### `install.bat` (Windows)
```batch
rem Vollständige Installation und Start
install.bat

rem Nur Installation ohne Start
install.bat --install

rem Nur starten (Virtual Environment muss existieren)
install.bat --start

rem Produktionsserver starten
install.bat --production

rem Tests ausführen
install.bat --test

rem Hilfe anzeigen
install.bat --help
```

### 2. Start Scripts (nur starten)

#### `start.sh` (macOS/Linux)
```bash
# App starten (Entwicklungsserver)
./start.sh

# App starten (Produktionsserver mit Gunicorn)
./start.sh --production

# Hilfe anzeigen
./start.sh --help
```

#### `start.bat` (Windows)
```batch
rem App starten (Entwicklungsserver)
start.bat

rem App starten (Produktionsserver mit Gunicorn)
start.bat --production
```

## 🎯 Empfohlener Workflow

### Erste Installation
1. **Vollständige Einrichtung:**
   - Linux/macOS: `./install.sh`
   - Windows: `install.bat`

2. **Das Script führt automatisch aus:**
   - ✅ Systemvoraussetzungen prüfen (Python, pip)
   - ✅ Virtual Environment erstellen
   - ✅ Dependencies installieren
   - ✅ .env Datei konfigurieren
   - ✅ Google Maps API Key einrichten
   - ✅ Anwendung testen
   - ✅ App starten

### Spätere Verwendung
Nach der ersten Installation kannst du einfach die Start-Scripts verwenden:

- Linux/macOS: `./start.sh`
- Windows: `start.bat`

## 🔧 Was die Scripts machen

### Installation Scripts Features:
- **🔍 Systemcheck**: Automatische Prüfung von Python, pip und Git
- **📦 Virtual Environment**: Erstellt und aktiviert isolierte Python-Umgebung
- **⚙️ Dependencies**: Installiert alle benötigten Python-Pakete
- **🔑 API Setup**: Interaktive Konfiguration des Google Maps API Keys
- **✅ Testing**: Führt Funktionsprüfungen durch
- **🌐 Smart Port**: Findet automatisch freie Ports (5000-5005, 8080)
- **🎨 Farbige Ausgabe**: Übersichtliche und gut lesbare Fortschrittsanzeige
- **🛡️ Error Handling**: Robuste Fehlerbehandlung und Recovery

### Start Scripts Features:
- **⚡ Schnellstart**: Direkter App-Start ohne Installation
- **🔧 Environment Check**: Prüft Virtual Environment und Projektdateien
- **🌐 Port Management**: Automatische Port-Erkennung
- **🏭 Production Mode**: Optional mit Gunicorn für Produktionsumgebung
- **📊 Status Display**: Zeigt App-URLs und wichtige Informationen

## 📂 Nach der Installation

Die App ist verfügbar unter:
- **🌐 Hauptanwendung**: `http://localhost:PORT/`
- **🔧 API Test Interface**: `http://localhost:PORT/api/test`
- **📋 API Dokumentation**: `API_CONFIG.md`

## 🛠️ Manuelle Installation (falls Scripts nicht funktionieren)

```bash
# 1. Virtual Environment erstellen
python3 -m venv .venv

# 2. Aktivieren
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate.bat

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. .env Datei erstellen und konfigurieren
cp .env.example .env
# Bearbeite .env und füge Google Maps API Key ein

# 5. App starten
python app.py
```

## 📞 Support

Bei Problemen:
1. Prüfe die Script-Ausgabe auf Fehlermeldungen
2. Stelle sicher, dass Python 3.8+ installiert ist
3. Überprüfe deine .env Konfiguration
4. Verwende `--help` für detaillierte Informationen

## 🎉 Schnelltest

Nach erfolgreicher Installation:
1. Öffne `http://localhost:PORT` im Browser
2. Gib eine deutsche Postleitzahl ein (z.B. 20095 für Hamburg)
3. Wähle einen Radius (z.B. 10 km)
4. Klicke auf "Makler suchen"
5. Die App findet und zeigt Versicherungsmakler in der Nähe!
