#!/usr/bin/env bash

# Produktion: Flask per WSGI (Gunicorn) über HTTPS starten
# - Verwendet Let's Encrypt Zertifikate aus /etc/letsencrypt/live/<domain>/
# - Fallback auf HTTP, wenn kein Zertifikat vorhanden ist
# - Deutsche Ausgaben, kompatibel mit vorhandenem .venv

set -Eeuo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $*"; }
succ()    { echo -e "${GREEN}[OK]${NC}   $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[FEHLER]${NC} $*"; }

APP_MODULE="wsgi:application"       # Gunicorn-Eintrittspunkt (App unter /scraper)
PORT="443"                 # HTTPS Standard-Port
WORKERS="3"
DOMAIN=""
CERT_FILE=""
KEY_FILE=""
HTTP_ONLY="0"

usage() {
  cat <<USAGE
Verwendung: $0 --domain example.com [Optionen]

Optionen:
  --domain <name>        Pflicht. Domain, für die Zertifikate existieren (Let's Encrypt).
  --port <nr>            Port (Standard: 443 für HTTPS, 8000 für HTTP-Fallback).
  --workers <anzahl>     Gunicorn Worker (Standard: 3).
  --cert <pfad>          Pfad zur Zertifikatsdatei (fullchain.pem). Überschreibt Auto-Suche.
  --key <pfad>           Pfad zur Key-Datei (privkey.pem). Überschreibt Auto-Suche.
  --http                 HTTP-Modus erzwingen (ohne TLS).
  --help                 Diese Hilfe.

Beispiele:
  $0 --domain meine-domain.de
  $0 --domain api.meine-domain.de --workers 4
  $0 --domain meine-domain.de --cert /etc/letsencrypt/live/meine-domain.de/fullchain.pem \
     --key /etc/letsencrypt/live/meine-domain.de/privkey.pem
  $0 --http --port 8000
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --workers) WORKERS="$2"; shift 2;;
    --cert) CERT_FILE="$2"; shift 2;;
    --key) KEY_FILE="$2"; shift 2;;
    --http) HTTP_ONLY="1"; shift;;
    --help|-h) usage; exit 0;;
    *) error "Unbekannte Option: $1"; usage; exit 1;;
  esac
done

# Projekt-Root ermitteln (Verzeichnis dieser Datei)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$SCRIPT_DIR"

# .venv aktivieren
if [[ -d .venv && -f .venv/bin/activate ]]; then
  info "Aktiviere Virtual Environment (.venv)"
  # shellcheck disable=SC1091
  source .venv/bin/activate
  succ ".venv aktiviert"
else
  warn ".venv nicht gefunden – nutze System-Python"
fi

# Gunicorn sicherstellen
if ! command -v gunicorn >/dev/null 2>&1; then
  info "Installiere Gunicorn..."
  python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
  python3 -m pip install gunicorn >/dev/null
  succ "Gunicorn installiert"
fi

# App-Modul prüfen
if ! [[ -f app.py ]]; then
  error "app.py nicht gefunden. Stelle sicher, dass du im Projektordner bist."
  exit 1
fi

# HTTPS vorbereiten, sofern nicht explizit HTTP erzwungen
HTTPS_ARGS=()
if [[ "$HTTP_ONLY" != "1" ]]; then
  if [[ -z "$DOMAIN" && -z "$CERT_FILE" ]]; then
    warn "Keine Domain/Zertifikat angegeben – starte im HTTP-Modus (nutze --domain für HTTPS)."
    HTTP_ONLY="1"
  fi
fi

if [[ "$HTTP_ONLY" != "1" ]]; then
  # Cert/Key automatisch bestimmen, falls nicht übergeben
  if [[ -z "$CERT_FILE" || -z "$KEY_FILE" ]]; then
    if [[ -n "$DOMAIN" ]]; then
      BASE="/etc/letsencrypt/live/$DOMAIN"
      CAND_CERT="$BASE/fullchain.pem"
      CAND_KEY="$BASE/privkey.pem"
      if [[ -f "$CAND_CERT" && -f "$CAND_KEY" ]]; then
        CERT_FILE="$CAND_CERT"
        KEY_FILE="$CAND_KEY"
      else
        warn "Kein Zertifikat in $BASE gefunden – starte im HTTP-Modus. (genssl.sh verwenden)"
        HTTP_ONLY="1"
      fi
    fi
  fi
  if [[ "$HTTP_ONLY" != "1" ]]; then
    HTTPS_ARGS=(--certfile "$CERT_FILE" --keyfile "$KEY_FILE")
    succ "TLS aktiv: ${CERT_FILE} / ${KEY_FILE}"
  fi
fi

# Port-Berechtigung prüfen (443 benötigt root oder CAP_NET_BIND_SERVICE)
if [[ "$HTTP_ONLY" != "1" && "$PORT" -lt 1024 ]]; then
  if [[ "$EUID" -ne 0 ]]; then
    warn "Port $PORT erfordert Root-Rechte. Starte mit sudo oder nutze --port 8443."
    warn "Beispiel: sudo $0 --domain $DOMAIN"
    exit 1
  fi
fi

# Startinfo
if [[ "$HTTP_ONLY" == "1" ]]; then
  [[ "$PORT" == "443" ]] && PORT=8000
  info "Starte Gunicorn im HTTP-Modus auf Port $PORT"
  URL_SCHEME="http"
else
  info "Starte Gunicorn im HTTPS-Modus auf Port $PORT"
  URL_SCHEME="https"
fi

info "Endpoint: $URL_SCHEME://0.0.0.0:$PORT"
info "Workers:  $WORKERS"

exec gunicorn \
  --workers "$WORKERS" \
  --bind 0.0.0.0:"$PORT" \
  ${HTTPS_ARGS[@]:-} \
  "$APP_MODULE"
