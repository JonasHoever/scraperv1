#!/usr/bin/env bash

# genssl.sh - Let's Encrypt Zertifikate mit Certbot erstellen/erneuern
# Unterstützt Nginx- und Standalone-Modus. Führt automatische HTTP-01 Challenge durch.
# Beispiel:
#   sudo ./genssl.sh --domain example.com --email admin@example.com --nginx
#   sudo ./genssl.sh --domain example.com --email admin@example.com --standalone

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

DOMAIN=""
EMAIL=""
USE_NGINX="0"
USE_STANDALONE="0"
STAGING="0"

usage() {
  cat <<USAGE
Verwendung: sudo $0 --domain example.com --email admin@example.com [--nginx|--standalone] [--staging]

Optionen:
  --domain <name>       Pflicht. Domain für das Zertifikat.
  --email <adresse>     Pflicht. E-Mail für Let’s Encrypt Benachrichtigungen.
  --nginx               Nginx Plugin verwenden (empfohlen wenn Nginx läuft).
  --standalone          Standalone Webserver von certbot verwenden (stoppt Port 80 Nutzung).
  --staging             Let’s Encrypt Staging-CA (Ratelimits vermeiden, nur zu Testzwecken).
  --help                Hilfe anzeigen.

Beispiele:
  sudo $0 --domain meine-domain.de --email ich@domain.de --nginx
  sudo $0 --domain api.meine-domain.de --email ops@domain.de --standalone --staging
USAGE
}

require_root() {
  if [[ "$EUID" -ne 0 ]]; then
    error "Root-Rechte erforderlich. Bitte mit sudo ausführen."
    exit 1
  fi
}

install_certbot_if_needed() {
  if command -v certbot >/dev/null 2>&1; then
    succ "certbot gefunden"
    return
  fi
  info "Installiere certbot..."
  if command -v snap >/dev/null 2>&1; then
    snap install core >/dev/null 2>&1 || true
    snap refresh core >/dev/null 2>&1 || true
    snap install --classic certbot
    ln -sf /snap/bin/certbot /usr/bin/certbot
  else
    # Fallback für Systeme ohne snap
    if command -v apt >/dev/null 2>&1; then
      apt update
      apt install -y certbot
    elif command -v dnf >/dev/null 2>&1; then
      dnf install -y certbot
    elif command -v yum >/dev/null 2>&1; then
      yum install -y certbot
    else
      error "Konnte certbot nicht automatisch installieren. Bitte manuell installieren."
      exit 1
    fi
  fi
  succ "certbot installiert"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --domain) DOMAIN="$2"; shift 2;;
      --email) EMAIL="$2"; shift 2;;
      --nginx) USE_NGINX="1"; shift;;
      --standalone) USE_STANDALONE="1"; shift;;
      --staging) STAGING="1"; shift;;
      --help|-h) usage; exit 0;;
      *) error "Unbekannte Option: $1"; usage; exit 1;;
    esac
  done
  if [[ -z "$DOMAIN" || -z "$EMAIL" ]]; then
    error "--domain und --email sind erforderlich."
    usage; exit 1
  fi
  if [[ "$USE_NGINX" == "1" && "$USE_STANDALONE" == "1" ]]; then
    error "Bitte entweder --nginx oder --standalone verwenden, nicht beides."
    exit 1
  fi
  if [[ "$USE_NGINX" == "0" && "$USE_STANDALONE" == "0" ]]; then
    warn "Kein Modus angegeben – verwende --standalone."
    USE_STANDALONE="1"
  fi
}

obtain_certificate() {
  local staging_arg=()
  [[ "$STAGING" == "1" ]] && staging_arg=(--staging)

  if [[ "$USE_NGINX" == "1" ]]; then
    info "Fordere Zertifikat über Nginx-Plugin an..."
    certbot --nginx "${staging_arg[@]}" -d "$DOMAIN" -m "$EMAIL" --agree-tos --no-eff-email
  else
    info "Fordere Zertifikat im Standalone-Modus an (Port 80 notwendig)..."
    # Stoppe ggf. Dienste auf Port 80 (optional, vorsichtig einsetzen)
    if command -v systemctl >/dev/null 2>&1; then
      if systemctl is-active --quiet nginx; then
        warn "Stoppe temporär nginx für Standalone-Challenge"
        systemctl stop nginx
      fi
    fi
    certbot certonly --standalone "${staging_arg[@]}" -d "$DOMAIN" -m "$EMAIL" --agree-tos --no-eff-email
    if command -v systemctl >/dev/null 2>&1; then
      if systemctl list-unit-files | grep -q nginx; then
        info "Starte nginx wieder (falls vorhanden)"
        systemctl start nginx || true
      fi
    fi
  fi
  succ "Zertifikat erstellt/erneuert: /etc/letsencrypt/live/$DOMAIN/"
}

post_instructions() {
  cat <<MSG

${GREEN}Weiter mit HTTPS-Start:${NC}
  sudo ./prod_start.sh --domain $DOMAIN

Automatische Erneuerung (cron):
  sudo crontab -e
  # Beispiel (täglich um 03:17 Uhr prüfen):
  17 3 * * * certbot renew --quiet --deploy-hook "systemctl reload nginx || true"

Zertifikatspfade:
  /etc/letsencrypt/live/$DOMAIN/fullchain.pem
  /etc/letsencrypt/live/$DOMAIN/privkey.pem

MSG
}

main() {
  require_root
  parse_args "$@"
  install_certbot_if_needed
  obtain_certificate
  post_instructions
}

main "$@"
