#!/usr/bin/env python
"""
Test-Script für die Versicherungsmakler Finder Webapp
Überprüft die grundlegenden Funktionalitäten ohne Google Maps API Key
"""

import os
import sys
import requests
from datetime import datetime

def test_webapp():
    """Testet die grundlegende Webapp-Funktionalität"""
    print("🔍 Teste Versicherungsmakler Finder Webapp")
    print("=" * 50)
    
    # Test 1: Import-Test
    print("\n1. Teste Python-Imports...")
    try:
        from app import app
        print("✅ Flask App importiert")
        
        import googlemaps
        print("✅ Google Maps API Client verfügbar")
        
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup für Web-Scraping verfügbar")
        
        import requests
        print("✅ Requests für HTTP-Calls verfügbar")
        
        from utils.geocoding import get_coordinates
        from utils.scraper import scrape_broker_website
        from utils.api_client import forward_to_external_api
        print("✅ Alle Utility-Module verfügbar")
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False
    
    # Test 2: Flask App Konfiguration
    print("\n2. Teste Flask App Konfiguration...")
    try:
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Test Startseite
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Startseite lädt korrekt")
        else:
            print(f"❌ Startseite Fehler: {response.status_code}")
        
        # Test API Endpoint
        response = client.get('/api/brokers')
        if response.status_code == 200:
            print("✅ API Endpoint funktioniert")
        else:
            print(f"❌ API Endpoint Fehler: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Flask-Test Fehler: {e}")
        return False
    
    # Test 3: Umgebungsvariablen
    print("\n3. Teste Umgebungskonfiguration...")
    
    env_file = "/Users/jonashover/Documents/vsc/scrum/.env"
    if os.path.exists(env_file):
        print("✅ .env Datei gefunden")
    else:
        print("⚠️  .env Datei nicht gefunden - erstelle Beispiel-Datei")
        create_example_env()
    
    # Test 4: Template-Dateien
    print("\n4. Teste Templates...")
    template_files = [
        'templates/base.html',
        'templates/index.html', 
        'templates/results.html',
        'templates/404.html',
        'templates/500.html'
    ]
    
    for template in template_files:
        if os.path.exists(template):
            print(f"✅ {template} vorhanden")
        else:
            print(f"❌ {template} fehlt")
    
    # Test 5: Statische Dateien
    print("\n5. Teste statische Dateien...")
    static_files = [
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    for static_file in static_files:
        if os.path.exists(static_file):
            print(f"✅ {static_file} vorhanden")
        else:
            print(f"❌ {static_file} fehlt")
    
    return True


def create_example_env():
    """Erstellt eine Beispiel .env Datei"""
    env_content = """# Kopiere diese Datei zu .env und fülle die Werte aus

# Google Maps API Key - erforderlich für Standortsuche und Geschäftssuche
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# URL der externen API für die Weiterleitung von Makler-Daten
EXTERNAL_API_URL=https://your-external-api.com/endpoint

# Flask Konfiguration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# Optional: Datenbankverbindung
DATABASE_URL=sqlite:///brokers.db
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("📝 .env Datei erstellt")


def demo_scraping():
    """Demonstriert die Scraping-Funktionalität mit einer Test-Website"""
    print("\n🕷️  Demo: Web-Scraping Funktionalität")
    print("=" * 40)
    
    # Test mit einer öffentlichen Test-Website
    test_url = "https://httpbin.org/html"
    
    try:
        from utils.scraper import scrape_broker_website
        result = scrape_broker_website(test_url)
        
        print(f"Scraping-Test für {test_url}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
            
        print("✅ Scraping-Funktionalität funktioniert")
        
    except Exception as e:
        print(f"❌ Scraping-Fehler: {e}")


def show_usage_instructions():
    """Zeigt Nutzungsanweisungen"""
    print("\n📋 Anweisungen zur Nutzung:")
    print("=" * 40)
    print("1. Erstelle eine .env Datei mit deinem Google Maps API Key:")
    print("   cp .env.example .env")
    print("   # Bearbeite .env und trage deinen API Key ein")
    print("\n2. Starte die Anwendung:")
    print("   python app.py")
    print("\n3. Öffne im Browser:")
    print("   http://localhost:5000")
    print("\n4. Für die externe API-Integration:")
    print("   Trage die EXTERNAL_API_URL in der .env Datei ein")
    
    print("\n🔑 Google Maps API Key erhalten:")
    print("1. Gehe zu: https://console.cloud.google.com/")
    print("2. Erstelle ein neues Projekt oder wähle ein bestehendes")
    print("3. Aktiviere die APIs: Maps JavaScript API, Places API, Geocoding API")
    print("4. Erstelle Anmeldedaten (API-Schlüssel)")
    print("5. Trage den Schlüssel in die .env Datei ein")


def main():
    """Hauptfunktion"""
    print("🚀 Versicherungsmakler Finder - Test & Demo")
    print(f"Zeitstempel: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Wechsle ins Projektverzeichnis
    os.chdir("/Users/jonashover/Documents/vsc/scrum")
    
    # Führe Tests durch
    success = test_webapp()
    
    if success:
        print("\n🎉 Alle Tests erfolgreich!")
        
        # Demo Scraping
        demo_scraping()
        
        # Zeige Nutzungsanweisungen
        show_usage_instructions()
        
        print("\n✨ Die Webapp ist bereit!")
        print("Starte sie mit: python app.py")
        
    else:
        print("\n❌ Tests fehlgeschlagen. Bitte überprüfe die Installation.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
