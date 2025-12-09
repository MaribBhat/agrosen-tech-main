import requests
import time

READ_API_KEY = "LHRD08XC1PTVOSV4"
CHANNEL_ID = "724299"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

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

while True:
    response = requests.get(url).json()
    
    feed = response["feeds"][0]

    n = int(feed["field1"])
    p = int(feed["field2"])
    k = int(feed["field3"])
    moisture = int(feed["field4"])

    print(f"N={n}, P={p}, K={k}, Moisture={moisture}")

    decisions = ai_decision(n, p, k, moisture)
    print("\nAI DECISION:")
    for d in decisions:
        print(" -", d)

    print("------------------------------------")
    time.sleep(15)
