# API Konfiguration für Versicherungsmakler Finder

## Unterstützte JSON Formate für externe APIs

### 1. BASIC Format (API_SEND_FORMAT=basic)
```json
{
  "name": "UFKB Berlin - Unabhängiger Versicherungsmakler Berlin",
  "phone": "+49 30 12345678",
  "website": "https://example-broker.de",
  "address": "Musterstraße 123, 10115 Berlin",
  "rating": 4.8
}
```

### 2. ENHANCED Format (API_SEND_FORMAT=enhanced) - Standard
```json
{
  "broker_info": {
    "name": "UFKB Berlin - Unabhängiger Versicherungsmakler Berlin",
    "contact_person": "Max Mustermann",
    "address": "Musterstraße 123, 10115 Berlin",
    "phone": "+49 30 12345678",
    "email": "info@ufkb-berlin.de",
    "website": "https://ufkb-berlin.de",
    "rating": 4.8,
    "total_reviews": 96,
    "google_place_id": "ChIJlQV3wNZQqEcRPRunsa1qbZE"
  },
  "scraped_data": {
    "contact_person": "Max Mustermann",
    "email": "info@ufkb-berlin.de",
    "additional_phone": "+49 30 12345678",
    "scraped_successfully": true
  },
  "metadata": {
    "source": "Versicherungsmakler-Finder",
    "scraped_at": "2025-08-13T10:57:00Z",
    "data_quality": "high",
    "format_version": "1.0"
  }
}
```

### 3. CUSTOM Format (API_SEND_FORMAT=custom)
```json
{
  "id": "ChIJlQV3wNZQqEcRPRunsa1qbZE",
  "companyName": "UFKB Berlin - Unabhängiger Versicherungsmakler Berlin",
  "contactPerson": "Max Mustermann",
  "businessAddress": "Musterstraße 123, 10115 Berlin",
  "phoneNumber": "+49 30 12345678",
  "emailAddress": "info@ufkb-berlin.de",
  "websiteUrl": "https://ufkb-berlin.de",
  "googleRating": 4.8,
  "reviewCount": 96,
  "industry": "Versicherungsmakler",
  "location": {
    "address": "Musterstraße 123, 10115 Berlin",
    "source": "Google Maps"
  },
  "lastUpdated": "2025-08-13T10:57:00Z"
}
```

## API Authentifizierung

### Bearer Token
```bash
EXTERNAL_API_TOKEN=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Key
```bash
EXTERNAL_API_KEY=your-secret-api-key-here
```

## Webhook Test URLs

Für Tests kannst du diese kostenlosen Webhook-Services verwenden:

- **Webhook.site**: https://webhook.site/
- **RequestBin**: https://requestbin.com/
- **Pipedream**: https://pipedream.com/

## Beispiel .env Konfiguration

```bash
# Externe API
EXTERNAL_API_URL=https://webhook.site/12345678-abcd-efgh-ijkl-123456789012
API_SEND_FORMAT=enhanced

# Mit Authentifizierung
EXTERNAL_API_KEY=your-api-key
# ODER
EXTERNAL_API_TOKEN=Bearer your-jwt-token
```

## Anpassung des Custom Formats

Um das Custom Format anzupassen, bearbeite die Funktion `prepare_custom_format()` in `utils/api_client.py`:

```python
def prepare_custom_format(broker_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dein benutzerdefiniertes Format hier"""
    return {
        'yourField': broker_data.get('name', ''),
        'yourFormat': 'custom'
        # ... weitere Felder
    }
```
