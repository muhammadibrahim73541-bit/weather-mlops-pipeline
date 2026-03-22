import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM weather").fetchall()

weather_text = ""
for r in rows:
    weather_text += f"{r[0]}: Temp {r[2]}°C, Wind {r[3]}, Rain {r[4]}\n"

prompt = f"""
Weather data:

{weather_text}

Write TWO poems:

1. English Poem:
- Compare Lahore, Doha, Aalborg
- Suggest best city

2. Urdu Poem:
- Same idea in Urdu

Keep them clearly separated.
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

poem = response.choices[0].message.content

with open("docs/poem.txt", "w") as f:
    f.write(poem)

print("Poem generated")