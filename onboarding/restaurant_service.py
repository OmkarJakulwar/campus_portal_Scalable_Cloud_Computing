import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class RestaurantRecommendationService:
    """Service to handle restaurant recommendation API calls"""

    def __init__(self):
        self.base_url = getattr(settings, 'RESTAURANT_API_URL', None)

    def get_restaurants(self, city, cuisine=None, budget=None, min_rating=None):
        
        if not self.base_url:
            logger.warning("Restaurant API URL not configured")
            return {
                "success": False,
                "error": "Restaurant API not configured",
                "restaurants": []
            }

        try:
            payload = {
                "location": city,
                "cuisine": cuisine or "Indian",
                "budget": int(budget) if budget not in (None, "",) else 2,
                "min_rating": float(min_rating) if min_rating not in (None, "",) else 4.0
            }
            print("api link", self.base_url)
            response = requests.post(
                f"{self.base_url}",
                json=payload,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            return {
                "success": True,
                "restaurants": data.get("recommended_restaurants", [])
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Restaurant API: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "restaurants": []
            }
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid restaurant input: {str(e)}")
            return {
                "success": False,
                "error": f"Invalid input: {str(e)}",
                "restaurants": []
            }