import requests
from dotenv import load_dotenv
import os

load_dotenv()


# ==================== EDGE CASE 1: Missing API Key ====================

def fetch_weather_with_api_key_validation(city):
    """
    Edge case: Validate API key before making request
    Raises ValueError if API key is missing
    """
    print(f"\n--- Edge Case 1: API Key Validation ({city}) ---")
    
    api_key = os.getenv("WEATHER_API_KEY")
    
    # EDGE CASE: Check if API key exists
    if not api_key:
        raise ValueError(
            "API key missing: WEATHER_API_KEY not found in .env file"
        )
    
    # EDGE CASE: Check if API key is empty string
    if api_key.strip() == "":
        raise ValueError(
            "API key is empty: WEATHER_API_KEY is empty in .env file"
        )
    
    # EDGE CASE: Check if API key meets minimum length
    if len(api_key) < 10:
        raise ValueError(
            f"API key too short: Expected >= 10 chars, got {len(api_key)}"
        )
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Successfully fetched weather for {city}")
            return response.json()
        else:
            print(f"✗ Failed: Status {response.status_code}")
            return None
    
    except Exception as e:
        print(f"✗ Error: {type(e).__name__} - {str(e)}")
        return None


# ==================== EDGE CASE 2: Timeout Handling ====================

def fetch_with_timeout_edge_cases(url, timeout_value=5):
    """
    Edge case: Handle timeout exceptions with different timeout values
    """
    print(f"\n--- Edge Case 2: Timeout ({url}) with timeout={timeout_value}s ---")
    
    # EDGE CASE: Negative timeout
    if timeout_value <= 0:
        print(f"✗ Invalid timeout: {timeout_value}. Must be positive.")
        return None
    
    try:
        response = requests.get(url, timeout=timeout_value)
        print(f"✓ Request completed within {timeout_value}s")
        return response.status_code
    
    except requests.exceptions.ConnectTimeout:
        print(f"✗ Connection Timeout: Failed to connect within {timeout_value}s")
        print("  Suggestion: Server is slow or unreachable")
        return None
    
    except requests.exceptions.ReadTimeout:
        print(f"✗ Read Timeout: No data received within {timeout_value}s")
        print("  Suggestion: Server sent response but too slowly")
        return None
    
    except requests.exceptions.Timeout:
        print(f"✗ General Timeout: Request timed out after {timeout_value}s")
        return None


# ==================== EDGE CASE 3: 404 Not Found ====================

def fetch_with_404_handling(city):
    """
    Edge case: Handle 404 errors gracefully
    """
    print(f"\n--- Edge Case 3: 404 Handling ({city}) ---")
    
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
        response.raise_for_status()  # Raises HTTPError for bad status codes
        
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        # EDGE CASE: Specific handling for 404
        if e.response.status_code == 404:
            print(f"✗ City '{city}' not found (404)")
            print(f"  Suggestion: Check city name spelling")
            return None
        
        # EDGE CASE: Specific handling for 401
        elif e.response.status_code == 401:
            print(f"✗ Unauthorized (401): Invalid API key")
            print(f"  Suggestion: Check WEATHER_API_KEY in .env file")
            return None
        
        # EDGE CASE: Specific handling for 429 (Rate limit)
        elif e.response.status_code == 429:
            print(f"✗ Rate Limited (429): Too many requests")
            print(f"  Suggestion: Wait before making more requests")
            return None
        
        # EDGE CASE: Other HTTP errors
        else:
            print(f"✗ HTTP Error: {e.response.status_code} - {e.response.reason}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {type(e).__name__}")
        return None


# ==================== EDGE CASE 4: Empty/Invalid City Name ====================

def fetch_with_city_validation(city):
    """
    Edge case: Validate city name before making API request
    """
    print(f"\n--- Edge Case 4: City Validation ---")
    
    # EDGE CASE: Empty city name
    if not city or city.strip() == "":
        print(f"✗ Invalid city: City name cannot be empty")
        return None
    
    # EDGE CASE: City name too long
    if len(city) > 100:
        print(f"✗ Invalid city: City name too long ({len(city)} chars)")
        return None
    
    # EDGE CASE: City name with invalid characters
    if not all(c.isalpha() or c.isspace() or c == '-' for c in city):
        print(f"✗ Invalid city: Contains special characters")
        return None
    
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
            print(f"✓ Found: {data.get('name')}, {data.get('sys', {}).get('country')}")
            return data
        else:
            print(f"✗ Failed: Status {response.status_code}")
            return None
    
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}")
        return None


# ==================== EDGE CASE 5: Null/Missing Fields ====================

def process_weather_with_null_checks(data):
    """
    Edge case: Handle missing/null fields in API response
    """
    print(f"\n--- Edge Case 5: Null Field Handling ---")
    
    # EDGE CASE: Null response
    if data is None:
        print("✗ Response is None")
        return None
    
    # EDGE CASE: Empty response
    if not data:
        print("✗ Response is empty")
        return None
    
    # EDGE CASE: Missing required fields
    if "name" not in data:
        print("✗ Missing 'name' field in response")
        return None
    
    if "main" not in data:
        print("✗ Missing 'main' field in response")
        return None
    
    # EDGE CASE: Null temperature
    temp = data.get("main", {}).get("temp")
    if temp is None:
        print("✗ Temperature is None")
        temp = "N/A"
    
    # EDGE CASE: Missing weather array
    weather_list = data.get("weather", [])
    if not weather_list:
        print("⚠ No weather data available")
        condition = "N/A"
    else:
        condition = weather_list[0].get("main", "Unknown")
    
    print(f"✓ City: {data.get('name')}")
    print(f"  Temperature: {temp}°C")
    print(f"  Condition: {condition}")
    return data


# ==================== MAIN: Testing All Edge Cases ====================

if __name__ == "__main__":
    print("=" * 70)
    print("EDGE CASE HANDLING EXAMPLES")
    print("=" * 70)
    
    # Edge Case 1: API Key Validation
    try:
        fetch_weather_with_api_key_validation("Mumbai")
    except ValueError as e:
        print(f"✗ Caught ValueError: {e}")
    
    # Edge Case 2: Timeout Handling
    print("\n--- Testing Timeout Edge Cases ---")
    fetch_with_timeout_edge_cases("https://api.openweathermap.org/data/2.5/weather", timeout_value=10)
    fetch_with_timeout_edge_cases("https://api.openweathermap.org", timeout_value=-1)  # Invalid
    
    # Edge Case 3: 404 Not Found
    fetch_with_404_handling("Mumbai")  # Valid city
    fetch_with_404_handling("XyzInvalidCity12345")  # Invalid city -> 404
    
    # Edge Case 4: City Validation
    print("\n--- Testing City Validation ---")
    fetch_with_city_validation("")  # Empty
    fetch_with_city_validation("Mumbai")  # Valid
    fetch_with_city_validation("a" * 150)  # Too long
    
    # Edge Case 5: Null Field Handling
    print("\n--- Testing Null Field Handling ---")
    api_key = os.getenv("WEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": "London", "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            process_weather_with_null_checks(response.json())
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("EDGE CASE SUMMARY")
    print("=" * 70)
    print("""
✓ Edge Cases Covered:
1. Missing/Invalid API Key
   - Check if key exists
   - Check if key is empty
   - Check if key meets minimum length

2. Timeout Exceptions
   - ConnectTimeout: Can't connect to server
   - ReadTimeout: No data after connection
   - Timeout: General timeout
   - Negative timeout values

3. HTTP Error Handling (404, 401, 429)
   - 404: Resource not found
   - 401: Unauthorized (bad API key)
   - 429: Rate limited (too many requests)

4. Input Validation
   - Empty city name
   - City name too long (>100 chars)
   - Invalid characters in city name

5. Response Field Validation
   - Null response
   - Empty response
   - Missing required fields
   - Null values in nested fields
    """)
