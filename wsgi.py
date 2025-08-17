from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix

# Import the Flask app
from app import app as flask_app

# Honor proxy headers (X-Forwarded-*) when behind a reverse proxy
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)


class HostRedirectMiddleware:
    """WSGI middleware that redirects www.* to apex (e.g., www.example.com -> example.com).
    Only manipulates the host if it begins with 'www.'.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        host = environ.get('HTTP_HOST', '')
        # Extract hostname without port
        hostname = host.split(':', 1)[0]
        if hostname.startswith('www.') and len(hostname) > 4:
            target_host = hostname[4:]
            # Preserve path and query, honor scheme from wsgi
            scheme = environ.get('wsgi.url_scheme', 'https')
            path = environ.get('PATH_INFO', '/') or '/'
            query = environ.get('QUERY_STRING', '')
            location = f"{scheme}://{target_host}{path}"
            if query:
                location += f"?{query}"
            headers = [
                ('Location', location),
                ('Content-Type', 'text/plain; charset=utf-8'),
                ('Content-Length', str(len(location)))
            ]
            start_response('301 Moved Permanently', headers)
            return [location.encode('utf-8')]
        return self.app(environ, start_response)


def root_dispatch_app(environ, start_response):
    """Root site (domain.de/) shows a selection menu; the app continues under /scraper.
    Unknown paths at root return 404.
    """
    path = (environ.get('PATH_INFO') or '/').rstrip('/') or '/'
    if path == '/':
        html = """
    <!DOCTYPE html>
    <html lang=\"de\">
    <head>
        <meta charset=\"utf-8\"> 
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> 
        <title>Wunsch‑Automatisierungen</title>
        <style>
            body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,\"Helvetica Neue\",Arial,sans-serif;background:#0f1218;color:#e9edf1}
            .wrap{min-height:100vh;display:grid;place-items:center;padding:24px}
            .card{background:#151a22;border:1px solid #232b36;border-radius:14px;max-width:720px;width:100%;padding:28px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.35)}
            h1{margin:0 0 8px;font-size:28px;letter-spacing:.2px}
            p{margin:0 0 20px;color:#9aa6b2}
            .btn{display:inline-block;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:600;background:#6a7eea;color:#fff}
            .btn:hover{filter:brightness(1.05)}
        </style>
        <link rel=\"preconnect\" href=\"https://cdn.jsdelivr.net\">
        <link rel=\"preconnect\" href=\"https://cdnjs.cloudflare.com\">
        <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\">
        <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\">
        <link rel=\"icon\" href=\"/scraper/static/favicon.ico\">
        <meta http-equiv=\"refresh\" content=\";url=/scraper/\" id=\"metaRefresh\" disabled>
        <script>/* Optional: enable timed redirect by setting content like '2;url=/scraper/' */</script>
        <script type=\"application/ld+json\">{"@context":"https://schema.org","@type":"WebSite","name":"Wunsch‑Automatisierungen","url":"/","potentialAction":{"@type":"SearchAction","target":"/scraper/search?location={location}&radius={radius}","query-input":"required name=location"}}</script>
        <meta name=\"robots\" content=\"index,follow\">
        <meta name=\"theme-color\" content=\"#151a22\">
    </head>
    <body>
        <div class=\"wrap\">
            <div class=\"card\">
                <h1><i class=\"fas fa-wand-magic-sparkles me-2\"></i>Willkommen bei Wunsch‑Automatisierungen</h1>
                <p>Weiter zur Anwendung:</p>
                <a href=\"/scraper/\" class=\"btn\"><i class=\"fas fa-arrow-right-to-bracket me-2\"></i>Zum Scraper</a>
            </div>
        </div>
    </body>
    </html>
        """
        body = html.encode('utf-8')
        start_response('200 OK', [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(body)))
        ])
        return [body]
    start_response('404 Not Found', [('Content-Type', 'text/plain; charset=utf-8')])
    return [b'Not Found']


# Mount the Flask app under /scraper
_mounted = DispatcherMiddleware(root_dispatch_app, {
    '/scraper': flask_app
})

# Wrap with host redirect to canonicalize away from www.* (after certificate covers both names)
application = HostRedirectMiddleware(_mounted)
