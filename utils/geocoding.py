import os
import googlemaps
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

def get_coordinates(location: str) -> Optional[Dict]:
    """
    Ermittelt Koordinaten für einen gegebenen Standort (PLZ oder Ortsname).
    
    Args:
        location (str): Postleitzahl oder Ortsname
        
    Returns:
        dict: Dictionary mit 'lat' und 'lng' Schlüsseln oder None bei Fehler
    """
    try:
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            logger.error("Google Maps API Key nicht gefunden")
            return None
            
        gmaps = googlemaps.Client(key=api_key)
        
        # Geocoding für deutschen Raum optimieren
        geocode_result = gmaps.geocode(f"{location}, Deutschland")
        
        if not geocode_result:
            # Fallback ohne "Deutschland" suffix
            geocode_result = gmaps.geocode(location)
            
        if geocode_result:
            location_data = geocode_result[0]['geometry']['location']
            logger.info(f"Koordinaten für {location}: {location_data['lat']}, {location_data['lng']}")
            return location_data
        else:
            logger.warning(f"Keine Koordinaten für {location} gefunden")
            return None
            
    except Exception as e:
        logger.error(f"Fehler bei der Geocodierung von {location}: {str(e)}")
        return None


def search_insurance_brokers(coordinates: Dict, radius_meters: int) -> List[Dict]:
    """
    Sucht Versicherungsmakler in einem bestimmten Umkreis.
    
    Args:
        coordinates (dict): Dictionary mit 'lat' und 'lng' Schlüsseln
        radius_meters (int): Suchradius in Metern
        
    Returns:
        list: Liste von Versicherungsmaklern mit deren Informationen
    """
    try:
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            logger.error("Google Maps API Key nicht gefunden")
            return []
            
        gmaps = googlemaps.Client(key=api_key)
        
        # Suchbegriffe für Versicherungsmakler
        search_queries = [
            'Versicherungsmakler',
            'Versicherungsberater', 
            'Versicherungsagentur',
            'Generalagentur Versicherung'
        ]
        
        all_brokers = []
        unique_place_ids = set()
        
        for query in search_queries:
            try:
                # Places API Nearby Search
                places_result = gmaps.places_nearby(
                    location=coordinates,
                    radius=radius_meters,
                    keyword=query,
                    type='insurance_agency'
                )
                
                brokers = places_result.get('results', [])
                
                # Weitere Ergebnisse abrufen wenn verfügbar
                while 'next_page_token' in places_result:
                    import time
                    time.sleep(2)  # Google erfordert eine Pause zwischen Requests
                    
                    places_result = gmaps.places_nearby(
                        page_token=places_result['next_page_token']
                    )
                    brokers.extend(places_result.get('results', []))
                
                # Duplikate basierend auf place_id entfernen
                for broker in brokers:
                    place_id = broker.get('place_id')
                    if place_id and place_id not in unique_place_ids:
                        unique_place_ids.add(place_id)
                        
                        # Detaillierte Informationen für jeden Makler abrufen
                        try:
                            place_details = gmaps.place(
                                place_id=place_id,
                                fields=[
                                    'name', 'formatted_address', 'formatted_phone_number',
                                    'website', 'rating', 'user_ratings_total', 
                                    'opening_hours', 'business_status'
                                ]
                            )
                            
                            if place_details['status'] == 'OK':
                                broker_info = place_details['result']
                                broker_info['place_id'] = place_id
                                all_brokers.append(broker_info)
                                
                        except Exception as detail_error:
                            logger.warning(f"Fehler beim Abrufen der Details für {place_id}: {str(detail_error)}")
                            # Fallback mit grundlegenden Informationen
                            broker['place_id'] = place_id
                            all_brokers.append(broker)
                            
            except Exception as query_error:
                logger.warning(f"Fehler bei der Suche nach {query}: {str(query_error)}")
                continue
        
        logger.info(f"Insgesamt {len(all_brokers)} Versicherungsmakler gefunden")
        
        # Nach Bewertung sortieren (höchste zuerst)
        all_brokers.sort(key=lambda x: x.get('rating', 0), reverse=True)
        
        return all_brokers
        
    except Exception as e:
        logger.error(f"Fehler bei der Maklersuche: {str(e)}")
        return []


def validate_german_location(location: str) -> bool:
    """
    Validiert ob ein Standort in Deutschland liegt.
    
    Args:
        location (str): Standort zum Validieren
        
    Returns:
        bool: True wenn in Deutschland, False sonst
    """
    try:
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            return False
            
        gmaps = googlemaps.Client(key=api_key)
        geocode_result = gmaps.geocode(location)
        
        if geocode_result:
            for component in geocode_result[0].get('address_components', []):
                if 'country' in component.get('types', []):
                    return component.get('short_name') == 'DE'
        
        return False
        
    except Exception:
        return False
