import os
import json
import requests

from dotenv import load_dotenv


def fetch_weather(city):
    """
    Fetch weather data for a given city from OpenWeatherMap API
    
    Args:
        city (str): Name of the city
    
    Returns:
        dict: Raw weather data from API or error message
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        return {"error": "WEATHER_API_KEY not found in .env file"}
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch weather. Status: {response.status_code}"}
    
    except requests.exceptions.Timeout:
        return {"error": f"Request timeout while fetching weather for {city}"}
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


def normalize_weather(data):
    """
    Normalize weather API response data to a simplified format
    
    Args:
        data (dict): Raw weather data from API
    
    Returns:
        dict: Normalized weather data
    """
    if "error" in data:
        return data
    
    return {
        "city": data.get("name"),
        "country": data.get("sys", {}).get("country"),
        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "condition": data.get("weather", [{}])[0].get("main"),
        "description": data.get("weather", [{}])[0].get("description"),
        "pressure": data.get("main", {}).get("pressure"),
        "wind_speed": data.get("wind", {}).get("speed")
    }


def save_json(data, filename="weather_data.json"):
    """
    Save data to a JSON file
    
    Args:
        data (dict): Data to save
        filename (str): Name of the file to save to (default: weather_data.json)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
        print(f"✓ Data saved to {filename}")
        return True
    except Exception as e:
        print(f"✗ Error saving file: {e}")
        return False


def main():
    """
    Main function to orchestrate fetching, normalizing, and saving weather data
    """
    # Load environment variables
    load_dotenv()
    
    # List of cities to fetch weather for
    cities = ["Mumbai", "London", "New York", "Tokyo", "Sydney"]
    
    all_weather_data = {}
    
    print("=" * 50)
    print("WEATHER DATA FETCHER")
    print("=" * 50)
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        
        # Step 1: Fetch raw data
        raw_data = fetch_weather(city)
        
        # Step 2: Check for errors
        if "error" in raw_data:
            print(f"✗ Error: {raw_data['error']}")
            continue
        
        # Step 3: Normalize data
        normalized_data = normalize_weather(raw_data)
        
        # Step 4: Store normalized data
        all_weather_data[city] = normalized_data
        
        # Display the normalized data
        print(f"✓ Successfully fetched weather for {city}")
        print(f"  Temperature: {normalized_data['temperature']}°C")
        print(f"  Condition: {normalized_data['condition']}")
        print(f"  Humidity: {normalized_data['humidity']}%")
    
    # Step 5: Save all data to JSON file
    print("\n" + "=" * 50)
    print("SAVING DATA")
    print("=" * 50)
    save_json(all_weather_data, "weather_data.json")
    
    # Display summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total cities processed: {len(all_weather_data)}")
    print(f"Cities: {', '.join(all_weather_data.keys())}")
    
    # Print formatted JSON
    print("\nFull data (pretty printed):")
    print(json.dumps(all_weather_data, indent=2))


if __name__ == "__main__":
    main()
