import requests
from dotenv import load_dotenv
import os

load_dotenv()


def fetch_with_error_handling_basic(url, params=None, timeout=10):
    """
    Basic error handling with Timeout and RequestException
    """
    print(f"\n--- Fetching: {url} ---")
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        
        if response.status_code == 200:
            print(f"✓ Success! Status: {response.status_code}")
            return response.json()
        else:
            print(f"✗ Failed with status: {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        print(f"✗ Timeout Error: Request exceeded {timeout}s timeout")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {type(e).__name__} - {str(e)}")
        return None


def fetch_with_error_handling_detailed(url, params=None, timeout=10):
    """
    Detailed error handling with specific exception types
    """
    print(f"\n--- Detailed Error Handling: {url} ---")
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    
    except requests.exceptions.Timeout:
        print(f"✗ Timeout Error: Request exceeded {timeout}s timeout")
        return None
    
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection Error: Failed to connect to server")
        return None
    
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e.response.status_code} - {e.response.reason}")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        return None
    
    except ValueError:
        print(f"✗ JSON Decode Error: Response is not valid JSON")
        return None


def fetch_with_retries(url, params=None, timeout=10, max_retries=3):
    """
    Error handling with retry logic
    """
    print(f"\n--- Fetch with Retries: {url} ---")
    
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}/{max_retries}...")
        
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            print(f"✓ Success on attempt {attempt}")
            return response.json()
        
        except requests.exceptions.Timeout:
            print(f"  ✗ Timeout on attempt {attempt}")
            if attempt < max_retries:
                print(f"  Retrying...")
        
        except requests.exceptions.ConnectionError:
            print(f"  ✗ Connection error on attempt {attempt}")
            if attempt < max_retries:
                print(f"  Retrying...")
        
        except requests.exceptions.HTTPError as e:
            print(f"  ✗ HTTP Error {e.response.status_code}")
            if e.response.status_code == 429:  # Rate limited
                print(f"  Rate limited! Stopping retries.")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Request Error: {type(e).__name__}")
    
    print(f"✗ Failed after {max_retries} attempts")
    return None


# Test cases
if __name__ == "__main__":
    print("=" * 60)
    print("REQUEST ERROR HANDLING EXAMPLES")
    print("=" * 60)
    
    # Test 1: Valid API request
    print("\n### TEST 1: Valid Request (Weather API) ###")
    api_key = os.getenv("WEATHER_API_KEY")
    params = {
        "q": "Mumbai",
        "appid": api_key,
        "units": "metric"
    }
    result = fetch_with_error_handling_basic(
        "https://api.openweathermap.org/data/2.5/weather",
        params=params
    )
    
    # Test 2: Invalid URL (Connection Error)
    print("\n### TEST 2: Invalid URL (Connection Error) ###")
    result = fetch_with_error_handling_detailed(
        "https://invalid-domain-that-does-not-exist.com/api"
    )
    
    # Test 3: Timeout with short timeout value
    print("\n### TEST 3: Timeout Test (SKIPPED - would hang) ###")
    print("Note: Timeout test skipped to prevent hanging")
    print("In production, you would test with: timeout=1 on a slow endpoint")
    # result = fetch_with_error_handling_basic(
    #     "https://httpbin.org/delay/15",  # This endpoint delays response by 15 seconds
    #     timeout=1  # But our timeout is only 1 second
    # )
    
    # Test 4: Bad status code
    print("\n### TEST 4: Bad Status Code (404) ###")
    result = fetch_with_error_handling_detailed(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": "", "appid": "invalid"}  # Missing city and invalid API key
    )
    
    # Test 5: Valid request with retries
    print("\n### TEST 5: Valid Request with Retry Logic ###")
    params = {
        "q": "London",
        "appid": api_key,
        "units": "metric"
    }
    result = fetch_with_retries(
        "https://api.openweathermap.org/data/2.5/weather",
        params=params,
        timeout=10,
        max_retries=2
    )
    
    print("\n" + "=" * 60)
    print("ERROR HANDLING SUMMARY")
    print("=" * 60)
    print("""
Exceptions handled:
1. requests.exceptions.Timeout
   - Request exceeded the timeout duration
   - Use: timeout=10 in requests.get()

2. requests.exceptions.ConnectionError
   - Failed to connect to the server
   - Network issues, DNS failure, etc.

3. requests.exceptions.HTTPError
   - HTTP error status code (4xx, 5xx)
   - Use response.raise_for_status()

4. requests.exceptions.RequestException
   - Parent class for all requests exceptions
   - Catches any request-related error

Best Practices:
- Always set a timeout to prevent hanging requests
- Use specific exceptions before general ones
- Implement retry logic for transient failures
- Log errors for debugging
- Handle JSON decode errors separately
    """)
