import requests    # module to allow user to send requests and receive data
from geopy import Nominatim   # module to convert cities into long/lat itude 
import json 
from pprint import pprint
from datetime import datetime 

# to activate the virtual environment, execute : .\env\Scripts\activate
# to leave the virutal environment : deactivate

def getCoords(city):
    # get city's geographical coordinates
    geolocator = Nominatim(user_agent="meteo-app")
    try:
        location = geolocator.geocode(city)
        if location is None:
            raise ValueError("No location found for this city")
        print(f"Chosen city, full address: {location.address}")
        return(location)
    except (ValueError) as e:
        print(f"Error: {e}")
        print("Please enter a valid city name")
        return None

def fetchWeather(url, city):
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json() 
        content = {"city": city, "weather": r.json()}
        with open(f"weather{city}.json", "w") as file:
            json.dump(content, file, indent=4)
        print(f"Weather data for {city} successfully fetched and saved as 'weather{city}.json'.")
    else:
        print(f"Failed to fetch weather data for {city}. Please try again.")
    return(data)

def createList (city):
    with open(f"weather{city}.json", "r") as file:
      content = json.load(file)
      today = content["weather"]["daily"]
      
      time = today["time"][0]
      max_temp = today["temperature_2m_max"][0]
      min_temp = today["temperature_2m_min"][0]
      sunrise = today["sunrise"][0]
      sunrise_hour = sunrise[-5:]
      sunset = today["sunset"][0]
      sunset_hour = sunset[-5:]
      precipitation = today["precipitation_sum"][0]
    
    sentence = f"Today in the city of {content['city']}, the sunrise is at {sunrise_hour} and the sunset is at {sunset_hour}. The maximum temperature is {max_temp} °C, the minimum temperature is {min_temp} °C and there will be {precipitation} mm of precipitation."
    print(sentence)

    with open(f"weather{city}.json", "a") as file:
        json.dump(sentence,file)

def main():
    city = input("Enter your city: ")
    coords = getCoords(city)
    while coords is None:
        city = input("Enter your city: ")
        coords = getCoords(city)
    city_display = coords.address[:coords.address.index(",")] + coords.address[coords.address.rindex(","):]
    print(f"Chosen city, short address: {city_display}")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords.latitude}&longitude={coords.longitude}&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum&timezone=Europe%2FLondon" 
    fetchWeather(url, city)
    createList(city)
    
main()