import os
import requests
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

# Tomorrow.io API key
API_KEY = os.environ.get("TOMORROW_API_KEY", "UVJ0lwSEQ0WVQauUnxggQQFOZJ1YJMMv")
BASE_URL = "https://api.tomorrow.io/v4/weather/forecast"

def get_coordinates(location):
    """
    Convert a location string to coordinates using geocoding.
    This is a simplified version - for a real app, you'd use a geocoding service.
    
    For now, we'll pass the location directly to the Tomorrow.io API
    as it accepts both coordinates and location names.
    """
    return location

def get_weather_data(location):
    """
    Fetch weather data from Tomorrow.io API
    
    Args:
        location (str): Location string (city name or coordinates)
        
    Returns:
        dict: Formatted weather data
    """
    try:
        params = {
            "location": location,
            "apikey": API_KEY,
            "units": "metric"
        }
        
        response = requests.get(BASE_URL, params=params)
        
        # Check if request was successful
        if response.status_code != 200:
            logger.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
        
        data = response.json()
        
        # Extract relevant data
        weather_data = {}
        
        # Get current weather data
        current = data.get('timelines', {}).get('minutely', [{}])[0].get('values', {})
        if not current:
            current = data.get('timelines', {}).get('hourly', [{}])[0].get('values', {})
        
        # Get daily data for high/low temperatures
        daily_data = data.get('timelines', {}).get('daily', [{}])[0].get('values', {})
        
        # Location information
        location_data = data.get('location', {})
        
        # Get location from input if API doesn't provide proper location data
        city = location_data.get('name')
        country = location_data.get('country')
        
        # If we don't have a city name from the API, use the input location
        if not city or city.lower() == 'unknown':
            # Try to clean up the location string (remove coordinates, commas)
            parsed_location = location.split(',')[0] if ',' in location else location
            city = parsed_location
        
        # Format the data
        weather_data = {
            'temperature': round(current.get('temperature', 0)),
            'temperature_unit': 'C',
            'condition': get_weather_condition(current.get('weatherCode', 0)),
            'wind_speed': round(current.get('windSpeed', 0)),
            'wind_speed_unit': 'km/h',
            'humidity': round(current.get('humidity', 0)),
            'visibility': round(current.get('visibility', 0)),
            'visibility_unit': 'km',
            'uv_index': round(current.get('uvIndex', 0)),
            'aqi': get_aqi_description(round(current.get('epaIndex', 0))),
            'aqi_value': round(current.get('epaIndex', 0)),
            'high': round(daily_data.get('temperatureMax', 0)),
            'low': round(daily_data.get('temperatureMin', 0)),
            'city': city,
            'country': country if country and country.lower() != 'unknown' else '',
            'weather_code': current.get('weatherCode', 0),
            'icon': get_weather_icon(current.get('weatherCode', 0))
        }
        
        return weather_data
        
    except Exception as e:
        logger.error(f"Error in get_weather_data: {str(e)}")
        raise e

def get_weather_condition(code):
    """
    Map Tomorrow.io weather code to human-readable condition
    Based on: https://docs.tomorrow.io/reference/data-layers-core
    """
    weather_codes = {
        0: "Unknown",
        1000: "Clear",
        1001: "Cloudy",
        1100: "Mostly Clear",
        1101: "Partly Cloudy",
        1102: "Mostly Cloudy",
        2000: "Fog",
        2100: "Light Fog",
        3000: "Light Wind",
        3001: "Wind",
        3002: "Strong Wind",
        4000: "Drizzle",
        4001: "Rain",
        4200: "Light Rain",
        4201: "Heavy Rain",
        5000: "Snow",
        5001: "Flurries",
        5100: "Light Snow",
        5101: "Heavy Snow",
        6000: "Freezing Drizzle",
        6001: "Freezing Rain",
        6200: "Light Freezing Rain",
        6201: "Heavy Freezing Rain",
        7000: "Ice Pellets",
        7101: "Heavy Ice Pellets",
        7102: "Light Ice Pellets",
        8000: "Thunderstorm"
    }
    
    return weather_codes.get(code, "Unknown")

def get_weather_icon(code):
    """
    Map Tomorrow.io weather code to Font Awesome icons
    """
    icon_map = {
        1000: "fas fa-sun",           # Clear
        1001: "fas fa-cloud",         # Cloudy
        1100: "fas fa-cloud-sun",     # Mostly Clear
        1101: "fas fa-cloud-sun",     # Partly Cloudy
        1102: "fas fa-cloud",         # Mostly Cloudy
        2000: "fas fa-smog",          # Fog
        2100: "fas fa-smog",          # Light Fog
        3000: "fas fa-wind",          # Light Wind
        3001: "fas fa-wind",          # Wind
        3002: "fas fa-wind",          # Strong Wind
        4000: "fas fa-cloud-rain",    # Drizzle
        4001: "fas fa-cloud-showers-heavy", # Rain
        4200: "fas fa-cloud-rain",    # Light Rain
        4201: "fas fa-cloud-showers-heavy", # Heavy Rain
        5000: "fas fa-snowflake",     # Snow
        5001: "fas fa-snowflake",     # Flurries
        5100: "fas fa-snowflake",     # Light Snow
        5101: "fas fa-snowflake",     # Heavy Snow
        6000: "fas fa-icicles",       # Freezing Drizzle
        6001: "fas fa-icicles",       # Freezing Rain
        6200: "fas fa-icicles",       # Light Freezing Rain
        6201: "fas fa-icicles",       # Heavy Freezing Rain
        7000: "fas fa-icicles",       # Ice Pellets
        7101: "fas fa-icicles",       # Heavy Ice Pellets
        7102: "fas fa-icicles",       # Light Ice Pellets
        8000: "fas fa-bolt"           # Thunderstorm
    }
    
    return icon_map.get(code, "fas fa-question")

def get_aqi_description(aqi_value):
    """
    Map AQI value to descriptive text
    Based on EPA guidelines
    """
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        return "Unhealthy"
    elif aqi_value <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"
