import requests
import sys

def get_weather():
    # Use the city you type, or default to Singapore
    location = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Singapore"
    
    url = f"https://wttr.in/{location}?format=j1"
    
    # This dictionary maps descriptions to icons
    icons = {
        "Sunny": "☀️",
        "Clear": "✨",
        "Partly cloudy": "⛅",
        "Cloudy": "☁️",
        "Overcast": "☁️",
        "Mist": "🌫️",
        "Patchy rain nearby": "🌦️",
        "Light rain": "🌧️",
        "Moderate rain": "🌧️",
        "Heavy rain": "⛈️",
        "Thundery outbreaks possible": "⚡"
    }

    try:
        response = requests.get(url)
        data = response.json()
        
        current = data['current_condition'][0]
        desc = current['weatherDesc'][0]['value']
        temp = current['temp_C']
        humidity = current['humidity']
        
        # Get the icon from our dictionary, or use a rainbow if not found
        icon = icons.get(desc, "🌈")

        print("\n" + "⭐" * 25)
        print(f" {icon}  WEATHER FOR {location.upper()}")
        print("⭐" * 25)
        print(f" Condition : {desc}")
        print(f" Temp      : {temp}°C")
        print(f" Humidity  : {humidity}%")
        print("-" * 25 + "\n")

    except Exception as e:
        print("Error: Could not fetch weather data.")

if __name__ == "__main__":
    get_weather()
    