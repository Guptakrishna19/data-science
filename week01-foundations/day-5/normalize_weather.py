import json

def normalize_weather_data(data):
    """
    Normalize weather API response to a simpler format
    
    Args:
        data (dict): Raw weather data from API
    
    Returns:
        dict: Normalized weather data
    """
    normalized = {
        "city": data.get("name"),
        "temperature": data.get("main", {}).get("temp"),
        "humidity": data.get("main", {}).get("humidity"),
        "condition": data.get("weather", [{}])[0].get("main")
    }
    return normalized


# Example 1: From practice.json
print("=== Example 1: Normalizing from practice.json ===")
raw_data = {
    "name": "Mumbai",
    "main": {
        "temp": 31.5,
        "humidity": 72
    },
    "weather": [
        {
            "main": "Clouds"
        }
    ]
}

normalized = normalize_weather_data(raw_data)
print("Before normalization:")
print(json.dumps(raw_data, indent=2))
print("\nAfter normalization:")
print(json.dumps(normalized, indent=2))

# Example 2: Simple case
print("\n=== Example 2: Simple weather data ===")
simple_data = {
    "name": "London",
    "main": {"temp": 28.26, "humidity": 57},
    "weather": [{"main": "Clear"}]
}

normalized_simple = normalize_weather_data(simple_data)
print("Before:")
print(json.dumps(simple_data, indent=2))
print("\nAfter:")
print(json.dumps(normalized_simple, indent=2))

# Example 3: Save normalized data to file
print("\n=== Example 3: Save normalized data to JSON file ===")
with open("practice_normalized.json", "w") as file:
    json.dump(normalized, file, indent=2)

print("Normalized data saved to practice_normalized.json")

# Verify by reading the file
with open("practice_normalized.json", "r") as file:
    loaded_data = json.load(file)
    print(f"\nLoaded from file:\n{json.dumps(loaded_data, indent=2)}")
