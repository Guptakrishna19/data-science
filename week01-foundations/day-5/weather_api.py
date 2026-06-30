from dotenv import load_dotenv
import os
import requests

load_dotenv('.env')

def fetch_weather(city):
    """
    Fetch weather data for a given city using OpenWeatherMap API
    
    Args:
        city (str): Name of the city
    
    Returns:
        dict: Weather data or error message
    """
    api_key = os.getenv("WEATHER_API_KEY")
    
    if not api_key:
        return {"error": "WEATHER_API_KEY not found in .env file"}
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "pressure": data["main"]["pressure"]
            }
        else:
            return {"error": f"Failed to fetch weather. Status code: {response.status_code}"}
    
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}


# Test the function
if __name__ == "__main__":
    # Test with different cities
    cities = ["London", "Mumbai", "New York"]
    
    for city in cities:
        print(f"\n--- Weather for {city} ---")
        weather = fetch_weather(city)
        
        if "error" in weather:
            print(f"Error: {weather['error']}")
        else:
            print(f"City: {weather['city']}, {weather['country']}")
            print(f"Temperature: {weather['temperature']}°C")
            print(f"Feels Like: {weather['feels_like']}°C")
            print(f"Humidity: {weather['humidity']}%")
            print(f"Condition: {weather['description']}")
            print(f"Pressure: {weather['pressure']} hPa")
