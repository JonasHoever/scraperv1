#!/usr/bin/env python3
"""
Robuste HTTPS-Server-Alternative mit mkcert oder eigenem Zertifikat
"""

import os
import sys
import subprocess
from pathlib import Path

# Füge das aktuelle Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent))

from app import app

def check_mkcert():
    """Prüft ob mkcert verfügbar ist"""
    try:
        result = subprocess.run(['mkcert', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_mkcert_cert():
    """Erstellt Zertifikat mit mkcert"""
    ssl_dir = Path('ssl')
    ssl_dir.mkdir(exist_ok=True)
    
    cert_file = ssl_dir / 'localhost.pem'
    key_file = ssl_dir / 'localhost-key.pem'
    
    if cert_file.exists() and key_file.exists():
        print("✅ mkcert-Zertifikate bereits vorhanden")
        return str(cert_file), str(key_file)
    
    try:
        # Erstelle Zertifikat mit mkcert
        cmd = [
            'mkcert', 
            '-cert-file', str(cert_file),
            '-key-file', str(key_file),
            'localhost', '127.0.0.1', '::1'
        ]
        
        result = subprocess.run(cmd, cwd=ssl_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ mkcert Zertifikat erstellt: {cert_file}")
            return str(cert_file), str(key_file)
        else:
            print(f"❌ mkcert Fehler: {result.stderr}")
            return None, None
            
    except Exception as e:
        print(f"❌ mkcert Fehler: {e}")
        return None, None

def create_openssl_cert():
    """Erstellt Zertifikat mit OpenSSL"""
    ssl_dir = Path('ssl')
    ssl_dir.mkdir(exist_ok=True)
    
    cert_file = ssl_dir / 'localhost.crt'
    key_file = ssl_dir / 'localhost.key'
    
    if cert_file.exists() and key_file.exists():
        print("✅ OpenSSL-Zertifikate bereits vorhanden")
        return str(cert_file), str(key_file)
    
    # OpenSSL Konfiguration für SAN
    config_content = """[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = DE
ST = Development
L = localhost
O = Development
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
IP.2 = ::1
"""
    
    config_file = ssl_dir / 'openssl.conf'
    config_file.write_text(config_content)
    
    try:
        # Erstelle Private Key
        subprocess.run([
            'openssl', 'genrsa', '-out', str(key_file), '2048'
        ], check=True, capture_output=True)
        
        # Erstelle Zertifikat
        subprocess.run([
            'openssl', 'req', '-new', '-x509', '-key', str(key_file),
            '-out', str(cert_file), '-days', '365',
            '-config', str(config_file),
            '-extensions', 'v3_req'
        ], check=True, capture_output=True)
        
        print(f"✅ OpenSSL Zertifikat erstellt: {cert_file}")
        config_file.unlink()  # Lösche Config-Datei
        return str(cert_file), str(key_file)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ OpenSSL Fehler: {e}")
        return None, None
    except FileNotFoundError:
        print("❌ OpenSSL nicht gefunden!")
        return None, None

def run_robust_https():
    """Startet HTTPS mit verschiedenen Zertifikat-Strategien"""
    print("🔐 HTTPS-Server Setup...")
    
    cert_file = None
    key_file = None
    
    # Strategie 1: mkcert (beste Option)
    if check_mkcert():
        print("🎯 Verwende mkcert für vertrauenswürdige Zertifikate...")
        cert_file, key_file = install_mkcert_cert()
    
    # Strategie 2: OpenSSL
    if not cert_file:
        print("🔧 Verwende OpenSSL für selbstsignierte Zertifikate...")
        cert_file, key_file = create_openssl_cert()
    
    # Strategie 3: Flask adhoc (Fallback)
    if not cert_file:
        print("⚡ Verwende Flask adhoc SSL...")
        try:
            import ssl
            print("\n🌐 HTTPS-Server (adhoc SSL):")
            print("   📍 URL: https://127.0.0.1:5000")
            print("   ⚠️  Selbstsigniertes Zertifikat - Warnung im Browser ignorieren")
            
            app.run(
                host='127.0.0.1',  # Nur localhost für bessere Kompatibilität
                port=5000,
                debug=True,
                ssl_context='adhoc'
            )
        except Exception as e:
            print(f"❌ Adhoc SSL fehgeschlagen: {e}")
            print("\n🔄 Fallback zu HTTP...")
            run_http_fallback()
        return
    
    # Starte mit echten Zertifikaten
    try:
        import ssl
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        
        print("\n🌐 HTTPS-Server (Eigene Zertifikate):")
        print(f"   📍 URL: https://127.0.0.1:5000")
        print(f"   🔒 Zertifikat: {cert_file}")
        print(f"   🗝️  Private Key: {key_file}")
        print("   🎯 Geolocation: Vollständig verfügbar")
        
        if 'mkcert' in cert_file:
            print("   ✅ Vertrauenswürdiges Zertifikat - Keine Browser-Warnung!")
        else:
            print("   ⚠️  Browser-Warnung: 'Erweitert' → 'Trotzdem fortfahren'")
        
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            ssl_context=context
        )
        
    except Exception as e:
        print(f"❌ HTTPS-Server Fehler: {e}")
        print("\n🔄 Fallback zu HTTP...")
        run_http_fallback()

def run_http_fallback():
    """HTTP-Fallback mit Geolocation-Info"""
    print("\n🌐 HTTP-Server (Fallback):")
    print("   📍 URL: http://127.0.0.1:5000")
    print("   📍 Geolocation: Auf localhost verfügbar")
    print("   💡 Für bessere Geolocation-Unterstützung nutzen Sie HTTPS")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

if __name__ == '__main__':
    try:
        run_robust_https()
    except KeyboardInterrupt:
        print("\n👋 Server gestoppt")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        print("🔄 Versuche HTTP-Fallback...")
        run_http_fallback()
