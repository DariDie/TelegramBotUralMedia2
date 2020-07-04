import os, io
import telebot
import logging
import urllib.request as urllib2
import requests
from flask import Flask, request


TOKEN = os.environ.get("APIKEY")
WEBHOOK_URL = os.environ.get("MYURL")

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

#Можно сделать текст кнопки эмодзи

@bot.message_handler(commands=['start'])
def start(message):
	#bot.send_message(message.chat.id, "Привет! Пришли мне фото!")
	user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
	user_markup.row('/start', '/stop')
	user_markup.row('1', '2', '3')
	bot.send_message(message.from_user.id, 'Добро пожаловать...', reply_markup=user_markup)

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
		bot.send_photo(message.from_user.id, img)
		bot.send_message(message.from_user.id, 'Графити "Вартовчанка')
		bot.send_message(message.from_user.id, 'Ссылка на маршрут: https://i.ibb.co/GsVDNQH/0-Lus2-Gx-Qesk.jpg')

	if message.text == '2':
		s_city = "Nizhnevartovsk,RU"
		city_id = 0
		appid = 'd230fcb17786fe3d64e9332ee331e2f9'
		try:
			res = requests.get("http://api.openweathermap.org/data/2.5/find",
							   params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
			data = res.json()
			cities = ["{} ({})".format(d['name'], d['sys']['country'])
					  for d in data['list']]
			print("city:", cities)
			city_id = data['list'][0]['id']
			print('city_id=', city_id)
		except Exception as e:
			print("Exception (find):", e)
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