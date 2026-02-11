"""
marine weather api client
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pydantic import ValidationError
from backend.models import MarineResponse
from services.helpers import validate_coordinates

# Session with retry: 3 attempts, backoff 1s, retry on 5xx/429 and connection/timeout errors
_REQUEST_TIMEOUT = 30
_RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=(500, 502, 503, 504, 429),
    allowed_methods=("GET",),
)
_session = requests.Session()
_session.mount("https://", HTTPAdapter(max_retries=_RETRY_STRATEGY))
_session.mount("http://", HTTPAdapter(max_retries=_RETRY_STRATEGY))


def get_marine_forecast(latitude: float, longitude: float) -> MarineResponse:
    """
    fetch marine forecast data from open-meteo api with validation

    args:
        latitude: latitude coordinate
        longitude: longitude coordinate

    returns:
        validated marine response

    raises:
        ValueError: if coordinates are out of valid range
        requests.HTTPError: if api request fails
        ValidationError: if api response doesn't match expected schema
    """
    validate_coordinates(latitude, longitude)
    # open-meteo marine api endpoint
    url = "https://marine-api.open-meteo.com/v1/marine"

    # parameters for the api request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        # Open-Meteo expects comma-separated strings for fields
        "hourly": ",".join(
            [
                "wave_height",
                "wave_direction",
                "wave_period",
                "wind_wave_height",
                "wind_wave_direction",
                "wind_wave_period",
                "swell_wave_height",
                "swell_wave_direction",
                "swell_wave_period",
            ]
        ),
        "daily": ",".join(
            [
                "wave_height_max",
                "wave_direction_dominant",
                "wave_period_max",
                "wind_wave_height_max",
                "wind_wave_direction_dominant",
                "wind_wave_period_max",
                "swell_wave_height_max",
                "swell_wave_direction_dominant",
                "swell_wave_period_max",
            ]
        ),
        "timezone": "auto",
        "forecast_days": 7,
    }

    response = _session.get(url, params=params, timeout=_REQUEST_TIMEOUT)
    response.raise_for_status()

    # validate response
    try:
        return MarineResponse(**response.json())
    except ValidationError as e:
        raise ValueError(f"invalid marine api response: {e}")
