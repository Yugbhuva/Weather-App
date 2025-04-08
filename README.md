# Weather App

A Flask-based web application that displays comprehensive weather information using the Tomorrow.io API. The app features an intuitive search interface with intelligent city name auto-suggestions.

## Features

- **Comprehensive Weather Data**: Temperature, weather conditions, wind speed, humidity, visibility, UV index, air quality index (AQI), temperature highs and lows
- **Intelligent Search**: Auto-complete suggestions for city names with fuzzy matching (tolerates typos and misspellings)
- **Custom City Database**: Support for your own city database file for personalized suggestions
- **Responsive Design**: Clean, modern interface that works well on both desktop and mobile devices
- **Error Handling**: Graceful error pages with helpful messages

## Getting Started

### Prerequisites

- Python 3.6+
- Flask and other dependencies (listed in requirements.txt)
- A Tomorrow.io API key (free tier available)

### Installation

1. Clone the repository or download the source code
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your API key as an environment variable:
   ```
   export TOMORROW_API_KEY=your_api_key_here
   ```

### Custom City Database

The application supports loading city suggestions from a custom JSON file. To use this feature:

1. Create a file named `city.list.json` in the project root directory
2. Format it as an array of city objects:
   ```json
   [
     {
       "id": 1,
       "name": "New York",
       "country": "US"
     },
     {
       "id": 2,
       "name": "London",
       "country": "GB"
     }
   ]
   ```
3. The application will automatically load this file on startup

If the file is not found or improperly formatted, the app will fall back to a built-in list of common cities.

### Running the Application

Start the application with:

```
python main.py
```

The application will be available at `http://localhost:5000`.

## API Endpoints

- **GET /api/city-suggestions?q=query**: Returns JSON array of city suggestions based on the partial query

## Components

- **app.py**: Main Flask application with routes
- **weather_api.py**: Tomorrow.io API client for fetching weather data
- **city_suggestions.py**: Logic for city name auto-suggestions and fuzzy matching
- **templates/**: HTML templates for the UI
- **static/**: CSS, JavaScript, and other static assets

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Weather data provided by [Tomorrow.io](https://www.tomorrow.io/)
- Built with [Flask](https://flask.palletsprojects.com/) and [Bootstrap](https://getbootstrap.com/)
