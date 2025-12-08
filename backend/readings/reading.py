class SensorReading:
   def __init__(self, nitrogen: int, potassium: int, phosphorus: int, soil_moisture: int, soil_moisture_2: int):
        self.nitrogen = nitrogen
        self.potassium = potassium
        self.phosphorus = phosphorus
        self.soil_moisture = soil_moisture
        self.soil_moisture_2 = soil_moisture_2


def parse(data) -> SensorReading:
    feeds = extract_feeds(data)
    return SensorReading(
        nitrogen=int(feeds['field1']),
        potassium=int(feeds['field3']),
        phosphorus=int(feeds['field2']),
        soil_moisture=int(feeds['field4']),
        soil_moisture_2=int(feeds['field5'])
    )

def extract_feeds(data):
   return data["feeds"][0]


def get_sensor_data():
    data = requests.get(url).json()
    return parse(data)

def classify_soil_moisture_2(value: float) -> str:
    # Clamp to 0-100
    val = max(0.0, min(100.0, float(value)))
    
    if 0.0 <= val <= 9.9:
        return "Very Dry"
    elif 10.0 <= val <= 14.9:
        return "Dry"
    elif 15.0 <= val <= 20.0:
        return "Ideal"
    elif 20.1 <= val <= 39.9:
        return "Moist"
    else:
        return "Wet"


