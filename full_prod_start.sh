#!/usr/bin/env bash

# full_prod_start.sh
# Startet die App gleichzeitig auf Port 80 (HTTP) und Port 443 (HTTPS)
# - Nutzt das vorhandene prod_start.sh für beide Instanzen
# - Sauberer Shutdown (CTRL+C/SIGTERM) -> Ports werden sofort wieder frei
# - Erfordert Root (oder CAP_NET_BIND_SERVICE) für Ports <1024

set -Eeuo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
succ()  { echo -e "${GREEN}[OK]${NC}   $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[FEHLER]${NC} $*"; }

DOMAIN=""
WORKERS="3"
CERT_FILE=""
KEY_FILE=""
HTTP_ONLY="0"
HTTPS_ONLY="0"

usage() {
  cat <<USAGE
Verwendung: sudo $0 --domain example.com [Optionen]

Startet zwei Gunicorn-Instanzen:
  - HTTP  auf :80 (ohne TLS)
  - HTTPS auf :443 (mit Let's Encrypt Zertifikat für --domain)

Optionen:
  --domain <name>    Domain (Pflicht für HTTPS). Zertifikate: /etc/letsencrypt/live/<domain>/
  --workers <anzahl> Anzahl Gunicorn Worker (Standard: 3)
  --cert <pfad>      Pfad zur Zertifikatsdatei (fullchain.pem) – überschreibt Auto-Suche
  --key <pfad>       Pfad zur Key-Datei (privkey.pem) – überschreibt Auto-Suche
  --http-only        Nur HTTP auf :80 starten
  --https-only       Nur HTTPS auf :443 starten (setzt --domain voraus)
  --help             Hilfe anzeigen

Beispiele:
  sudo $0 --domain wunsch-automatisierung.de
  sudo $0 --domain wunsch-automatisierung.de --workers 4
  sudo $0 --https-only --domain wunsch-automatisierung.de
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="$2"; shift 2;;
    --workers) WORKERS="$2"; shift 2;;
    --cert) CERT_FILE="$2"; shift 2;;
    --key) KEY_FILE="$2"; shift 2;;
    --http-only) HTTP_ONLY="1"; shift;;
    --https-only) HTTPS_ONLY="1"; shift;;
    --help|-h) usage; exit 0;;
    *) error "Unbekannte Option: $1"; usage; exit 1;;
  esac

done

# Projekt-Root (Verzeichnis dieser Datei)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$SCRIPT_DIR"

if [[ "$EUID" -ne 0 ]]; then
  warn "Ports 80/443 erfordern Root-Rechte oder CAP_NET_BIND_SERVICE."
  warn "Starte mit: sudo $0 --domain <deine-domain>"
  exit 1
fi

# .venv aktivieren, wenn vorhanden
if [[ -d .venv && -f .venv/bin/activate ]]; then
  info "Aktiviere Virtual Environment (.venv)"
  # shellcheck disable=SC1091
  source .venv/bin/activate
  succ ".venv aktiviert"
else
  warn ".venv nicht gefunden – nutze System-Python"
fi

# prod_start.sh prüfen
if [[ ! -x ./prod_start.sh ]]; then
  if [[ -f ./prod_start.sh ]]; then
    chmod +x ./prod_start.sh
  else
    error "prod_start.sh nicht gefunden – kann nicht fortfahren."
    exit 1
  fi
fi

# Ports belegt?
is_port_in_use() {
  local port="$1"
  ss -lnt 2>/dev/null | awk '{print $4}' | grep -E ":[${port}]$|:${port}$" >/dev/null 2>&1
}

if [[ "$HTTP_ONLY" != "1" ]]; then
  if is_port_in_use 443; then
    error "Port 443 ist bereits belegt. Bitte Dienst stoppen oder --http-only verwenden."
    exit 1
  fi
fi
if [[ "$HTTPS_ONLY" != "1" ]]; then
  if is_port_in_use 80; then
    error "Port 80 ist bereits belegt. Bitte Dienst stoppen oder --https-only verwenden."
    exit 1
  fi
fi

# HTTPS braucht Domain/Zertifikate
if [[ "$HTTPS_ONLY" == "1" || "$HTTP_ONLY" != "1" ]]; then
  if [[ -z "$DOMAIN" ]]; then
    error "--domain ist für HTTPS erforderlich."
    exit 1
  fi
fi

HTTP_PID=""
HTTPS_PID=""

shutdown() {
  echo
  info "Beende Dienste ..."
  # sanft stoppen
  if [[ -n "$HTTP_PID" ]] && kill -0 "$HTTP_PID" 2>/dev/null; then
    kill "$HTTP_PID" 2>/dev/null || true
  fi
  if [[ -n "$HTTPS_PID" ]] && kill -0 "$HTTPS_PID" 2>/dev/null; then
    kill "$HTTPS_PID" 2>/dev/null || true
  fi
  # warten bis beendet
  if [[ -n "$HTTP_PID" ]]; then wait "$HTTP_PID" 2>/dev/null || true; fi
  if [[ -n "$HTTPS_PID" ]]; then wait "$HTTPS_PID" 2>/dev/null || true; fi
  succ "Alle Prozesse beendet. Ports 80/443 sind wieder frei."
}

trap shutdown INT TERM

start_http() {
  info "Starte HTTP (ohne TLS) auf :80 (Workers=$WORKERS)"
  # prod_start.sh im HTTP-Modus
  ./prod_start.sh --http --port 80 --workers "$WORKERS" &
  HTTP_PID=$!
  succ "HTTP gestartet (PID=$HTTP_PID)"
}

start_https() {
  local args=(--domain "$DOMAIN" --port 443 --workers "$WORKERS")
  if [[ -n "$CERT_FILE" ]]; then args+=(--cert "$CERT_FILE"); fi
  if [[ -n "$KEY_FILE"  ]]; then args+=(--key  "$KEY_FILE");  fi
  info "Starte HTTPS (TLS) auf :443 (Workers=$WORKERS, Domain=$DOMAIN)"
  ./prod_start.sh "${args[@]}" &
  HTTPS_PID=$!
  succ "HTTPS gestartet (PID=$HTTPS_PID)"
}

# Startlogik
if [[ "$HTTPS_ONLY" == "1" ]]; then
  start_https
elif [[ "$HTTP_ONLY" == "1" ]]; then
  start_http
else
  start_http
  start_https
fi

echo
[[ "$HTTP_ONLY" != "1" ]]  && info "HTTPS Endpoint: https://0.0.0.0:443"
[[ "$HTTPS_ONLY" != "1" ]] && info "HTTP  Endpoint: http://0.0.0.0:80"

echo
warn "Drücke Ctrl+C zum Beenden – Ports werden danach freigegeben"

# Warten bis Prozesse enden (z.B. via Ctrl+C)
if [[ -n "$HTTP_PID" && -n "$HTTPS_PID" ]]; then
  # Warte auf beide; wenn einer endet, beende den anderen
  while true; do
    if ! kill -0 "$HTTP_PID" 2>/dev/null; then
      warn "HTTP Prozess beendet – stoppe HTTPS"
      [[ -n "$HTTPS_PID" ]] && kill "$HTTPS_PID" 2>/dev/null || true
      break
    fi
    if ! kill -0 "$HTTPS_PID" 2>/dev/null; then
      warn "HTTPS Prozess beendet – stoppe HTTP"
      [[ -n "$HTTP_PID" ]] && kill "$HTTP_PID" 2>/dev/null || true
      break
    fi
    sleep 1
  done
elif [[ -n "$HTTP_PID" ]]; then
  wait "$HTTP_PID" || true
elif [[ -n "$HTTPS_PID" ]]; then
  wait "$HTTPS_PID" || true
fi

# Finaler Shutdown (stellt sicher, dass alles aufgeräumt wird)
shutdown
