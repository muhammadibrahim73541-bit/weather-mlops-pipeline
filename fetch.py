import requests
import sqlite3
from datetime import datetime, timedelta

locations = {
    "Aalborg": (57.0488, 9.9217),
    "Doha": (25.276987, 51.520008),
    "Lahore": (31.5204, 74.3587)
}

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    location TEXT,
    date TEXT,
    temperature REAL,
    wind REAL,
    rain REAL
)
""")

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

for city, (lat, lon) in locations.items():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum,windspeed_10m_max&timezone=auto"

    data = requests.get(url).json()

    temp = data["daily"]["temperature_2m_max"][0]
    rain = data["daily"]["precipitation_sum"][0]
    wind = data["daily"]["windspeed_10m_max"][0]

    cursor.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?)",
                   (city, tomorrow, temp, wind, rain))

conn.commit()
conn.close()

print("Weather stored")