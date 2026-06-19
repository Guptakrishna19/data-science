import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Example 1: Using params with requests.get()
print("=== Example 1: Basic GET request with params ===")
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": "London",
    "appid": os.getenv("WEATHER_API_KEY"),
    "units": "metric"
}

response = requests.get(
    url,
    params=params,
    timeout=10
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Example 2: Multiple API calls with error handling
print("\n=== Example 2: Multiple requests with error handling ===")
cities = ["Paris", "Tokyo", "Sydney"]

for city in cities:
    params = {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    }
    
    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"{data['name']}: {data['main']['temp']}°C")
        else:
            print(f"Error for {city}: Status {response.status_code}")
    
    except requests.exceptions.Timeout:
        print(f"Timeout while fetching {city}")
    except requests.exceptions.RequestException as e:
        print(f"Error for {city}: {e}")

# Example 3: Bitcoin API request
print("\n=== Example 3: Bitcoin API request ===")
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin",
    "vs_currencies": "usd,inr",
    "include_market_cap": "true"
}

try:
    response = requests.get(
        url,
        params=params,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Bitcoin Price: ${data['bitcoin']['usd']}")
        print(f"Bitcoin Price (INR): ₹{data['bitcoin']['inr']}")
    else:
        print(f"Failed to fetch Bitcoin data: {response.status_code}")

except requests.exceptions.Timeout:
    print("Request timed out")
except Exception as e:
    print(f"Error: {e}")
