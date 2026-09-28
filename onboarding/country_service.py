import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class CountryInfoService:
    # Service to fetch country information including currency, timezone, and flag
    
    def __init__(self):
        self.base_url = settings.COUNTRY_API_URL
    
    def get_country_info(self, country_name):
        try:
            url = f"{self.base_url}{country_name}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                matched_country = None
                for c in data:
                    name = c.get("name", {}).get("common", "").lower()
                    if name == country_name.lower():
                       matched_country = c
                       break
                   
                country = matched_country if matched_country else data[0]
                
                return {
                "success": True,
                "name": country.get("name", {}).get("common"),
                "official_name": country.get("name", {}).get("official"),
                "flags": country.get("flags", {}),
                "capital": country.get("capital", []),
                "region": country.get("region"),
                "subregion": country.get("subregion"),
                "population": country.get("population"),
                "currencies": country.get("currencies", {}),
                "languages": country.get("languages", {}),
                "timezones": country.get("timezones", []),
                "latlng": country.get("latlng", []),
                "maps": country.get("maps", {}),
                }
            else:
                return {'success': False, 'error': 'Country not found'}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Country Info API: {str(e)}")
            return {'success': False, 'error': str(e)}
