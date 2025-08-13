from flask import Flask, render_template, request, jsonify, flash
import os
from dotenv import load_dotenv
import logging
from utils.geocoding import get_coordinates, search_insurance_brokers
from utils.scraper import scrape_broker_website
from utils.api_client import forward_to_external_api

# Umgebungsvariablen laden
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key_for_development')

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Hauptseite mit Suchformular"""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_brokers():
    """Suche nach Versicherungsmaklern basierend auf Standort und Radius"""
    try:
        # Formulardaten auslesen
        location = request.form.get('location', '').strip()
        radius_km = int(request.form.get('radius', 10))
        
        if not location:
            flash('Bitte geben Sie eine Postleitzahl oder einen Ort ein.', 'error')
            return render_template('index.html')
        
        if radius_km < 1 or radius_km > 100:
            flash('Der Radius muss zwischen 1 und 100 km liegen.', 'error')
            return render_template('index.html')
        
        logger.info(f"Suche nach Versicherungsmaklern in {location} im Umkreis von {radius_km}km")
        
        # Koordinaten des Standorts ermitteln
        coordinates = get_coordinates(location)
        if not coordinates:
            flash('Standort konnte nicht gefunden werden. Bitte überprüfen Sie die Eingabe.', 'error')
            return render_template('index.html')
        
        # Versicherungsmakler in der Nähe suchen
        brokers = search_insurance_brokers(coordinates, radius_km * 1000)  # Umwandlung km zu m
        
        if not brokers:
            flash('Keine Versicherungsmakler in der angegebenen Region gefunden.', 'info')
            return render_template('index.html')
        
        # Details für jeden Makler durch Web-Scraping ergänzen
        enhanced_brokers = []
        for broker in brokers[:10]:  # Limitierung auf 10 Ergebnisse für Performance
            try:
                # Web-Scraping für zusätzliche Details
                scraped_data = scrape_broker_website(broker.get('website', ''))
                
                # Daten zusammenführen
                enhanced_broker = {
                    'name': broker.get('name', 'Unbekannt'),
                    'address': broker.get('formatted_address', 'Unbekannt'),
                    'phone': broker.get('formatted_phone_number', scraped_data.get('phone', 'Nicht verfügbar')),
                    'website': broker.get('website', 'Nicht verfügbar'),
                    'email': scraped_data.get('email', 'Nicht verfügbar'),
                    'contact_person': scraped_data.get('contact_person', 'Nicht verfügbar'),
                    'rating': broker.get('rating', 0),
                    'user_ratings_total': broker.get('user_ratings_total', 0),
                    'place_id': broker.get('place_id', '')
                }
                
                enhanced_brokers.append(enhanced_broker)
                
            except Exception as e:
                logger.warning(f"Fehler beim Scraping für {broker.get('name', 'Unbekannt')}: {str(e)}")
                # Fallback ohne Scraping-Daten
                enhanced_broker = {
                    'name': broker.get('name', 'Unbekannt'),
                    'address': broker.get('formatted_address', 'Unbekannt'),
                    'phone': broker.get('formatted_phone_number', 'Nicht verfügbar'),
                    'website': broker.get('website', 'Nicht verfügbar'),
                    'email': 'Nicht verfügbar',
                    'contact_person': 'Nicht verfügbar',
                    'rating': broker.get('rating', 0),
                    'user_ratings_total': broker.get('user_ratings_total', 0),
                    'place_id': broker.get('place_id', '')
                }
                enhanced_brokers.append(enhanced_broker)
        
        logger.info(f"Gefunden: {len(enhanced_brokers)} Versicherungsmakler")
        
        return render_template('results.html', 
                             brokers=enhanced_brokers, 
                             location=location, 
                             radius=radius_km)
        
    except ValueError:
        flash('Ungültiger Radius. Bitte geben Sie eine Zahl ein.', 'error')
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Fehler bei der Maklersuche: {str(e)}")
        flash('Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.', 'error')
        return render_template('index.html')


@app.route('/api/brokers', methods=['GET'])
def api_get_brokers():
    """API Endpoint um alle gefundenen Makler als JSON zu erhalten"""
    # Hier könnte man eine Datenbank abfragen oder Session-Daten verwenden
    # Für diese Demo geben wir ein Beispiel zurück
    return jsonify({
        'status': 'success',
        'message': 'Verwenden Sie das Suchformular, um Makler zu finden.',
        'brokers': []
    })


@app.route('/api/test', methods=['GET', 'POST'])
def api_test_connection():
    """Test-Endpoint um die externe API-Verbindung zu testen"""
    from utils.api_client import test_external_api_connection, prepare_broker_payload
    
    if request.method == 'GET':
        # Zeige Test-Interface
        return render_template('api_test.html')
    
    try:
        # Test-Daten erstellen
        test_broker = {
            'name': 'Test Versicherungsmakler GmbH',
            'contact_person': 'Max Mustermann',
            'address': 'Teststraße 123, 12345 Teststadt',
            'phone': '+49 123 456789',
            'email': 'test@example.com',
            'website': 'https://test-makler.de',
            'rating': 4.5,
            'user_ratings_total': 42,
            'place_id': 'test_place_id_12345'
        }
        
        # Test-Payload erstellen
        payload = prepare_broker_payload(test_broker)
        
        # An externe API senden
        response = forward_to_external_api(test_broker)
        
        if response and response.get('success'):
            return jsonify({
                'status': 'success',
                'message': 'API-Test erfolgreich',
                'sent_payload': payload,
                'api_response': response,
                'format_used': os.getenv('API_SEND_FORMAT', 'enhanced')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'API-Test fehlgeschlagen',
                'sent_payload': payload,
                'error_details': response,
                'format_used': os.getenv('API_SEND_FORMAT', 'enhanced')
            }), 500
            
    except Exception as e:
        logger.error(f"Fehler beim API-Test: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'API-Test Fehler: {str(e)}'
        }), 500


@app.route('/api/forward', methods=['POST'])
def api_forward_broker():
    """API Endpoint um Makler-Daten an externe API weiterzuleiten"""
    try:
        broker_data = request.get_json()
        
        if not broker_data:
            return jsonify({
                'status': 'error',
                'message': 'Keine Daten empfangen'
            }), 400
        
        # An externe API weiterleiten
        response = forward_to_external_api(broker_data)
        
        if response and response.get('success'):
            return jsonify({
                'status': 'success',
                'message': 'Daten erfolgreich weitergeleitet',
                'external_response': response,
                'format_used': os.getenv('API_SEND_FORMAT', 'enhanced')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Fehler beim Weiterleiten der Daten',
                'error_details': response
            }), 500
            
    except Exception as e:
        logger.error(f"Fehler beim Weiterleiten der API-Daten: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Interner Serverfehler'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Überprüfung der wichtigsten Umgebungsvariablen
    if not os.getenv('GOOGLE_MAPS_API_KEY'):
        logger.warning("GOOGLE_MAPS_API_KEY nicht gesetzt! Bitte .env Datei konfigurieren.")
    
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true', 
            host='0.0.0.0', 
            port=int(os.getenv('PORT', 5000)))
