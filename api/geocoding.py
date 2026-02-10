"""
geocoding api client for converting city names to coordinates
https://geopy.readthedocs.io/en/stable/
"""

import time
import sys
from geopy.geocoders import Nominatim

_GEOCODE_TIMEOUT = 10
_GEOCODE_RETRIES = 3
_GEOCODE_RETRY_DELAY = 1.0


def geocode_location(city_name: str) -> tuple[float, float, str]:
    """
    convert city name to latitude and longitude coordinates

    args:
        city_name: name of the city or location

    returns:
        tuple of (latitude, longitude, full_location_name)

    raises:
        ValueError: if location cannot be found
    """
    geolocator = Nominatim(user_agent="surf_forecast_mcp", timeout=_GEOCODE_TIMEOUT)
    location = None
    for attempt in range(_GEOCODE_RETRIES):
        try:
            location = geolocator.geocode(city_name)
            break
        except (OSError, TimeoutError):
            if attempt == _GEOCODE_RETRIES - 1:
                raise
            time.sleep(_GEOCODE_RETRY_DELAY)
    if location is None:
        raise ValueError(f"could not find location: {city_name}")

    return location.latitude, location.longitude, location.address


if __name__ == "__main__":
    city_query = (
        " ".join(sys.argv[1:]).strip() or "Lisbon"
    )  # example: python api/geocoding.py "Lisbon"
    try:
        lat, lon, addr = geocode_location(city_query)
        print(addr)
        print(f"{lat},{lon}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise
