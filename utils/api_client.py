import requests
import json
import logging
import os
from typing import Dict, Optional, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def forward_to_external_api(broker_data: Dict[str, Any]) -> Optional[Dict]:
    """
    Sendet Versicherungsmakler-Daten an eine externe API.
    
    Args:
        broker_data (dict): Makler-Daten im JSON-Format
        
    Returns:
        dict: Response der externen API oder None bei Fehler
    """
    try:
        # Stelle sicher, dass die .env-Änderungen in jedem Worker geladen werden
        load_dotenv(override=True)
        external_api_url = os.getenv('EXTERNAL_API_URL')
        
        if not external_api_url:
            logger.warning("EXTERNAL_API_URL nicht konfiguriert")
            # Liefere eine klare Fehlerstruktur zurück, statt None
            return {
                'success': False,
                'error': 'EXTERNAL_API_URL not configured',
                'status_code': None
            }
        
        # Daten für externe API aufbereiten
        payload = prepare_broker_payload(broker_data)
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Versicherungsmakler-Finder/1.0',
            'Accept': 'application/json'
        }
        
        # API Authentifizierung hinzufügen
        api_key = os.getenv('EXTERNAL_API_KEY')
        api_token = os.getenv('EXTERNAL_API_TOKEN')
        
        if api_token:
            # Bearer Token (z.B. JWT)
            if api_token.startswith('Bearer '):
                headers['Authorization'] = api_token
            else:
                headers['Authorization'] = f'Bearer {api_token}'
        elif api_key:
            # API Key (verschiedene Formate unterstützen)
            headers['X-API-Key'] = api_key
            # Alternative: headers['Authorization'] = f'Bearer {api_key}'
        
        logger.info(f"Sende Makler-Daten an externe API: {external_api_url}")
        
        response = requests.post(
            external_api_url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        # Treat any 2xx as success; try JSON, fall back to text
        response.raise_for_status()
        logger.info(f"Externe API Antwort: Status {response.status_code}")
        try:
            result = response.json() if response.content else {}
        except json.JSONDecodeError:
            result = {'text': response.text[:1000]}
        return {
            'status_code': response.status_code,
            'data': result,
            'success': True
        }
        
    except requests.exceptions.Timeout:
        logger.error("Timeout bei der Übertragung zur externen API")
        return {
            'error': 'Timeout',
            'success': False
        }
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP-Fehler bei externer API: {e}")
        return {
            'error': f'HTTP Error: {e}',
            'status_code': e.response.status_code if e.response else None,
            'success': False
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Request-Fehler bei externer API: {e}")
        return {
            'error': str(e),
            'success': False
        }
    except json.JSONDecodeError as e:
        logger.error(f"JSON-Dekodierungsfehler: {e}")
        return {
            'error': 'Invalid JSON response',
            'success': False
        }
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim API-Aufruf: {e}")
        return {
            'error': str(e),
            'success': False
        }


def prepare_broker_payload(broker_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Bereitet Makler-Daten für die externe API auf.
    Unterstützt verschiedene Formate basierend auf API_SEND_FORMAT.
    
    Args:
        broker_data (dict): Rohe Makler-Daten
        
    Returns:
        dict: Aufbereitete Daten für externe API
    """
    send_format = os.getenv('API_SEND_FORMAT', 'enhanced').lower()
    
    if send_format == 'basic':
        # Minimales Format - nur essenzielle Daten
        payload = {
            'name': broker_data.get('name', ''),
            'phone': broker_data.get('phone', ''),
            'website': broker_data.get('website', ''),
            'address': broker_data.get('address', ''),
            'rating': broker_data.get('rating', 0)
        }
    
    elif send_format == 'custom':
        # Benutzerdefiniertes Format für spezielle APIs
        payload = prepare_custom_format(broker_data)
    
    else:  # 'enhanced' - Standard Format
        # Vollständiges Format mit allen gescrapten Daten
        payload = {
            'broker_info': {
                'name': broker_data.get('name', ''),
                'contact_person': broker_data.get('contact_person', ''),
                'address': broker_data.get('address', ''),
                'phone': broker_data.get('phone', ''),
                'email': broker_data.get('email', ''),
                'website': broker_data.get('website', ''),
                'rating': broker_data.get('rating', 0),
                'total_reviews': broker_data.get('user_ratings_total', 0),
                'google_place_id': broker_data.get('place_id', '')
            },
            'scraped_data': {
                'contact_person': broker_data.get('contact_person', ''),
                'email': broker_data.get('email', ''),
                'additional_phone': broker_data.get('phone', ''),
                'scraped_successfully': (
                    broker_data.get('email', 'Nicht verfügbar') != 'Nicht verfügbar' or
                    broker_data.get('contact_person', 'Nicht verfügbar') != 'Nicht verfügbar'
                )
            },
            'metadata': {
                'source': 'Versicherungsmakler-Finder',
                'scraped_at': get_current_timestamp(),
                'data_quality': assess_data_quality(broker_data),
                'format_version': '1.0'
            }
        }
    
    return payload


def prepare_custom_format(broker_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Benutzerdefiniertes Format für spezielle API-Anforderungen.
    Kann nach Bedarf angepasst werden.
    """
    return {
        'id': broker_data.get('place_id', ''),
        'companyName': broker_data.get('name', ''),
        'contactPerson': broker_data.get('contact_person', ''),
        'businessAddress': broker_data.get('address', ''),
        'phoneNumber': broker_data.get('phone', ''),
        'emailAddress': broker_data.get('email', ''),
        'websiteUrl': broker_data.get('website', ''),
        'googleRating': broker_data.get('rating', 0),
        'reviewCount': broker_data.get('user_ratings_total', 0),
        'industry': 'Versicherungsmakler',
        'location': {
            'address': broker_data.get('address', ''),
            'source': 'Google Maps'
        },
        'lastUpdated': get_current_timestamp()
    }


def assess_data_quality(broker_data: Dict[str, Any]) -> str:
    """
    Bewertet die Qualität der Makler-Daten.
    
    Args:
        broker_data (dict): Makler-Daten
        
    Returns:
        str: Qualitätsbewertung ('high', 'medium', 'low')
    """
    required_fields = ['name', 'phone', 'address']
    optional_fields = ['email', 'website', 'contact_person']
    
    required_score = sum(1 for field in required_fields 
                        if broker_data.get(field) and 
                        broker_data.get(field) != 'Nicht verfügbar')
    
    optional_score = sum(1 for field in optional_fields 
                        if broker_data.get(field) and 
                        broker_data.get(field) != 'Nicht verfügbar')
    
    total_score = (required_score / len(required_fields)) * 0.7 + \
                  (optional_score / len(optional_fields)) * 0.3
    
    if total_score >= 0.8:
        return 'high'
    elif total_score >= 0.5:
        return 'medium'
    else:
        return 'low'


def get_current_timestamp() -> str:
    """Gibt aktuellen Zeitstempel im ISO-Format zurück."""
    from datetime import datetime
    return datetime.utcnow().isoformat() + 'Z'


def batch_forward_brokers(brokers: list) -> Dict[str, Any]:
    """
    Sendet mehrere Makler-Datensätze als Batch an die externe API.
    
    Args:
        brokers (list): Liste von Makler-Datensätzen
        
    Returns:
        dict: Zusammenfassung der Batch-Übertragung
    """
    results = {
        'total': len(brokers),
        'successful': 0,
        'failed': 0,
        'errors': []
    }
    
    for i, broker in enumerate(brokers):
        try:
            result = forward_to_external_api(broker)
            if result and result.get('success'):
                results['successful'] += 1
                logger.info(f"Makler {i+1}/{len(brokers)} erfolgreich übertragen")
            else:
                results['failed'] += 1
                error_msg = result.get('error', 'Unbekannter Fehler') if result else 'Keine Antwort'
                results['errors'].append(f"Makler {i+1}: {error_msg}")
                logger.error(f"Makler {i+1}/{len(brokers)} Übertragung fehlgeschlagen: {error_msg}")
                
        except Exception as e:
            results['failed'] += 1
            error_msg = str(e)
            results['errors'].append(f"Makler {i+1}: {error_msg}")
            logger.error(f"Makler {i+1}/{len(brokers)} Übertragung fehlgeschlagen: {error_msg}")
    
    logger.info(f"Batch-Übertragung abgeschlossen: {results['successful']}/{results['total']} erfolgreich")
    return results


def test_external_api_connection() -> bool:
    """
    Testet die Verbindung zur externen API.
    
    Returns:
        bool: True wenn Verbindung erfolgreich
    """
    try:
        external_api_url = os.getenv('EXTERNAL_API_URL')
        if not external_api_url:
            return False
        
        # Einfacher GET-Request zum Testen
        headers = {
            'User-Agent': 'Versicherungsmakler-Finder/1.0'
        }
        
        api_key = os.getenv('EXTERNAL_API_KEY')
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        response = requests.get(external_api_url, headers=headers, timeout=10)
        return response.status_code < 500
        
    except Exception as e:
        logger.error(f"Fehler beim Testen der API-Verbindung: {e}")
        return False
