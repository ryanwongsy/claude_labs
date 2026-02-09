from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pro Weather</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: {{ bg_color }};
            transition: background 0.5s ease;
        }
        .card { 
            background: rgba(255, 255, 255, 0.2); 
            backdrop-filter: blur(10px);
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            width: 300px;
        }
        input { padding: 12px; border-radius: 25px; border: none; width: 80%; margin-bottom: 10px; outline: none; }
        button { padding: 10px 20px; background: #333; color: white; border: none; border-radius: 25px; cursor: pointer; font-weight: bold; }
        h1 { color: #333; margin-bottom: 20px; }
        .temp { font-size: 3rem; font-weight: bold; margin: 10px 0; }
        .details { display: flex; justify-content: space-around; margin-top: 20px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📍 {{ city if city else "Weather" }}</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Search city..." required>
            <button type="submit">Search</button>
        </form>
        
        {% if weather %}
            <div class="temp">{{ weather.temp }}°C</div>
            <div style="text-transform: capitalize; font-weight: 500;">{{ weather.desc }}</div>
            <div class="details">
                <div>💧 {{ weather.humidity }}%<br>Humidity</div>
                <div>💨 {{ weather.wind }}km/h<br>Wind</div>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = ""
    bg_color = "#e0e0e0"
    
    if request.method == "POST":
        city = request.form.get("city")
        try:
            r = requests.get(f"https://wttr.in/{city}?format=j1").json()
            curr = r['current_condition'][0]
            desc = curr['weatherDesc'][0]['value'].lower()
            
            weather_data = {
                'temp': curr['temp_C'],
                'desc': desc,
                'humidity': curr['humidity'],
                'wind': curr['windspeedKmph']
            }

            # Pro Color Logic
            if any(w in desc for w in ["sun", "clear"]): bg_color = "#fceabb" # Sunny
            elif any(w in desc for w in ["rain", "shower"]): bg_color = "#89f7fe" # Rainy
            elif any(w in desc for w in ["cloud", "overcast"]): bg_color = "#acb6e5" # Cloudy
            elif any(w in desc for w in ["snow", "ice"]): bg_color = "#ffffff" # Snowy
        except:
            weather_data = {'temp': '?', 'desc': 'City not found', 'humidity': '0', 'wind': '0'}
            
    return render_template_string(HTML_TEMPLATE, weather=weather_data, city=city, bg_color=bg_color)

if __name__ == "__main__":
    app.run(debug=True)