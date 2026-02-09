from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# This is the "HTML" - the design of your website
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Endo Weather App</title>
    <style>
        body { font-family: sans-serif; text-align: center; margin-top: 50px; background: {{ bg_color }};
        .card { background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        input { padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌦️ Weather Lookup</h1>
        <form method="POST">
            <input type="text" name="city" placeholder="Enter city (e.g. Singapore)" required>
            <button type="submit">Check Weather</button>
        </form>
        {% if weather %}
            <h2>{{ city }}</h2>
            <p><strong>Condition:</strong> {{ weather.desc }}</p>
            <p><strong>Temp:</strong> {{ weather.temp }}°C</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = ""
    bg_color = "#f0f4f8"  # Default light blue-gray
    
    if request.method == "POST":
        city = request.form.get("city")
        try:
            r = requests.get(f"https://wttr.in/{city}?format=j1").json()
            current = r['current_condition'][0]
            # We use .lower() to make sure "Sunny" matches "sunny"
            desc = current['weatherDesc'][0]['value'].lower()
            print(f"DEBUG: The weather is {desc}") # This shows in your CMD window

            weather_data = {
                'temp': current['temp_C'],
                'desc': current['weatherDesc'][0]['value']
            }

            # Stronger logic
            if any(word in desc for word in ["sun", "clear", "fair"]):
                bg_color = "#FFD700" 
            elif any(word in desc for word in ["rain", "drizzle", "shower", "patchy"]):
                bg_color = "#A7C7E7" 
            elif any(word in desc for word in ["cloud", "overcast", "mist", "fog"]):
                bg_color = "#D3D3D3"
                
        except Exception as e:
            print(f"Error: {e}")
            weather_data = {'temp': 'N/A', 'desc': 'Error fetching data'}
            
    return render_template_string(HTML_TEMPLATE, weather=weather_data, city=city, bg_color=bg_color)

if __name__ == "__main__":
    app.run(debug=True)