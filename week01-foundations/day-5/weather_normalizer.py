import json


def normalize_weather(data):
    """
    Normalize weather API response data to a simplified format
    
    Transforms nested weather API structure into flat, easy-to-use format.
    
    Args:
        data (dict): Raw weather data from API with structure:
                    {
                        "name": "city_name",
                        "main": {"temp": float, "humidity": int},
                        "weather": [{"main": "condition"}]
                    }
    
    Returns:
        dict: Normalized weather data with structure:
              {
                  "city": "city_name",
                  "temperature": float,
                  "humidity": int,
                  "condition": "condition"
              }
    
    Example:
        >>> raw = {
        ...     "name": "Mumbai",
        ...     "main": {"temp": 31.5, "humidity": 72},
        ...     "weather": [{"main": "Clouds"}]
        ... }
        >>> normalize_weather(raw)
        {
            'city': 'Mumbai',
            'temperature': 31.5,
            'humidity': 72,
            'condition': 'Clouds'
        }
    """
    return {
        "city": data.get("name"),
        "temperature": data.get("main", {}).get("temp"),
        "humidity": data.get("main", {}).get("humidity"),
        "condition": data.get("weather", [{}])[0].get("main")
    }


# Test the function
if __name__ == "__main__":
    # Test case 1
    test_data_1 = {
        "name": "Mumbai",
        "main": {"temp": 31.5, "humidity": 72},
        "weather": [{"main": "Clouds"}]
    }
    
    result_1 = normalize_weather(test_data_1)
    print("Test 1 - Mumbai:")
    print(json.dumps(result_1, indent=2))
    
    # Test case 2
    test_data_2 = {
        "name": "London",
        "main": {"temp": 28.26, "humidity": 57},
        "weather": [{"main": "Clear"}]
    }
    
    result_2 = normalize_weather(test_data_2)
    print("\nTest 2 - London:")
    print(json.dumps(result_2, indent=2))
    
    # Test case 3
    test_data_3 = {
        "name": "Tokyo",
        "main": {"temp": 24.59, "humidity": 68},
        "weather": [{"main": "Rainy"}]
    }
    
    result_3 = normalize_weather(test_data_3)
    print("\nTest 3 - Tokyo:")
    print(json.dumps(result_3, indent=2))
