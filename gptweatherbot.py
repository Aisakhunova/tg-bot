import datetime
from config import tg_token_bot, open_weather_token
from aiogram import Bot, types
from aiogram.types import Message
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import filters
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
import logging
import asyncio
import logging
import sys
import requests
from pprint import pprint
from openai import OpenAI
import openai
from config import api_key
import os
import telegram
import pymorphy2

dp = Dispatcher()
openai.api_key = api_key

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я чат бот, который может поддержать общение, а также давать инофомацию о погоде в нужном городе.\nДля этого напиши ключевое слово 'погода' и впиши название города сразу после него. ")
async def get_weather(city, message):
     print("Get WEATHER-----------------------\n")
     code_to_smile = {
         "Clear": "Clear \U00002600",
         "Clouds": "Cloudy \U00002601",
         "Rain": "Rain \U00002614",
         "Drizzle": "Drizzle \U00002614",
         "Thunderstorm": "Thunder!! \U000026A1",
         "Snow": "Snow \U0001F328",
         "Mist": "Mist \U0001F328",
     }
     r = requests.get(
         f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
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
     await message.answer(
        f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\nПогода в {city}: \nТемпература {current_temperature}°C {ed}\nСкорость ветра - {wind} m/s\nДавление {pressure}"
        f"\nВлажность {humidity}\nРассвет в {sunrise_time}\nЗакат в {sunset_time}\nХорошего дня!!"
    )

def extract_city_from_message(text):
    print("________EXTCACT CITY_____\n")

    keyword = 'погода'

    morph = pymorphy2.MorphAnalyzer()

    words = text.lower().split()


    if keyword in words:

        city_indices = [i + 1 for i, word in enumerate(words) if word == keyword and i + 1 < len(words)]
        potential_cities = [words[index] for index in city_indices]
        normalized_cities = [morph.parse(city)[0].normal_form for city in potential_cities]

        if normalized_cities:
            print(normalized_cities[0], "________CITY_____\n")
            return normalized_cities[0]

    return None

@dp.message()
async def send_something(message: Message):

        if 'погода' in message.text.lower() or 'weather' in message.text.lower():

            city = extract_city_from_message(message.text)
            if city:
                await get_weather(city, message)
            else:
                await message.answer("Не удалось определить город. Пожалуйста, уточните запрос.")
        else:

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": message.text
                }],
                temperature=0.5,
                max_tokens=1024,
                top_p=1
            )

            assistant_reply = response.choices[0].message.content

            bot_with_html_parse_mode = Bot(tg_token_bot, parse_mode=ParseMode.HTML)
            await bot_with_html_parse_mode.send_message(message.chat.id, text=assistant_reply)

            pprint(assistant_reply)

async def main() -> None:
    bot = Bot(tg_token_bot, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
