from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_temperature(city):
    try:
        weather_api_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        response = requests.get(weather_api_url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['current']['temp_c']
            return temperature
        else:
            return None
    except Exception as e:
        return None

def get_location(client_ip):
    try:
        location_api_url = f"http://ipinfo.io/{client_ip}/json"
        response = requests.get(location_api_url)
        if response.status_code == 200:
            location_data = response.json()
            city = location_data.get("city", "Unknown")
            return city
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    client_ip = request.client.host

    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()

    city = get_location(client_ip)
    temperature = get_temperature(city)
    if temperature is None:
        temperature = "unknown"

    return {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}."
    }
