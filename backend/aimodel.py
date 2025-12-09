import random
import time

class AIModel:
    def __init__(self):
        self.last_update = time.time()
        # Initial realistic values for Saffron soil
        self.nitrogen = 140  # Ideal: 120-160
        self.phosphorus = 40  # Ideal: 30-50
        self.potassium = 160 # Ideal: 150-180
        self.soil_moisture = 450 # Raw value
        self.soil_moisture_2 = 18.0 # %

    def predict(self):
        """
        Simulates AI predictions based on time and random fluctuations
        to mimic real-time sensor data.
        """
        # Add small random noise to simulate sensor jitter
        self.nitrogen += random.uniform(-2, 2)
        self.phosphorus += random.uniform(-1, 1)
        self.potassium += random.uniform(-2, 2)
        
        # Constrain to realistic ranges
        self.nitrogen = max(100, min(200, self.nitrogen))
        self.phosphorus = max(20, min(80, self.phosphorus))
        self.potassium = max(100, min(250, self.potassium))

        # Moisture fluctuation
        self.soil_moisture_2 += random.uniform(-0.5, 0.5)
        self.soil_moisture_2 = max(10, min(40, self.soil_moisture_2))

        return {
            "nitrogen": int(self.nitrogen),
            "phosphorus": int(self.phosphorus),
            "potassium": int(self.potassium),
            "soil_moisture": int(self.soil_moisture),
            "soil_moisture_2": round(self.soil_moisture_2, 1)
        }

model = AIModel()

def get_ai_reading():
    return model.predict()
