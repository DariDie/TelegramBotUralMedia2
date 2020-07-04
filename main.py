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
    # bot.send_message(message.chat.id, "Привет! Пришли мне фото!")
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start')
    user_markup.row('1', '2', '3')
    bot.send_message(message.from_user.id, 'Привет!🔥 \nСудя по всему, ты собираешься в путешествие, но ещё определяешься с местом поездки🤔 \nПредлагаю тебе путешествие в Ханты-Мансийский АО, а именно в город Нижневартовск, который превздоёт все твои ожидания ⬆', reply_markup=user_markup)
    bot.send_message(message.from_user.id, 'Выбери направление отдыха в меню ниже⬇:')

@bot.message_handler(commands=['stop'])
def stop(message):
    hide_markup = telebot.types.ReplyKeyboardHide()
    bot.send_message(message.from_user.id, '..', reply_markup=hide_markup)


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == '1':
        url = 'https://i.ibb.co/GsVDNQH/0-Lus2-Gx-Qesk.jpg'
        urllib2.urlretrieve(url, '0-Lus2-Gx-Qesk.jpg')
        img = open('0-Lus2-Gx-Qesk.jpg', 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img, 'Графити "Вартовчанка, Ссылка на маршрут: '
                                                  'https://i.ibb.co/GsVDNQH/0-Lus2-Gx-Qesk.jpg')
    # bot.send_message(message.from_user.id, 'Графити "Вартовчанка')
    # bot.send_message(message.from_user.id, 'Ссылка на маршрут: https://i.ibb.co/GsVDNQH/0-Lus2-Gx-Qesk.jpg')

    if message.text == '2':
        s_city = "Nizhnevartovsk,RU"
        city_id = 1497543
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            #bot.send_message(message.from_user.id, "Условия: " + data['weather'][0]['description'])
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
