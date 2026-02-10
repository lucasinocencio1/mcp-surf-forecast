"""
surf forecast mcp server - provides wave and surf conditions for any location
how to run:
python server.py

how to use:
mcp server --url http://localhost:8000

how to use the tool:
mcp server --url http://localhost:8000 --tool get_surf_forecast --args "city_name"

how to use the tool:
mcp server --url http://localhost:8000 --tool get_surf_forecast --args "city_name"
"""

from fastmcp import FastMCP
from api.geocoding import geocode_location
from api.marine import get_marine_forecast
from api.weather import weather_forecast
from backend.models import SurfForecast
from services import ForecastService

# create server
mcp = FastMCP("Surf Forecast Server")


@mcp.resource("surf://info")
def get_server_info() -> str:
    """
    provides information about the surf forecast mcp server.
    
    returns details about capabilities, data sources, and usage guidelines.
    """
    return """
    surf forecast mcp server
    
    capabilities:
    - real-time surf and wave forecasts for any coastal location worldwide
    - 5-day forecast with hourly data
    - wave height, direction, and period analysis
    - wind conditions (speed, direction, gusts)
    - surf quality assessment
    
    data sources:
    - open-meteo marine forecast api
    - open-meteo weather forecast api
    - nominatim geocoding service
    
    usage:
    use the get_surf_forecast tool with a city name to retrieve detailed surf conditions.
    the server provides comprehensive wave analysis optimized for surfers and water sports enthusiasts.
    """


@mcp.prompt()
def analyze_surf_conditions(location: str) -> str:
    """
    generate a prompt for analyzing surf conditions at a specific location.
    
    args:
        location: name of the city/location to analyze
    """
    return f"""
    please analyze the surf conditions for {location} and provide:
    
    1. current surf quality and whether it's suitable for surfing
    2. best time to surf in the next 24 hours (considering wave height, wind, and conditions)
    3. forecast trend for the next few days (improving or deteriorating)
    4. any incoming swell (swell height, swell direction, swell period, etc.)
    
    use the get_surf_forecast tool to retrieve the data, then provide a clear,
    actionable summary for surfers planning their session.
    """


@mcp.tool()
def get_surf_forecast(city_name: str) -> str:
    """
    get surf forecast for a location by city name.
    
    returns current conditions and 5-day forecast including:
    - wave heights (total, swell, wind waves) with directions
    - wind speed and direction (in knots) with gusts
    - air temperature
    - surf quality assessment
    
    the forecast is returned as formatted text optimized for llm context,
    with compass directions (n, s, e, w, etc) for easy interpretation.
    
    args:
        city_name: name of the city/location (e.g., "livorno", "san diego", "biarritz")
    
    returns:
        formatted surf forecast text optimized for llm consumption
    """
    # geocode the location
    latitude, longitude, full_location = geocode_location(city_name)
    
    # fetch marine and weather forecast data
    marine_data = get_marine_forecast(latitude, longitude)
    weather_data = weather_forecast(latitude, longitude)
    
    # parse and structure the data
    forecast = ForecastService.parse_forecast_data(
        marine_data,
        weather_data,
        full_location,
        latitude,
        longitude
    )
    
    # return as llm-optimized text format
    return forecast.to_llm_context()

if __name__ == "__main__":
    # start the FastMCP server
    mcp.run()
