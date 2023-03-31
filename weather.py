import requests
import yaml

class class_weather:
    def __init__(self, api_key, lat, lon):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        
    def get_weather(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        weather = {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "weather": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "wind_dir": data["wind"]["deg"],
            "place": data["name"]
        }
        
        return weather

def test_weather():
    with open("/home/pi/.config/tests/config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    print(f"Config: {config}")

    wg = class_weather(config["api_key"], config["lat"], config["lon"])
    weather = wg.get_weather()

    # Print the weather information
    print(f"The temperature in {weather['place']} is {weather['temperature']}°C")
    print(f"Feels like: {weather['feels_like']}°C")
    print(f"Weather Type: {weather['weather']}")
    print(f"Weather Description: {weather['description']}")
    print(f"Wind Speed: {weather['wind_speed']} m/s")
    print(f"Wind Direction: {weather['wind_dir']} degrees")

if __name__ == '__main__':
    test_weather()
