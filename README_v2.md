# Versicherungsmakler Finder 2.0 🚀

Eine erweiterte Flask Web-Anwendung zur intelligenten Suche nach Versicherungsmaklern mit modernen Animationen, Excel-Export und produktiven Extras.

## ✨ Neue Features in Version 2.0

### 🎨 Verbesserte Animationen & UI
- **Moderne CSS-Animationen** mit GPU-beschleunigten Transitionen
- **Glasmorphismus-Effekte** für moderne Optik
- **Interaktive Hover-Effekte** und Micro-Interactions
- **Responsive Design** für alle Bildschirmgrößen
- **Dark Mode** mit automatischer Speicherung der Benutzereinstellung
- **Page Loader** mit animierter Ladezeit-Anzeige

### 📊 Export-Funktionen
- **Excel-Export (.xlsx)** mit formatiertem Layout und mehreren Arbeitsblättern
- **Erweiteter JSON-Export** mit Metadaten und Versionsinformationen
- **Batch-Verarbeitung** für große Datenmengen
- **Download-Tracking** und Fortschrittsanzeige

### 🛠️ Produktive Extras
- **Service Worker** für Offline-Funktionalität
- **Keyboard Shortcuts** (Ctrl+K für Suche, Ctrl+E für Excel, etc.)
- **Geolocation API** zur automatischen Standorterkennung
- **Auto-Complete** für Ortsname-Eingaben
- **Suchverlauf** mit lokaler Speicherung
- **Performance Monitoring** und Ladezeit-Optimierung
- **Enhanced Form Validation** mit Live-Feedback
- **Toast Notifications** für bessere Benutzerführung

### 📱 Mobile Optimierungen
- **Touch-Gestures** und mobile Navigation
- **Progressive Web App (PWA)** Funktionalität
- **Optimierte Touch-Targets** für mobile Geräte
- **Responsive Breakpoints** für alle Gerätegrößen

## 🚀 Schnellstart

### Installation
```bash
# Repository klonen
git clone <repository-url>
cd scraperv1

# Virtual Environment erstellen (Windows)
python -m venv .venv
.venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Umgebungsvariablen konfigurieren
copy .env.example .env
# GOOGLE_MAPS_API_KEY in .env eintragen
```

### Starten
```bash
# Development Server
python app.py

# Oder mit dem Start-Script
start.bat

# Produktionsstart
start.bat --production
```

## 📁 Projektstruktur

```
scraperv1/
├── app.py                 # Hauptanwendung mit neuen Routes
├── requirements.txt       # Erweiterte Dependencies (openpyxl, pandas)
├── start.bat             # Windows Start-Script
├── install.bat           # Windows Installation-Script
├── static/
│   ├── css/
│   │   └── style.css     # Modernisierte CSS mit Animationen
│   ├── js/
│   │   └── app.js        # Erweiterte JavaScript-Funktionalität
│   └── sw.js             # Service Worker für Offline-Funktionalität
├── templates/
│   ├── base.html         # Erweiterte Base-Template
│   ├── index.html        # Modernisierte Startseite
│   ├── results.html      # Verbesserte Ergebnisseite
│   ├── api_test.html     # API-Test Interface
│   ├── 404.html          # Custom Error Pages
│   └── 500.html
└── utils/
    ├── __init__.py
    ├── geocoding.py      # Google Maps Integration
    ├── scraper.py        # Web-Scraping Funktionalität
    └── api_client.py     # API-Client für externe Integration
```

## 🔧 Neue API-Endpoints

### Export-Endpoints
- `GET /export/excel` - Excel-Export der letzten Suchergebnisse
- `GET /export/json` - Erweiteter JSON-Export mit Metadaten

### Bestehende Endpoints (erweitert)
- `POST /search` - Maklersuche (mit verbesserter Session-Speicherung)
- `POST /api/forward` - Datenweiterleitung an externe APIs
- `GET /api/test` - API-Test-Interface

## ⌨️ Keyboard Shortcuts

| Shortcut | Funktion |
|----------|----------|
| `Ctrl+K` | Suchfeld fokussieren |
| `Ctrl+E` | Excel-Export starten |
| `Ctrl+J` | JSON-Export starten |
| `Ctrl+A` | Alle Makler auswählen (Ergebnisseite) |
| `Alt+S` | Zur Suche springen |
| `Alt+G` | Standort per GPS ermitteln |
| `Esc` | Modals/Dropdowns schließen |

## 🎯 Features im Detail

### Excel-Export
Der Excel-Export erstellt eine formatierte .xlsx-Datei mit:
- **Makler-Daten** auf dem Hauptarbeitsblatt
- **Suchparameter** auf einem separaten Arbeitsblatt
- **Spalten-Formatierung** mit angepassten Breiten
- **Header-Styling** mit Corporate Design
- **Automatische Dateinamen** mit Zeitstempel

### Animationen & UX
- **GPU-beschleunigte CSS-Animationen** für flüssige Performance
- **Staggered Animations** für Kartenlisten
- **Micro-Interactions** bei Hover und Click
- **Loading States** mit modernen Spinner-Designs
- **Progress Bars** für lange Operationen
- **Ripple Effects** bei Button-Klicks

### Performance-Optimierungen
- **Service Worker** für Caching und Offline-Funktionalität
- **Lazy Loading** für Bilder und schwere Komponenten
- **Debounced Inputs** zur Vermeidung von API-Spam
- **Intersection Observer** für sichtbarkeitsbasierte Animationen
- **Resource Preloading** für kritische Assets

## 🔧 Konfiguration

### Umgebungsvariablen (.env)
```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
PORT=5000
API_SEND_FORMAT=enhanced
EXTERNAL_API_URL=https://your-api.com/endpoint
```

### Performance-Einstellungen
```python
# In app.py
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
```

## 🧪 Testing

### Lokaler Test
```bash
# API-Test Interface
http://localhost:5000/api/test

# Manuelle Tests
python test_app.py
python test_api.py
```

### Export-Tests
1. Führen Sie eine Suche durch
2. Testen Sie Excel-Export: `http://localhost:5000/export/excel`
3. Testen Sie JSON-Export: `http://localhost:5000/export/json`

## 📱 Progressive Web App (PWA)

Die Anwendung unterstützt PWA-Features:
- **Offline-Funktionalität** durch Service Worker
- **Installierbar** auf mobile Geräte und Desktop
- **Push-Benachrichtigungen** (optional konfigurierbar)
- **Background Sync** für Offline-Formulare

### PWA-Installation
1. Öffnen Sie die App in Chrome/Edge
2. Klicken Sie auf das "Installieren"-Icon in der Adressleiste
3. Die App wird als Desktop-App installiert

## 🚨 Troubleshooting

### Häufige Probleme

**Excel-Export funktioniert nicht:**
```bash
pip install openpyxl pandas
```

**Service Worker Fehler:**
- Prüfen Sie, ob `static/sw.js` existiert
- Öffnen Sie DevTools → Application → Service Workers

**Animationen ruckeln:**
- Reduzieren Sie `--transition-duration` in CSS
- Deaktivieren Sie Animationen bei `prefers-reduced-motion`

**Google Maps API Fehler:**
- Prüfen Sie Ihren API-Key in der `.env`-Datei
- Stellen Sie sicher, dass Places API aktiviert ist

## 📄 Changelog v2.0

### Neue Features
- ✅ Excel-Export mit Formatierung
- ✅ Erweiterte CSS-Animationen
- ✅ Service Worker für Offline-Funktionalität
- ✅ Dark Mode mit Theme-Toggle
- ✅ Keyboard Shortcuts
- ✅ Geolocation-Integration
- ✅ Auto-Complete für Ortseingabe
- ✅ Suchverlauf-Speicherung
- ✅ Performance-Monitoring
- ✅ Enhanced Form Validation
- ✅ Toast-Benachrichtigungen
- ✅ Mobile Optimierungen

### Verbesserungen
- 🔄 Modernisierte UI mit Glasmorphismus
- 🔄 Verbesserte API-Error-Handling
- 🔄 Optimierte Ladezeiten
- 🔄 Responsive Design-Überarbeitung
- 🔄 Enhanced Security Headers
- 🔄 Code-Struktur-Optimierung

## 🤝 Contributing

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Commit Ihre Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffnen Sie einen Pull Request

## 📝 License

Dieses Projekt steht unter der MIT License - siehe [LICENSE](LICENSE) Datei für Details.

## 🙏 Acknowledgments

- **Bootstrap 5.3** für das responsive Framework
- **Font Awesome 6.4** für die Icons
- **Google Maps API** für Geodaten
- **BeautifulSoup** für Web-Scraping
- **Flask** für das Backend-Framework
- **OpenPyXL & Pandas** für Excel-Export

---

Made with ❤️ for the Insurance Industry | Version 2.0 | 2024
