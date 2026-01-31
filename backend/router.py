"""
API router for the Surf Forecast API.
"""

from fastapi import APIRouter, HTTPException, Query, status

from backend.models import SurfForecast
from api.geocoding import geocode_location
from api.marine import get_marine_forecast
from api.weather import weather_forecast
from services.forecast import ForecastService


router = APIRouter(tags=["forecast"])


@router.get("/forecast", response_model=SurfForecast)
def get_forecast(city: str = Query(..., min_length=1, description="City or location name")):
    """
    Get surf forecast for a location by city name.

    Returns current conditions and 5-day forecast: wave heights, wind, temperature,
    and surf quality context.
    """
    city = city.strip()
    try:
        lat, lon, full_name = geocode_location(city)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Location not found: {e!s}",
        ) from e
    try:
        marine_data = get_marine_forecast(lat, lon)
        weather_data = weather_forecast(lat, lon)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Forecast service error: {e!s}",
        ) from e
    forecast = ForecastService.parse_forecast_data(
        marine_data, weather_data, full_name, lat, lon
    )
    return forecast


@router.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    return {"status": "ok"}
