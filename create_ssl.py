#!/usr/bin/env python3
"""
SSL-Zertifikat Generator für localhost
Erstellt selbstsignierte Zertifikate für HTTPS-Entwicklung
"""

import os
import subprocess
import sys
from pathlib import Path

def create_ssl_certificate():
    """Erstellt selbstsignierte SSL-Zertifikate für localhost"""
    
    ssl_dir = Path('ssl')
    ssl_dir.mkdir(exist_ok=True)
    
    cert_file = ssl_dir / 'cert.pem'
    key_file = ssl_dir / 'key.pem'
    
    # Prüfen ob Zertifikate bereits existieren
    if cert_file.exists() and key_file.exists():
        print("✅ SSL-Zertifikate existieren bereits")
        return str(cert_file), str(key_file)
    
    print("🔐 Erstelle SSL-Zertifikate für localhost...")
    
    try:
        # OpenSSL Kommando für selbstsignierte Zertifikate
        cmd = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
            '-keyout', str(key_file),
            '-out', str(cert_file),
            '-sha256', '-days', '365', '-nodes',
            '-subj', '/CN=localhost'
        ]
        
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print(f"✅ Zertifikat erstellt: {cert_file}")
        print(f"✅ Private Key erstellt: {key_file}")
        print("\n🌐 Starten Sie die App mit: python app_https.py")
        print("📱 Öffnen Sie: https://127.0.0.1:5000")
        print("⚠️  Akzeptieren Sie das selbstsignierte Zertifikat im Browser")
        
        return str(cert_file), str(key_file)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Erstellen der Zertifikate: {e}")
        print("💡 Installieren Sie OpenSSL oder verwenden Sie einen anderen Ansatz")
        return None, None
    except FileNotFoundError:
        print("❌ OpenSSL nicht gefunden!")
        print("💡 Installieren Sie OpenSSL:")
        print("   - Windows: https://slproweb.com/products/Win32OpenSSL.html")
        print("   - oder verwenden Sie Python-Bibliotheken")
        
        # Fallback: Python-basierte Zertifikatserstellung
        return create_python_certificate()

def create_python_certificate():
    """Erstellt Zertifikat mit Python cryptography"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        print("🐍 Verwende Python cryptography für Zertifikatserstellung...")
        
        # Private Key generieren
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Zertifikat erstellen
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "DE"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Development"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Localhost"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Development Server"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        ssl_dir = Path('ssl')
        ssl_dir.mkdir(exist_ok=True)
        
        cert_file = ssl_dir / 'cert.pem'
        key_file = ssl_dir / 'key.pem'
        
        # Zertifikat speichern
        with open(cert_file, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
            
        # Private Key speichern
        with open(key_file, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            
        print(f"✅ Python-Zertifikat erstellt: {cert_file}")
        print(f"✅ Python Private Key erstellt: {key_file}")
        
        return str(cert_file), str(key_file)
        
    except ImportError:
        print("❌ cryptography-Bibliothek nicht installiert!")
        print("💡 Installieren Sie mit: pip install cryptography")
        return None, None

if __name__ == "__main__":
    cert_file, key_file = create_ssl_certificate()
    
    if cert_file and key_file:
        print("\n🎉 SSL-Setup erfolgreich!")
        print("📝 Nächste Schritte:")
        print("   1. python app_https.py")
        print("   2. Öffnen Sie https://127.0.0.1:5000")
        print("   3. Akzeptieren Sie das Zertifikat")
        print("   4. Testen Sie die Geolocation!")
    else:
        print("\n⚠️  Fallback: Verwenden Sie weiterhin HTTP für localhost")
