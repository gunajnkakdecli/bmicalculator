import requests
from config import WEATHER_API_KEY

city = "Bhopal"

url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
)

response = requests.get(url)

print(response.json())