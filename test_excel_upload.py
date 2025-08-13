#!/usr/bin/env python3
"""
Test script für Excel Upload Funktionalität
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import parse_excel_file, find_duplicates, allowed_file

def create_test_excel():
    """Erstelle eine Test-Excel-Datei"""
    print("🔧 Erstelle Test-Excel-Datei...")
    
    # Test-Daten
    test_data = {
        'Name': [
            'Mustermann Versicherungen GmbH',
            'Schmidt & Partner',
            'Versicherungsbüro Weber',
            'Allianz Agentur Berlin',
            'Generali Vertretung'
        ],
        'Address': [
            'Musterstraße 123, 10115 Berlin',
            'Hauptstraße 45, 10117 Berlin', 
            'Friedrichstraße 78, 10117 Berlin',
            'Unter den Linden 12, 10117 Berlin',
            'Potsdamer Platz 1, 10785 Berlin'
        ],
        'Phone': [
            '+49 30 12345678',
            '+49 30 23456789',
            '+49 30 34567890',
            '+49 30 45678901',
            '+49 30 56789012'
        ],
        'Email': [
            'info@mustermann-versicherungen.de',
            'kontakt@schmidt-partner.de',
            'weber@versicherung.de',
            'berlin@allianz.de',
            'info@generali-berlin.de'
        ],
        'Website': [
            'https://mustermann-versicherungen.de',
            'https://schmidt-partner.de',
            'https://weber-versicherung.de',
            'https://allianz.de',
            'https://generali.de'
        ]
    }
    
    df = pd.DataFrame(test_data)
    
    # Uploads-Ordner erstellen falls nicht vorhanden
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Test-Excel-Datei speichern
    test_file = 'uploads/test_brokers.xlsx'
    df.to_excel(test_file, index=False)
    
    print(f"✅ Test-Excel-Datei erstellt: {test_file}")
    return test_file

def test_excel_parsing():
    """Teste Excel-Parsing-Funktionalität"""
    print("\n📊 Teste Excel-Parsing...")
    
    # Test-Excel-Datei erstellen
    test_file = create_test_excel()
    
    # Excel-Datei parsen
    brokers = parse_excel_file(test_file)
    
    if brokers:
        print(f"✅ {len(brokers)} Makler erfolgreich geparst:")
        for i, broker in enumerate(brokers, 1):
            print(f"   {i}. {broker.get('name', 'Unbekannt')}")
    else:
        print("❌ Fehler beim Parsen der Excel-Datei")
        return False
    
    return brokers

def test_duplicate_detection():
    """Teste Duplikat-Erkennung"""
    print("\n🔍 Teste Duplikat-Erkennung...")
    
    # Bestehende Makler (aus Excel)
    existing = [
        {'name': 'Mustermann Versicherungen GmbH', 'address': 'Musterstraße 123, 10115 Berlin'},
        {'name': 'Schmidt & Partner', 'address': 'Hauptstraße 45, 10117 Berlin'}
    ]
    
    # Neue Makler (simuliert Google Places Ergebnisse)
    new_brokers = [
        {'name': 'Mustermann Versicherungen GmbH', 'address': 'Musterstraße 123, 10115 Berlin'},  # Duplikat
        {'name': 'Neue Versicherung Berlin', 'address': 'Neue Straße 99, 10117 Berlin'},  # Neu
        {'name': 'Schmidt & Partner', 'address': 'Hauptstraße 45, 10117 Berlin'},  # Duplikat
        {'name': 'Another Insurance Co.', 'address': 'Another Street 88, 10117 Berlin'}  # Neu
    ]
    
    unique_new, duplicates = find_duplicates(existing, new_brokers)
    
    print(f"✅ {len(unique_new)} neue einzigartige Makler gefunden:")
    for broker in unique_new:
        print(f"   • {broker.get('name', 'Unbekannt')}")
    
    print(f"⚠️  {len(duplicates)} Duplikate erkannt:")
    for broker in duplicates:
        print(f"   • {broker.get('name', 'Unbekannt')}")
    
    return len(unique_new) == 2 and len(duplicates) == 2

def test_file_validation():
    """Teste Datei-Validierung"""
    print("\n📁 Teste Datei-Validierung...")
    
    # Test verschiedene Dateinamen
    test_files = [
        'test.xlsx',  # Erlaubt
        'test.xls',   # Erlaubt
        'test.pdf',   # Nicht erlaubt
        'test.txt',   # Nicht erlaubt
        'test',       # Nicht erlaubt
    ]
    
    for filename in test_files:
        is_allowed = allowed_file(filename)
        status = "✅" if is_allowed else "❌"
        expected = "✅" if filename.endswith(('.xlsx', '.xls')) else "❌"
        
        if status == expected:
            print(f"   {status} {filename} - Korrekt")
        else:
            print(f"   ⚠️  {filename} - Unerwartetes Ergebnis")
            return False
    
    return True

def main():
    """Hauptfunktion für Tests"""
    print("🚀 Starte Tests für Excel Upload Funktionalität")
    print("=" * 50)
    
    # Test 1: Excel-Parsing
    brokers = test_excel_parsing()
    if not brokers:
        print("\n❌ Excel-Parsing-Test fehlgeschlagen!")
        return
    
    # Test 2: Duplikat-Erkennung
    if not test_duplicate_detection():
        print("\n❌ Duplikat-Erkennungs-Test fehlgeschlagen!")
        return
    
    # Test 3: Datei-Validierung
    if not test_file_validation():
        print("\n❌ Datei-Validierungs-Test fehlgeschlagen!")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Alle Tests erfolgreich!")
    print("\nDie Excel Upload-Funktionalität ist bereit:")
    print("• Excel-Dateien (.xlsx, .xls) können hochgeladen werden")
    print("• Makler-Daten werden automatisch geparst")
    print("• Duplikate werden intelligent erkannt")
    print("• Neue Makler werden in der Zone gesucht")
    
    # Aufräumen
    test_file = 'uploads/test_brokers.xlsx'
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\n🧹 Test-Datei entfernt: {test_file}")

if __name__ == "__main__":
    main()
