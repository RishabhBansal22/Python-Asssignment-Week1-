import requests
import os
import pandas as pd


class Weather:
    def __init__(self, api_key=os.getenv("weather_api_key")):
        """Initialize Weather client with API key."""
        self.api_key = api_key

    def fetch_weather(self, city: str, api_key: str = None) -> dict:
        """
        Fetch current weather data for a city.
        """
        # Use instance API key if not provided
        if not api_key:
            api_key = self.api_key
            
        try:
            # Make API request with metric units
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            fetch = requests.get(url)
            
            if fetch.status_code == 200:
                response = fetch.json()
                return response
            else:
                # Return error details
                return {
                    "error": fetch.status_code,
                    "message": fetch.json() if fetch.content else "error fetching response from api"
                }
        except Exception as e:
            # Handle connection or parsing errors
            return {
                "error": "exception",
                "message": str(e)
            }
        
    def analyze_weather(self, weather_data: dict) -> str:
        """
        Analyze weather data and categorize conditions.
        """
        try:
            # Extract main weather metrics
            main_data = weather_data.get("main")
            if not main_data:
                raise ValueError("Invalid weather data: missing 'main' key")
                
            temp = main_data.get("temp")
            humidity = main_data.get("humidity")
            wind_data = weather_data.get("wind", {})
            wind_speed = wind_data.get("speed", 0)
        except Exception as e:
            raise e
        
        warnings = []
        
        # Check for high wind conditions
        if wind_speed > 10:
            warnings.append("High wind alert!")
            
        # Check for high humidity
        if humidity > 80:
            warnings.append("Humid conditions!")
        
        # Categorize temperature
        if int(temp) <= 10:
            temp_category = "Cold (≤10°C)"
        elif int(temp) in range(11, 25):
            temp_category = "Mild (11-24°C)"
        else:
            temp_category = "Hot (≥25°C)"
        
        # Combine category with warnings
        result = temp_category
        if warnings:
            result += "\nWarnings: " + ", ".join(warnings)
        
        return result
    
    def log_weather(self, city: str, filename: str) -> dict:
        """
        Fetch weather data and log it to a CSV file.
        
        Args:
            city (str): Name of the city
            filename (str): Path to CSV file for logging
            
        Returns:
            dict: Success message or error dictionary
        """
        # Fetch weather data
        weather_data = self.fetch_weather(city)
        
        # Check for errors in response
        if not isinstance(weather_data, dict) or "error" in weather_data:
            return weather_data if isinstance(weather_data, dict) else {
                "error": "invalid_response",
                "message": str(weather_data)
            }
        
        # Extract relevant weather metrics
        main_data = weather_data.get("main", {})
        wind_data = weather_data.get("wind", {})
        weather_desc = weather_data.get("weather", [{}])[0]
        
        # Prepare log entry with all relevant data
        log_entry = {
            "city": city,
            "temperature": main_data.get("temp"),
            "humidity": main_data.get("humidity"),
            "wind_speed": wind_data.get("speed"),
            "description": weather_desc.get("description"),
            "category": self.analyze_weather(weather_data)
        }
        
        # Determine if CSV headers are needed
        file_exists = os.path.isfile(filename)
        
        # Append data to CSV file
        df = pd.DataFrame([log_entry])
        df.to_csv(filename, mode='a', header=not file_exists, index=False)
        
        return {
            "status": "success",
            "message": f"Weather data for {city} logged to {filename}"
        }
       

def main(action: str, city: str, filename: str | bool = None):
    """
    Main entry point for weather operations.
    
    Args:
        action (str): Action to perform ('analyze_weather' or 'log_weather')
        city (str): City name
        filename (str | bool, optional): CSV filename for logging
        
    Returns:
        str | dict: Analysis result or logging status
    """
    # Initialize weather client with API key
    client = Weather(os.getenv("weather_api_key"))
    
    if action.lower() == "analyze_weather":
        # Fetch and analyze weather
        data = client.fetch_weather(city)
        result = client.analyze_weather(data)
        return result
    else:
        # Log weather data to CSV
        logging = client.log_weather(city, filename)
        return logging


if __name__ == "__main__":
    # Example: Analyze weather for Jaipur
    res = main("analyze_weather", "jaipur")
    print(res)


      