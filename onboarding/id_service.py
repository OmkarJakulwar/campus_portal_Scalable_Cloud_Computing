import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class DigitalIDCardService:
    """Service to handle digital ID card API calls"""

    def __init__(self):
        self.base_url = settings.ID_CARD_API_URL

    def generate_card_id(self, first_name, last_name, email, phone, city=None, country=None):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "role": "Student",
            "includeQr": True,
            "includeCardImage": True,
        }

        if city:
            payload["city"] = city
        if country:
            payload["country"] = country

        try:
            response = requests.post(self.base_url, json=payload, timeout=15)

            response.raise_for_status()
            data = response.json()

            return {
                "success": True,
                "cardId": data.get("cardId"),
                "cardImageDataUrl": data.get("cardImageDataUrl"),
                "raw_response": data
            }

        except requests.exceptions.HTTPError as e:
            error_text = None
            error_json = None
            status_code = None

            if e.response is not None:
                status_code = e.response.status_code
                error_text = e.response.text
                try:
                    error_json = e.response.json()
                except ValueError:
                    error_json = None

            logger.error("HTTP error calling ID Card API")
            logger.error("Payload sent: %s", payload)
            logger.error("Status code: %s", status_code)
            logger.error("Response text: %s", error_text)
            logger.error("Response json: %s", error_json)

            return {
                "success": False,
                "error": error_json or error_text or str(e),
                "cardId": None
            }

        except requests.exceptions.RequestException as e:
            logger.error("Request error calling ID Card API: %s", str(e))
            logger.error("Payload sent: %s", payload)

            return {
                "success": False,
                "error": str(e),
                "cardId": None
            }