import os
import json
import logging
import requests
from difflib import get_close_matches

# Set up logging
logger = logging.getLogger(__name__)

# Cache to store city data
_city_cache = None

def _load_city_data():
    """
    Load city data from a local file
    """
    global _city_cache
    
    if _city_cache is not None:
        return _city_cache
    
    try:
        # Try to load cities from the city.list.json file
        with open('city.list.json', 'r', encoding='utf-8') as file:
            city_data = json.load(file)
            
            # Extract city names from the JSON structure
            # Adapt this based on the actual structure of your JSON file
            # This assumes each entry has a "name" property
            if isinstance(city_data, list):
                # Handle array-style JSON 
                cities = []
                for city in city_data:
                    if isinstance(city, dict) and 'name' in city:
                        city_name = city['name']
                        # # Add country information if available
                        # if 'country' in city and city['country']:
                        #     city_name = f"{city_name}, {city['country']}"
                        cities.append(city_name)
                    elif isinstance(city, str):
                        cities.append(city)
            elif isinstance(city_data, dict):
                # Handle object-style JSON with keys
                cities = []
                for key, city in city_data.items():
                    if isinstance(city, dict) and 'name' in city:
                        city_name = city['name']
                        if 'country' in city and city['country']:
                            city_name = f"{city_name}, {city['country']}"
                        cities.append(city_name)
                    elif isinstance(city, str):
                        cities.append(city)
            
            # Alphabetically sort the list for better organization
            cities.sort()
            _city_cache = cities
            logger.info(f"Loaded {len(cities)} cities from city.list.json")
            return _city_cache
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading city.list.json: {str(e)}")
        logger.info("Falling back to built-in city list")
        
        # Fallback to a compact built-in city list if the file is not found
        cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
            "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
            "Fort Worth", "Columbus", "San Francisco", "Charlotte", "Indianapolis", 
            "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", 
            "Detroit", "Oklahoma City", "Portland", "Las Vegas", "Memphis", "Louisville",
            "London", "Berlin", "Madrid", "Rome", "Paris", "Tokyo", "Delhi", "Shanghai",
            "São Paulo", "Mumbai", "Beijing", "Cairo", "Bangkok", "Toronto", "Sydney"
        ]
        
        # Alphabetically sort the list for better organization
        cities.sort()
        
        _city_cache = cities
        return _city_cache

def get_city_suggestions(query, max_results=10):
    """
    Get city suggestions based on a partial input
    
    Args:
        query (str): The partial city name entered by the user
        max_results (int): Maximum number of suggestions to return
        
    Returns:
        list: List of city suggestions
    """
    if not query or len(query) < 2:
        return []
    
    try:
        cities = _load_city_data()
        
        # Convert query to lowercase for case-insensitive matching
        query_lower = query.lower()
        
        # First, find cities that start with the query
        starts_with_matches = [city for city in cities if city.lower().startswith(query_lower)]
        
        # Then, find cities that contain the query
        contains_matches = [city for city in cities if query_lower in city.lower() and city not in starts_with_matches]
        
        # Finally, find close matches (for typos and misspellings)
        remaining_cities = [city for city in cities if city not in starts_with_matches and city not in contains_matches]
        close_matches = get_close_matches(query, remaining_cities, n=max_results)
        
        # Combine all matches, prioritizing the order: starts_with, contains, close_matches
        all_matches = starts_with_matches + contains_matches + close_matches
        
        # Remove duplicates while preserving order
        unique_matches = []
        for match in all_matches:
            if match not in unique_matches:
                unique_matches.append(match)
        
        # Return the top max_results matches
        return unique_matches[:max_results]
        
    except Exception as e:
        logger.error(f"Error in get_city_suggestions: {str(e)}")
        return []