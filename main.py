import os, io
import telebot
import logging
import urllib.request as urllib2
import requests
from flask import Flask, request

TOKEN = os.environ.get("APIKEY")
WEBHOOK_URL = os.environ.get("MYURL")
appid = os.environ.get("APIWEATHER")

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


def get_filer_by_id(file_id):
    file = bot.get_file(file_id)
    downloaded_file = bot.download_file(file.file_path)
    user_photo = io.BytesIO()
    user_photo.write(downloaded_file)
    user_photo.seek(0)
    return user_photo


# Можно сделать текст кнопки эмодзи

@bot.message_handler(commands=['start'])
def start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start')
    user_markup.row('Прогулки', 'Еда', 'Культура')
    user_markup.row('Узнать погоду в городе')
    bot.send_message(message.from_user.id, 'Привет! 🔥 \nСудя по всему, ты собираешься в путешествие, но ещё определяешься с местом поездки 🤔 \nПредлагаю тебе путешествие в Ханты-Мансийский АО, а именно в город Нижневартовск, который превздоёт все твои ожидания ⬆', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Выбери направление отдыха в меню ниже ⬇:')

@bot.message_handler(commands=['stop'])
def stop(message):
    hide_markup = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.from_user.id, '..', reply_markup=hide_markup)


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == 'Прогулки':
        url = 'https://i.ibb.co/xsWtrcK/1.png'
        urllib2.urlretrieve(url, '1.png')
        img = open('1.png', 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img, 'Для знакомства с городом и его красотами предлагаю тебе следующий маршрут ⬆ \nP.S. Отметил тебе там интересные граффити по пути, на их фоне красивые фотокарточки обеспечены 😉  \nСсылка на маршрут: '
                                                  'https://www.google.com/maps/d/edit?mid=1IiH2vVc59QbSYIV0dXVijYVuXKNaYTJY&usp=sharing')


    if message.text == 'Узнать погоду в городе':
        s_city = "Nizhnevartovsk,RU"
        city_id = 1497543
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            temperature = data['main']['temp']
            bot.send_message(message.from_user.id, "Условия: " + data['weather'][0]['description'] + "\nТемпература: " + str(temperature))

        except Exception as e:
            print("Exception (weather):", e)
            pass


@server.route("/", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "!", 200
