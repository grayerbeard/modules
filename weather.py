# To get the local air temperature for a location in the UK, you can use the OpenWeatherMap API, which provides weather information for various locations around the world, including the UK.
# To use the OpenWeatherMap API, you will need an API key, which you can obtain by creating a free account on the OpenWeatherMap website.
# Once you have your API key, you can use the requests library in Python to make a request to the API and retrieve the current weather data for your desired location. Here's an example code snippet that demonstrates how to get the local air temperature for a location in the UK using the OpenWeatherMap API:
#python
import requests
import json

# Replace <API_KEY> with your OpenWeatherMap API key
api_key = "31a67209c80c5c442df49e2ed4ac50aa"

# Replace <CITY> and <COUNTRY_CODE> with the name of the city and the ISO 3166 country code, respectively
city = "London"
country_code = "GB"
lat = 52.9716
lon = -2.6908


# Create the API request URL
# url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
# Send the API request and get the response
response = requests.get(url)

# Parse the JSON data in the response
data = response.json()

# Extract the temperature from the data
weather = {}
weather['temperature'] = data["main"]["temp"]
weather['feels_like'] = data['main']['feels_like']
weather['weather'] = data['weather'][0]['main']
weather['description'] = data['weather'][0]['description']
weather['wind_speed'] = data['wind']['speed']
weather['wind_dir'] = data['wind']['deg']
weather['place'] =  data['name']

# Print the temperature
# print(f"The temperature in {city}, {country_code} is {temperature:.1f}°C")
print(f"The temperature in  Lat  {lat} and lon {lon} is {weather['temperature']:.1f}°C")
print(f"The full data set is ",json.dumps(data,indent = 4))
print(weather)
