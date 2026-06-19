import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def fetch_and_display_weather(city):
    """
    Fetch weather data and display in a formatted way
    Shows successful API response with all fields
    """
    print(f"\n{'='*70}")
    print(f"FETCHING WEATHER DATA FOR: {city.upper()}")
    print(f"{'='*70}")
    
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        print("✗ API key missing")
        return None
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Display 1: Raw JSON Response
            print("\n1️⃣  RAW API RESPONSE (Pretty JSON):")
            print("-" * 70)
            print(json.dumps(data, indent=2))
            
            # Display 2: Key Fields Extracted
            print("\n2️⃣  KEY WEATHER FIELDS:")
            print("-" * 70)
            print(f"City:              {data.get('name')}")
            print(f"Country:           {data.get('sys', {}).get('country')}")
            print(f"Coordinates:       Lat {data.get('coord', {}).get('lat')}, Lon {data.get('coord', {}).get('lon')}")
            print(f"Timezone (UTC):    {data.get('timezone')/3600:.1f} hours")
            
            # Display 3: Temperature Data
            print("\n3️⃣  TEMPERATURE DATA:")
            print("-" * 70)
            main = data.get('main', {})
            print(f"Current Temp:      {main.get('temp')}°C")
            print(f"Feels Like:        {main.get('feels_like')}°C")
            print(f"Min Temp:          {main.get('temp_min')}°C")
            print(f"Max Temp:          {main.get('temp_max')}°C")
            print(f"Humidity:          {main.get('humidity')}%")
            print(f"Pressure:          {main.get('pressure')} hPa")
            print(f"Sea Level:         {main.get('sea_level')} hPa")
            print(f"Ground Level:      {main.get('grnd_level')} hPa")
            
            # Display 4: Weather Conditions
            print("\n4️⃣  WEATHER CONDITIONS:")
            print("-" * 70)
            weather_list = data.get('weather', [])
            for i, weather in enumerate(weather_list, 1):
                print(f"Condition {i}:")
                print(f"  Main:        {weather.get('main')}")
                print(f"  Description: {weather.get('description')}")
                print(f"  Icon:        {weather.get('icon')}")
                print(f"  ID:          {weather.get('id')}")
            
            # Display 5: Wind Data
            print("\n5️⃣  WIND DATA:")
            print("-" * 70)
            wind = data.get('wind', {})
            print(f"Wind Speed:        {wind.get('speed')} m/s")
            print(f"Wind Gust:         {wind.get('gust', 'N/A')} m/s")
            print(f"Wind Direction:    {wind.get('deg')}°")
            
            # Display 6: Cloud & Visibility
            print("\n6️⃣  CLOUD & VISIBILITY:")
            print("-" * 70)
            print(f"Cloudiness:        {data.get('clouds', {}).get('all')}%")
            print(f"Visibility:        {data.get('visibility')} meters")
            
            # Display 7: Sun Times
            print("\n7️⃣  SUN TIMES (Sunrise/Sunset):")
            print("-" * 70)
            import datetime
            sys_data = data.get('sys', {})
            sunrise = datetime.datetime.fromtimestamp(sys_data.get('sunrise', 0))
            sunset = datetime.datetime.fromtimestamp(sys_data.get('sunset', 0))
            print(f"Sunrise:           {sunrise.strftime('%H:%M:%S')}")
            print(f"Sunset:            {sunset.strftime('%H:%M:%S')}")
            print(f"Day Length:        {(sunset - sunrise).total_seconds() / 3600:.1f} hours")
            
            # Display 8: Normalized Data
            print("\n8️⃣  NORMALIZED/SIMPLIFIED VIEW:")
            print("-" * 70)
            normalized = {
                "city": data.get('name'),
                "country": data.get('sys', {}).get('country'),
                "temperature": data.get('main', {}).get('temp'),
                "feels_like": data.get('main', {}).get('feels_like'),
                "humidity": data.get('main', {}).get('humidity'),
                "condition": data.get('weather', [{}])[0].get('main'),
                "description": data.get('weather', [{}])[0].get('description'),
                "wind_speed": data.get('wind', {}).get('speed'),
                "visibility_km": data.get('visibility', 0) / 1000
            }
            print(json.dumps(normalized, indent=2))
            
            return data
        
        else:
            print(f"✗ Request failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    except requests.exceptions.Timeout:
        print("✗ Request timed out")
        return None
    except Exception as e:
        print(f"✗ Error: {type(e).__name__} - {str(e)}")
        return None


def compare_multiple_cities():
    """
    Fetch weather for multiple cities and create comparison table
    """
    print("\n\n" + "="*70)
    print("COMPARISON TABLE: MULTIPLE CITIES")
    print("="*70)
    
    cities = ["Mumbai", "London", "New York", "Tokyo", "Sydney"]
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        print("✗ API key missing")
        return
    
    # Header
    print(f"\n{'City':<15} {'Temp':<8} {'Feels':<8} {'Humidity':<10} {'Condition':<20} {'Wind':<8}")
    print("-" * 80)
    
    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                main = data.get('main', {})
                weather = data.get('weather', [{}])[0]
                wind = data.get('wind', {})
                
                print(f"{data.get('name'):<15} "
                      f"{main.get('temp', 'N/A'):<8.1f} "
                      f"{main.get('feels_like', 'N/A'):<8.1f} "
                      f"{main.get('humidity', 'N/A'):<10} "
                      f"{weather.get('main', 'N/A'):<20} "
                      f"{wind.get('speed', 'N/A'):<8.1f}")
        except Exception as e:
            print(f"{city:<15} Error: {type(e).__name__}")


# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n" * 2)
    print("🌤️  WEATHER API DATA FETCHING - SUCCESSFUL RESPONSES")
    print("=" * 70)
    
    # Fetch and display detailed data for a single city
    fetch_and_display_weather("Mumbai")
    fetch_and_display_weather("London")
    
    # Create comparison table for multiple cities
    compare_multiple_cities()
    
    print("\n" + "=" * 70)
    print("✓ All data fetched successfully!")
    print("=" * 70 + "\n")
