import json
import telebot
import requests
import datetime

bot = telebot.TeleBot("6756128598:AAHrS5q0QYfK5isHxRENXuozl4pHAeqAYdw")
API = "d336a5bb399c85686b104a5aa0f4e915"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name}. "
                                      f"Напиши название города, и я составлю прогноз погоды🗿")


@bot.message_handler(content_types=["text"])
def weather(message):
    city = message.text.strip()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        sunrise = str(datetime.datetime.fromtimestamp(data['sys']['sunrise']))[-8:]
        sunset = str(datetime.datetime.fromtimestamp(data['sys']['sunset']))[-8:]
        the_length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                                datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        weathers = {
            "Clear": "Ясная☀️",
            "Clouds": "Облачная☁️",
            "Rain": "Дождливая🌧",
            "Drizzle": "Дождливая🌧",
            "Thunderstorm": "Грозливая🌩",
            "Snow": "Снежливая🌨",
            "Mist": "Туманная🌫",
        }
        a = data['weather'][0]['main']
        if data['weather'][0]['main'] in weathers:
            weather = weathers[a]
        else:
            weather = ''
        bot.reply_to(message, f"Погода в городе {city} на {str(datetime.datetime.today())[:19]}:\n{weather}\n"
                              f"Температура - {temperature}°С🌡\n"
                              f"Влажность воздуха - {humidity}%💧\n"
                              f"Скорость ветра - {wind_speed} м/с💨\n"
                              f"Время восхода - {sunrise}🌅\nВремя заката - {sunset}🌄\n"
                              f"Продолжительность дня - {the_length_of_the_day}⏱")
        bot.send_message(message.chat.id, "Напиши название города, и я составлю прогноз погоды🗿")
    else:
        bot.reply_to(message, "Город указан неверно, попробуйте ещё раз👈")


bot.polling(none_stop=True)
