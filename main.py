import requests
import datetime
from config import open_weather_token
from pprint import pprint

def get_weather(city, open_weather_token):

    code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clear \U00002601",
        "Rain": "Clear \U00002614",
        "Drizzle": "Clear \U00002614",
        "Thunderstorm": "Clear \U000026A1",
        "Snow": "Clear \U0001F328",
        "Mist": "Clear \U0001F328",
    }
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
        data = r.json()
        pprint(data)

        city = data["name"]
        current_temperature = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            ed = code_to_smile[weather_description]
        else:
            ed = "open the window bro"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunrise_time - sunset_time

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\nWeather in {city}: \nTemperature is {current_temperature}°C {ed}\nWind is {wind} m/s\nPressure is {pressure}"
              f"\nHumidity is {humidity}\nSunrise is at {sunrise_time} and Sunset is at {sunset_time}\nHave a good day!!")

    except Exception as ex:
        print(ex)
        print("Enter valid weather")

def main():
    city = input("Enter your city name: ")
    get_weather(city, open_weather_token)

if __name__ == "__main__":
    main()