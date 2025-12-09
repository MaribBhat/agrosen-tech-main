from season import get_days_until_next_season, get_current_season
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from readings.reading import parse, classify_soil_moisture_2
from readings.ranges import *

READ_API_KEY = "LHRD08XC1PTVOSV4"
CHANNEL_ID = "724299"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"


app = Flask(__name__)
# Allow CORS for all domains to enable local/Vercel connectivity testing
CORS(app, resources={r"/*": {"origins": "*"}})

def ai_decision(n, p, k, moisture):
    decision = []

    if moisture < 500:
        decision.append("Moisture LOW → Turn ON irrigation")
    else:
        decision.append("Moisture OK → Turn OFF irrigation")

    if n < 20:
        decision.append("Nitrogen LOW → Add Urea")
    if p < 10:
        decision.append("Phosphorus LOW → Add DAP")
    if k < 10:
        decision.append("Potassium LOW → Add Potash")

    if n > 200 or p > 200 or k > 200:
        decision.append("NPK VERY HIGH → Stop fertilizing")
        
    return decision

@app.route('/api/reading')
def get_reading():
    data = requests.get(url).json()
    reading = parse(data)
    return jsonify({
        "nitrogen": reading.nitrogen,
        "phosphorus": reading.phosphorus,
        "potassium": reading.potassium,
        "soil_moisture": reading.soil_moisture,
        "soil_moisture_2": reading.soil_moisture_2,
        "soil_moisture_2_label": classify_soil_moisture_2(reading.soil_moisture_2),
        "ai_analysis": ai_decision(reading.nitrogen, reading.phosphorus, reading.potassium, reading.soil_moisture)
    })

@app.route('/api/season')
def get_season():
    current = get_current_season()
    next_season = get_days_until_next_season()
    
    return jsonify({
        "current_season": current.season.value,
        "description": current.description,
        "care_tips": current.care_tips,
        "next_season": next_season['season'],
        "days_until_next": next_season['days'],
        "next_season_date": next_season['date']
    })

@app.route('/api/ranges')
def get_ranges():
    return jsonify({
        "nitrogen": NITROGEN,
        "potassium": POTASSIUM,
        "phosphorus": PHOSPHORUS,
        "soil_moisture": SOIL_MOISTURE,
        "soil_moisture_2": SOIL_MOISTURE_2,
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9000)

