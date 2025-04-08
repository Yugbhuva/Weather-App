import os
import logging
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from weather_api import get_weather_data
from city_suggestions import get_city_suggestions

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def weather():
    location = request.args.get('location', '')
    
    if not location:
        return render_template('index.html', error="Please enter a location")
    
    try:
        # Get weather data from the Tomorrow.io API
        weather_data = get_weather_data(location)
        
        if not weather_data:
            return render_template('error.html', error="Could not retrieve weather data for the specified location. Please try again.")
        
        return render_template('index.html', weather=weather_data, location=location)
    
    except Exception as e:
        logger.error(f"Error retrieving weather data: {str(e)}")
        return render_template('error.html', error=f"An error occurred: {str(e)}")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@app.route('/api/city-suggestions', methods=['GET'])
def city_suggestions_api():
    """API endpoint for city name auto-suggestions"""
    query = request.args.get('q', '')
    suggestions = get_city_suggestions(query)
    return jsonify(suggestions)

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Server error. Please try again later."), 500