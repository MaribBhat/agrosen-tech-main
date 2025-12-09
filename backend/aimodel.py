import requests
import json
from readings.reading import parse, classify_soil_moisture_2

# Configuration for ThingSpeak
READ_API_KEY = "LHRD08XC1PTVOSV4"
CHANNEL_ID = "724299"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

def get_ai_reading():
    """
    Fetches real-time data from ThingSpeak.
    Previously simulated, now connected to live sensor feed.
    """
    try:
        response = requests.get(URL)
        data = response.json()
        
        # Parse the data using strict logic from existing reading module
        # Note: server.py was using parse() so we reuse it for consistency
        reading = parse(data)
        
        return {
            "nitrogen": reading.nitrogen,
            "phosphorus": reading.phosphorus,
            "potassium": reading.potassium,
            "soil_moisture": reading.soil_moisture,
            "soil_moisture_2": reading.soil_moisture_2,
            "soil_moisture_2_label": classify_soil_moisture_2(reading.soil_moisture_2)
        }
    except Exception as e:
        print(f"Error fetching ThingSpeak data: {e}")
        # Fallback to zeroes if API fails, to indicate "No Data" rather than confusing random data
        return {
            "nitrogen": 0,
            "phosphorus": 0,
            "potassium": 0,
            "soil_moisture": 0,
            "soil_moisture_2": 0,
            "soil_moisture_2_label": "Error"
        }
