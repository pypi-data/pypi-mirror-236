import logging

from django.conf import settings
from requests import request

logger = logging.getLogger("django_anexia_sms_gateway")


def send_sms(message: str, destination: str):
    """
    Send a single SMS via Anexia SMS Gateway (ASGW)
    """
    asgw_active = getattr(settings, "ASGW_ACTIVE", False)
    encoding = getattr(settings, "ASGW_ENCODING", "GSM")
    url = getattr(
        settings,
        "ASGW_SINGLE_MESSAGE_URL",
        "https://engine.anexia-it.com/api/sms/v1/message.json",
    )
    token = getattr(settings, "ASGW_API_TOKEN", "")

    if asgw_active:
        request_params = {
            "method": "POST",
            "url": url,
            "headers": {
                "Authorization": f"Token {token}",
                "Content-Type": "application/json",
            },
            "json": {
                "destination": destination,
                "message": message,
                "encoding": encoding,
            },
        }

        logger.info(f"Send {encoding} encoded SMS to {destination}: {message}")

        response = request(**request_params)
        response.raise_for_status()

        if response.content:
            return response.json()
        else:
            return None
