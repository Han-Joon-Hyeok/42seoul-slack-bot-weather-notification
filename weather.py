import requests
import os

from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

lang = "kr"
units = "metric" # 온도 표시 단위(Celsius)

# 서울 종로구 좌표
lat = "37.5683"
lon = "126.9778"

api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&lang={lang}&appid={OPENWEATHER_API_KEY}"

def fetch_data_from_openweather_api():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        return data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    return {}

def parse_weather_data(json):
    data = {
        'description': json['weather'][0]['description'],
        'min_temp': json['main']['temp_min'],
        'max_temp': json['main']['temp_max'],
        'humidity': json['main']['humidity'],
        'wind': json['wind']['speed'],
    }
    return data