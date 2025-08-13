#!/usr/bin/env python3
"""
Test-Script für Google Maps API Konfiguration
Dieses Script überprüft, ob der API Key korrekt konfiguriert ist.
"""

import os
import sys
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

def test_api_key_config():
    """Testet die API Key Konfiguration"""
    print("🔍 Teste Google Maps API Konfiguration...\n")
    
    # API Key prüfen
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        print("❌ FEHLER: GOOGLE_MAPS_API_KEY nicht gefunden in .env Datei")
        return False
    
    if api_key == 'your_google_maps_api_key_here':
        print("❌ FEHLER: GOOGLE_MAPS_API_KEY noch nicht konfiguriert!")
        print("   Bitte ersetze 'your_google_maps_api_key_here' mit deinem echten API Key")
        return False
    
    print(f"✅ API Key gefunden: {api_key[:8]}...")
    
    # Teste API-Verbindung
    try:
        import googlemaps
        print("✅ googlemaps-Bibliothek ist installiert")
        
        gmaps = googlemaps.Client(key=api_key)
        print("✅ Google Maps Client erstellt")
        
        # Teste einfache Geocoding-Anfrage
        print("🔄 Teste Geocoding mit 'Berlin'...")
        result = gmaps.geocode('Berlin, Deutschland')
        
        if result:
            location = result[0]['geometry']['location']
            print(f"✅ Geocoding erfolgreich!")
            print(f"   Berlin Koordinaten: {location['lat']}, {location['lng']}")
            
            # Teste Places API
            print("🔄 Teste Places API...")
            places_result = gmaps.places_nearby(
                location=location,
                radius=1000,
                keyword='Versicherung'
            )
            
            if places_result.get('results'):
                print(f"✅ Places API funktioniert! {len(places_result['results'])} Orte gefunden")
                return True
            else:
                print("⚠️  Places API gibt keine Ergebnisse zurück")
                return False
        else:
            print("❌ Geocoding fehlgeschlagen")
            return False
            
    except ImportError:
        print("❌ googlemaps-Bibliothek nicht installiert")
        print("   Führe aus: pip install googlemaps")
        return False
    except Exception as e:
        print(f"❌ API-Test fehlgeschlagen: {str(e)}")
        print("   Mögliche Ursachen:")
        print("   - API Key ist ungültig")
        print("   - APIs sind nicht aktiviert")
        print("   - Quota überschritten")
        return False

def show_setup_instructions():
    """Zeigt Setup-Anweisungen"""
    print("\n" + "="*50)
    print("📋 SETUP ANWEISUNGEN")
    print("="*50)
    print("1. Google Cloud Console öffnen:")
    print("   https://console.cloud.google.com/")
    print()
    print("2. Neues Projekt erstellen oder bestehendes auswählen")
    print()
    print("3. Folgende APIs aktivieren:")
    print("   - Maps JavaScript API")
    print("   - Places API")
    print("   - Geocoding API")
    print()
    print("4. API Key erstellen:")
    print("   APIs & Services → Credentials → Create Credentials → API Key")
    print()
    print("5. API Key in .env Datei eintragen:")
    print("   GOOGLE_MAPS_API_KEY=dein_echter_api_key")
    print()
    print("6. Dieses Script erneut ausführen:")
    print("   python test_api.py")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Google Maps API Test")
    print("="*30)
    
    success = test_api_key_config()
    
    if success:
        print("\n🎉 ALLES BEREIT!")
        print("Die Flask-App sollte jetzt funktionieren.")
        print("Starte die App mit: python app.py")
    else:
        show_setup_instructions()
        sys.exit(1)
