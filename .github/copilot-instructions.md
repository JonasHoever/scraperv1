<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Versicherungsmakler Finder - Flask Webapp

This is a Flask web application that finds insurance brokers (Versicherungsmakler) within a specified radius of a given location (postal code or city name).

## Key Features:
- Location-based search with radius selection
- Web scraping of broker websites for detailed information
- JSON API endpoint for forwarding data to external APIs
- German language support for location searches

## Technologies Used:
- Flask for the web framework
- Google Maps API for location and business search
- BeautifulSoup for web scraping
- Requests for HTTP operations
- SQLite for local data storage (optional)

## Code Guidelines:
- Use German variable names and comments where appropriate for business logic
- Implement proper error handling for API calls and web scraping
- Follow Flask best practices for route organization
- Include rate limiting for API calls to prevent blocking
- Use environment variables for sensitive API keys
