import requests
import sys

def get_weather():
    # If you didn't type a city, show instructions
    if len(sys.argv) < 2:
        print("Usage: python weather_app.py <city or zip code>")
        return

    # Take what you typed (like "London" or "90210")
    location = " ".join(sys.argv[1:])
    
    # This is the secret URL that gives us the weather data
    url = f"https://wttr.in/{location}?format=j1"
    
    print(f"Fetching weather for: {location}...")

    try:
        response = requests.get(url)
        data = response.json()

        # Digging through the data to find the current weather
        current = data['current_condition'][0]
        temp_c = current['temp_C']
        desc = current['weatherDesc'][0]['value']

        print("\n--- RESULTS ---")
        print(f"Condition: {desc}")
        print(f"Temperature: {temp_c}°C")
        print("---------------")

    except:
        print("Error: Could not connect to the weather service.")

if __name__ == "__main__":
    get_weather()