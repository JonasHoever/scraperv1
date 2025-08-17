import os
import re
import googlemaps
import logging
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger(__name__)

def _normalize_german_address(raw: str) -> str:
    """Normalisiert deutsche Adressen, unterstützt u.a.:
    - "21641 Apensen"
    - "Musterstraße 1, 21641 Apensen"
    - "Musterstraße 1 ,21641 Apensen" (fehlerhafte Kommas korrigieren)
    Gibt eine für Geocoding geeignete Zeichenkette zurück (mit , Deutschland).
    """
    s = (raw or "").strip()
    # doppelte/trailing Kommas und unnötige Leerzeichen korrigieren
    s = re.sub(r"\s*,\s*", ", ", s)
    s = re.sub(r"\s+", " ", s)

    # Wenn keine Länderangabe drin, DE hinzufügen
    if not re.search(r"\b(Deutschland|Germany)\b", s, re.IGNORECASE):
        s = f"{s}, Deutschland"
    return s


def _pick_best_geocode_result(input_text: str, results: List[Dict]) -> Optional[Dict]:
    """Wählt das passendste Geocode-Ergebnis aus.
    Strategie:
      1) Wenn im Input eine 5-stellige PLZ vorkommt, Ergebnis mit gleicher PLZ priorisieren.
      2) Falls eine Stadt im Input vorkommt, Ergebnis mit passender locality priorisieren.
      3) Sonst erstes Ergebnis.
    """
    if not results:
        return None

    # finde PLZ im Input
    m = re.search(r"\b(\d{5})\b", input_text)
    input_plz = m.group(1) if m else None

    # versuche Stadt aus Input grob zu extrahieren (Wort nach PLZ oder letztes Wort)
    input_lower = input_text.lower()
    candidate_city = None
    if input_plz and "," in input_lower:
        # z.B. "..., 21641 Apensen, Deutschland"
        tail = input_lower.split(",")
        tail = [t.strip() for t in tail if t.strip()]
        if tail:
            last = tail[-1]
            # entferne 'deutschland'
            if "deutschland" in last:
                last = last.replace("deutschland", "").strip()
            # nehme erstes Wort als Stadtannahme
            parts = last.split()
            if parts:
                candidate_city = parts[0]

    def extract_component(res: Dict, comp_type: str) -> Optional[str]:
        for c in res.get('address_components', []):
            if comp_type in c.get('types', []):
                return c.get('long_name')
        return None

    # 1) PLZ-Match priorisieren
    scored: List[Tuple[int, Dict]] = []
    for res in results:
        score = 0
        postal_code = extract_component(res, 'postal_code')
        locality = extract_component(res, 'locality') or extract_component(res, 'postal_town')
        country = extract_component(res, 'country')

        if country and country.lower() in ("deutschland", "germany"):
            score += 2
        if input_plz and postal_code == input_plz:
            score += 5
        if candidate_city and locality and locality.lower() == candidate_city:
            score += 3
        # leichte Bevorzugung von locality/route-Adressen
        types = res.get('types', [])
        if any(t in types for t in ('street_address', 'route', 'locality', 'postal_code')):
            score += 1

        scored.append((score, res))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1] if scored else results[0]


def get_coordinates(location: str) -> Optional[Dict]:
    """
    Ermittelt Koordinaten für einen gegebenen Standort (Adresse, PLZ + Ort, etc.).
    Bevorzugt deutsche Ergebnisse und versucht, die passendste Adresse zu wählen.
    """
    try:
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            logger.error("Google Maps API Key nicht gefunden")
            return None

        gmaps = googlemaps.Client(key=api_key)

        # 1) Wenn Eingabe "lat, lng" ist, direkt Koordinaten verwenden
        ll_match = re.match(r"^\s*(-?\d{1,3}\.\d+)\s*,\s*(-?\d{1,3}\.\d+)\s*$", location or "")
        if ll_match:
            lat = float(ll_match.group(1))
            lng = float(ll_match.group(2))
            logger.info(f"Erkannte GPS-Koordinaten: lat={lat}, lng={lng}")
            return {"lat": lat, "lng": lng}

        prepared = _normalize_german_address(location)

        # Komponenten-Filter aufbauen (Deutschland + evtl. PLZ)
        comps = {"country": "DE"}
        m = re.search(r"\b(\d{5})\b", prepared)
        if m:
            comps["postal_code"] = m.group(1)

        # Bias auf Deutschland und deutsche Sprache
        geocode_result = gmaps.geocode(
            prepared,
            region='de',
            language='de',
            components=comps
        )

        if not geocode_result:
            # Fallback: ohne components
            geocode_result = gmaps.geocode(prepared, region='de', language='de')

        if geocode_result:
            best = _pick_best_geocode_result(prepared, geocode_result)
            location_data = best['geometry']['location']
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
        
        # Stelle sicher, dass Koordinaten als Tupel vorliegen
        center = (coordinates.get('lat'), coordinates.get('lng'))

        for query in search_queries:
            try:
                # Places API Nearby Search
                places_result = gmaps.places_nearby(
                    location=center,
                    radius=radius_meters,
                    keyword=query,
                    type='insurance_agency',
                    language='de'
                )
                
                brokers = places_result.get('results', [])
                
                # Weitere Ergebnisse abrufen wenn verfügbar
                while 'next_page_token' in places_result:
                    import time
                    time.sleep(2)  # Google erfordert eine Pause zwischen Requests
                    
                    places_result = gmaps.places_nearby(
                        page_token=places_result['next_page_token'],
                        language='de'
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
                                ],
                                language='de'
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
