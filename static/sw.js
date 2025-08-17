// Service Worker für Versicherungsmakler Finder
const CACHE_NAME = 'versicherungsmakler-finder-v2.0';

// Bestimme Basis-Pfad aus der Registrierungs-Scope (z. B. "/scraper/")
const SCOPE_URL = self.registration && self.registration.scope ? new URL(self.registration.scope) : new URL('/', self.location);
const BASE = new URL('.', SCOPE_URL).pathname.replace(/\/$/, ''); // z.B. "/scraper"

const urlsToCache = [
    `${BASE}/`,
    `${BASE}/static/css/style.css`,
    `${BASE}/static/js/app.js`,
    `${BASE}/static/favicon.ico`,
    // Bootstrap CDN files (falls verfügbar)
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    // Font Awesome (falls verfügbar)
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Installation
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Cache wird erstellt');
                return cache.addAll(urlsToCache.map(url => new Request(url, {
                    cache: 'no-cache'
                })));
            })
            .catch(function(error) {
                console.log('Cache-Fehler beim Installieren:', error);
            })
    );
});

// Aktivierung
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Alte Cache wird gelöscht:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch-Ereignisse abfangen
self.addEventListener('fetch', function(event) {
    // Nur GET-Requests cachen
    if (event.request.method !== 'GET') {
        return;
    }
    
    // Externe API-Calls nicht cachen
    if (event.request.url.includes('googleapis.com') || 
        event.request.url.includes('api.') ||
        event.request.url.includes('/api/')) {
        return;
    }
    
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Cache-Treffer - Cached Response zurückgeben
                if (response) {
                    return response;
                }
                
                // Kein Cache-Treffer - Request vom Netzwerk laden
                return fetch(event.request).then(function(response) {
                    // Prüfen ob valide Response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    // Response klonen
                    const responseToCache = response.clone();
                    
                    // Zur Cache hinzufügen
                    caches.open(CACHE_NAME)
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                });
            })
        .catch(function() {
                // Netzwerk und Cache fehlgeschlagen - Offline-Fallback
                if (event.request.destination === 'document') {
            return caches.match(`${BASE}/`);
                }
                
                // Für andere Ressourcen einen generischen Fehler zurückgeben
                return new Response('Offline - Ressource nicht verfügbar', {
                    status: 503,
                    statusText: 'Service Unavailable',
                    headers: new Headers({
                        'Content-Type': 'text/plain'
                    })
                });
            })
    );
});

// Background Sync für Offline-Formularübermittlungen
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-search') {
        event.waitUntil(doBackgroundSearch());
    }
});

function doBackgroundSearch() {
    // Hier könnten offline gespeicherte Suchvorgänge verarbeitet werden
    return new Promise((resolve) => {
        console.log('Background sync für Suche ausgeführt');
        resolve();
    });
}

// Push-Benachrichtigungen (falls erwünscht)
self.addEventListener('push', function(event) {
    const options = {
        body: event.data ? event.data.text() : 'Neue Versicherungsmakler gefunden!',
        icon: `${BASE}/static/favicon.ico`,
        badge: `${BASE}/static/favicon.ico`,
        tag: 'broker-notification',
        requireInteraction: false,
        actions: [
            {
                action: 'view',
                title: 'Anzeigen'
            },
            {
                action: 'close',
                title: 'Schließen'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Versicherungsmakler Finder', options)
    );
});

// Notification Click Handler
self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'view') {
        event.waitUntil(
            clients.openWindow(`${BASE}/`)
        );
    }
});

// Periodic Background Sync (experimentell)
self.addEventListener('periodicsync', function(event) {
    if (event.tag === 'update-brokers') {
        event.waitUntil(updateBrokerData());
    }
});

function updateBrokerData() {
    // Hier könnte eine Hintergrundaktualisierung der Makler-Daten stattfinden
    return Promise.resolve();
}

// Fehlerbehandlung
self.addEventListener('error', function(event) {
    console.error('Service Worker Fehler:', event.error);
});

self.addEventListener('unhandledrejection', function(event) {
    console.error('Unbehandelter Promise-Fehler im Service Worker:', event.reason);
});

console.log('Versicherungsmakler Finder Service Worker geladen');
