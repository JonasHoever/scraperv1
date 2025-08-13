🔧 **Dark Mode Navigation Fix** 
==============================

## Problem behoben:
❌ **Navigation-Links waren im Dark Mode schwarz/unsichtbar**
- Startseite
- Excel Upload  
- API Config
- Export (Dropdown)

## Was wurde geändert:

### CSS-Ergänzungen für Dark Mode:

```css
/* Navbar Brand */
[data-theme="dark"] .navbar-brand {
    color: #f8f9fa !important;
}

/* Navbar Links */
[data-theme="dark"] .navbar-nav .nav-link {
    color: #f8f9fa !important;
    opacity: 0.8;
    transition: all 0.3s ease;
}

/* Hover Effects */
[data-theme="dark"] .navbar-nav .nav-link:hover,
[data-theme="dark"] .navbar-nav .nav-link:focus {
    color: #ffffff !important;
    opacity: 1;
}

/* Active Link */
[data-theme="dark"] .navbar-nav .nav-link.active {
    color: var(--primary-color) !important;
    opacity: 1;
    font-weight: 600;
}

/* Dropdown Items */
[data-theme="dark"] .dropdown-item {
    color: #f8f9fa !important;
}

[data-theme="dark"] .dropdown-item:hover {
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.1);
}
```

## Erwartetes Verhalten:
✅ **Dark Mode Navigation jetzt sichtbar:**
- Navigation-Links sind hell/weiß auf dunklem Hintergrund
- Hover-Effekte funktionieren korrekt
- Active Links sind hervorgehoben (blau)
- Dropdown-Items sind ebenfalls sichtbar

## Test:
1. Seite laden: http://127.0.0.1:5000
2. Auf Mond-Symbol klicken (Dark Mode aktivieren)
3. Navigation sollte jetzt vollständig sichtbar sein

**Version:** CSS v2.2 mit Cache-Busting
**Status:** ✅ Behoben
