#!/usr/bin/env python3
"""
Flask App mit HTTPS-Unterstützung für Geolocation
"""

import os
import sys
from pathlib import Path

# Füge das aktuelle Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent))

# Importiere die Haupt-App
from app import app

def create_simple_ssl_context():
    """Erstellt einfachen SSL-Kontext für Entwicklung"""
    try:
        import ssl
        
        ssl_dir = Path('ssl')
        cert_file = ssl_dir / 'cert.pem'
        key_file = ssl_dir / 'key.pem'
        
        if cert_file.exists() and key_file.exists():
            print(f"🔐 Verwende SSL-Zertifikate: {cert_file}, {key_file}")
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(str(cert_file), str(key_file))
            return context
        else:
            print("⚠️  SSL-Zertifikate nicht gefunden. Erstelle sie mit: python create_ssl.py")
            return 'adhoc'  # Automatische Zertifikat-Erstellung
            
    except Exception as e:
        print(f"❌ SSL-Fehler: {e}")
        return None

def run_https_server():
    """Startet Flask-Server mit HTTPS"""
    
    print("🚀 Starte HTTPS-Server für Geolocation-Support...")
    
    # Prüfe ob pyOpenSSL verfügbar ist für 'adhoc' SSL
    try:
        import OpenSSL
        has_openssl = True
    except ImportError:
        has_openssl = False
        print("💡 Für automatische SSL-Zertifikate installieren Sie: pip install pyopenssl")
    
    ssl_context = create_simple_ssl_context()
    
    if ssl_context is None and not has_openssl:
        print("❌ Kein SSL möglich. Verwenden Sie HTTP mit:")
        print("   python app.py")
        return
    
    try:
        print("\n🌐 HTTPS-Server Informationen:")
        print("   📍 URL: https://127.0.0.1:5000")
        print("   📍 Lokales Netzwerk: https://192.168.x.x:5000")
        print("   🔒 SSL: Aktiviert")
        print("   📍 Geolocation: Verfügbar")
        print("\n⚠️  Browser-Warnung:")
        print("   - Klicken Sie 'Erweitert' → 'Trotzdem fortfahren'")
        print("   - Oder akzeptieren Sie das selbstsignierte Zertifikat")
        print("\n🎯 Jetzt funktioniert der Standort-Button!")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            ssl_context=ssl_context or 'adhoc'
        )
        
    except Exception as e:
        print(f"\n❌ HTTPS-Server Fehler: {e}")
        print("\n🔄 Fallback: Starte HTTP-Server...")
        print("   ⚠️  Geolocation funktioniert nur eingeschränkt über HTTP")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )

if __name__ == '__main__':
    run_https_server()
