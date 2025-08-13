import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse
import time

logger = logging.getLogger(__name__)

def scrape_broker_website(url: str) -> Dict[str, str]:
    """
    Scrapt eine Versicherungsmakler-Website für zusätzliche Informationen.
    
    Args:
        url (str): URL der zu scrapenden Website
        
    Returns:
        dict: Dictionary mit gescrapten Informationen
    """
    if not url or not url.startswith(('http://', 'https://')):
        return {
            'email': 'Nicht verfügbar',
            'contact_person': 'Nicht verfügbar',
            'phone': 'Nicht verfügbar'
        }
    
    try:
        # Headers setzen um als echter Browser zu erscheinen
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de,en-US;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        # Request mit Timeout
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        # Encoding sicherstellen
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Daten extrahieren
        scraped_data = {
            'email': extract_email(soup, response.text),
            'contact_person': extract_contact_person(soup),
            'phone': extract_phone(soup, response.text)
        }
        
        logger.info(f"Website {url} erfolgreich gescrapt")
        return scraped_data
        
    except requests.exceptions.Timeout:
        logger.warning(f"Timeout beim Scraping von {url}")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request-Fehler beim Scraping von {url}: {str(e)}")
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim Scraping von {url}: {str(e)}")
    
    return {
        'email': 'Nicht verfügbar',
        'contact_person': 'Nicht verfügbar',
        'phone': 'Nicht verfügbar'
    }


def extract_email(soup: BeautifulSoup, text: str) -> str:
    """Extrahiert E-Mail-Adressen aus HTML"""
    try:
        # Regex für E-Mail-Adressen
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Zuerst in Links suchen (mailto:)
        mailto_links = soup.find_all('a', href=re.compile(r'^mailto:', re.I))
        if mailto_links:
            email = mailto_links[0]['href'].replace('mailto:', '').strip()
            if re.match(email_pattern, email):
                return email
        
        # In sichtbarem Text suchen
        visible_text = soup.get_text()
        emails = re.findall(email_pattern, visible_text)
        if emails:
            # Spam-E-Mails filtern
            valid_emails = [email for email in emails if not any(
                spam in email.lower() for spam in ['noreply', 'no-reply', 'donotreply']
            )]
            if valid_emails:
                return valid_emails[0]
        
        # Im HTML-Quellcode suchen (für obfuscated emails)
        emails_in_source = re.findall(email_pattern, text)
        if emails_in_source:
            valid_emails = [email for email in emails_in_source if not any(
                spam in email.lower() for spam in ['noreply', 'no-reply', 'donotreply']
            )]
            if valid_emails:
                return valid_emails[0]
                
    except Exception as e:
        logger.error(f"Fehler beim Extrahieren der E-Mail: {str(e)}")
    
    return 'Nicht verfügbar'


def extract_contact_person(soup: BeautifulSoup) -> str:
    """Extrahiert Ansprechpartner/Geschäftsführer aus HTML"""
    try:
        # Häufige Selektoren für Ansprechpartner
        contact_selectors = [
            # Deutsche Begriffe
            '*[class*="geschäftsführer"]',
            '*[class*="geschaeftsfuehrer"]', 
            '*[class*="inhaber"]',
            '*[class*="ansprechpartner"]',
            '*[class*="kontakt"]',
            '*[class*="team"]',
            '*[class*="über-uns"]',
            '*[class*="about"]',
            # Nach Text suchen
            '*:contains("Geschäftsführer")',
            '*:contains("Inhaber")',
            '*:contains("Ansprechpartner")',
            '*:contains("Ihr Kontakt")'
        ]
        
        for selector in contact_selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    # Namen-Pattern suchen
                    name_matches = re.findall(r'\b[A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+\b', text)
                    if name_matches:
                        return name_matches[0]
            except:
                continue
        
        # Fallback: Nach typischen deutschen Namen-Patterns suchen
        all_text = soup.get_text()
        
        # Pattern für deutsche Namen mit Titeln
        name_patterns = [
            r'(?:Herr|Frau|Hr\.|Fr\.|Mr\.|Mrs\.|Dr\.|Prof\.)\s+([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+)',
            r'Geschäftsführer[:\s]*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+)',
            r'Inhaber[:\s]*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+)',
            r'Ansprechpartner[:\s]*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+)'
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, all_text)
            if matches:
                return matches[0].strip()
                
    except Exception as e:
        logger.error(f"Fehler beim Extrahieren des Ansprechpartners: {str(e)}")
    
    return 'Nicht verfügbar'


def extract_phone(soup: BeautifulSoup, text: str) -> str:
    """Extrahiert Telefonnummern aus HTML"""
    try:
        # Deutsche Telefonnummer-Pattern
        phone_patterns = [
            r'\+49\s*\(?\d+\)?\s*[\d\s\-/]{6,}',  # +49 Format
            r'0\d{2,5}\s*[\d\s\-/]{6,}',          # 0xxx Format
            r'\(\d{2,5}\)\s*[\d\s\-/]{6,}',       # (0xxx) Format
            r'Tel[\.:]?\s*([\+\d\(\)\s\-/]{8,})', # Tel: Format
            r'Telefon[\.:]?\s*([\+\d\(\)\s\-/]{8,})' # Telefon: Format
        ]
        
        # Zuerst in tel: Links suchen
        tel_links = soup.find_all('a', href=re.compile(r'^tel:', re.I))
        if tel_links:
            phone = tel_links[0]['href'].replace('tel:', '').strip()
            if len(phone) >= 6:
                return clean_phone_number(phone)
        
        # In sichtbarem Text suchen
        visible_text = soup.get_text()
        for pattern in phone_patterns:
            matches = re.findall(pattern, visible_text)
            if matches:
                phone = matches[0] if isinstance(matches[0], str) else matches[0]
                cleaned = clean_phone_number(phone)
                if len(cleaned) >= 6:
                    return cleaned
        
        # Im HTML-Quellcode suchen
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                phone = matches[0] if isinstance(matches[0], str) else matches[0]
                cleaned = clean_phone_number(phone)
                if len(cleaned) >= 6:
                    return cleaned
                    
    except Exception as e:
        logger.error(f"Fehler beim Extrahieren der Telefonnummer: {str(e)}")
    
    return 'Nicht verfügbar'


def clean_phone_number(phone: str) -> str:
    """Bereinigt eine Telefonnummer"""
    # Entfernen von HTML-Tags und extra Whitespace
    phone = re.sub(r'<[^>]+>', '', phone).strip()
    
    # Normalisieren von deutschen Nummern
    phone = re.sub(r'[^\d\+\(\)\-\s/]', '', phone)
    phone = re.sub(r'\s+', ' ', phone).strip()
    
    return phone


def is_valid_broker_website(url: str) -> bool:
    """
    Überprüft ob eine URL zu einer gültigen Versicherungsmakler-Website gehört.
    
    Args:
        url (str): Zu überprüfende URL
        
    Returns:
        bool: True wenn gültige Makler-Website
    """
    if not url:
        return False
        
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
            
        # Bekannte Versicherungsportale ausschließen
        excluded_domains = [
            'check24.de', 'verivox.de', 'tarifcheck.de',
            'facebook.com', 'instagram.com', 'twitter.com',
            'youtube.com', 'linkedin.com', 'xing.com'
        ]
        
        domain = parsed.netloc.lower()
        return not any(excluded in domain for excluded in excluded_domains)
        
    except Exception:
        return False
