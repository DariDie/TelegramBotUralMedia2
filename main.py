import os, io
import telebot
import logging
import urllib.request as urllib2
import requests
from telebot.types import InputMediaPhoto
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
    #user_markup.row('/start')
    user_markup.row('Прогулки', 'Еда', 'Культура')
    user_markup.row('Узнать погоду в городе')
    bot.send_message(message.from_user.id, 'Привет! 🔥 \nСудя по всему, ты собираешься в путешествие, но ещё '
                                           'определяешься с местом поездки 🤔 \nПредлагаю тебе путешествие в '
                                           'Ханты-Мансийский АО, а именно в город Нижневартовск, который превзойдёт '
                                           'все твои ожидания ⬆', reply_markup=user_markup)
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
        bot.send_photo(message.from_user.id, img, 'Для знакомства с городом и его красотами предлагаю тебе следующий '
                                                  'маршрут ⬆ \nP.S. Отметил там интересные граффити по пути, '
                                                  'на их фоне красивые фотокарточки тебе обеспечены 😉  \nСсылка на '
                                                  'маршрут: '
                                                  'https://www.google.com/maps/d/edit?mid=1IiH2vVc59QbSYIV0dXVijYVuXKNaYTJY&usp=sharing')
        bot.send_media_group(message.from_user.id,
                             [InputMediaPhoto('https://i.ibb.co/ZzzhsbN/RR1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/Y2n3mW9/RR.jpg'),
                              InputMediaPhoto('https://i.ibb.co/6YPz6qG/RB1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/mC9JXB9/RB.jpg'),
                              InputMediaPhoto('https://i.ibb.co/PcrCs70/PP1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/B2YjCg6/PP.jpg'),
                              InputMediaPhoto('https://i.ibb.co/RgXk1WV/G3.jpg'),
                              InputMediaPhoto('https://i.ibb.co/ncvL1mG/G2.jpg'),
                              InputMediaPhoto('https://i.ibb.co/SXQW4Yz/G1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/yqRznPV/G.jpg'),
                                ])
        bot.send_message(message.from_user.id, '1⃣ Набережная - самое популярное место для отдыха и прогулок 👍 Это '
                                               'своеобразная визитная карточка города, поскольку именно река Обь '
                                               'является его историческим началом 🌇 \n2⃣ Рябиновый бульвар - '
                                               'пешеходная улица, выполненная с различными архитектурными '
                                               'конструкциями и решением сохранения зелёного фонда 🌱 Кроме того, '
                                               'на бульваре можно увидеть представителей местной фауны - '
                                               'красавцев-снегирей 🥰\n3⃣ Парк победы - важное место для города и его '
                                               'истории. Внутри же него, помимо мемориала и скульптур, можно найти '
                                               'скромный, но не менее интересный парк аттракционов 🎯 \n4⃣ Граффити, '
                                               'которые ты сможешь встретить на своем маршруте. Говорят, на их фоне '
                                               'получаются самые удачные фото 🔥 ')

    if message.text == 'Еда':
        url = 'https://i.ibb.co/92Qtj63/2.png'
        urllib2.urlretrieve(url, '2.png')
        img = open('2.png', 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img,
                       'Для того, чтобы попробовать город на вкус и насладиться красивыми интерьерами, советую тебе '
                       'следующие заведения ⬆ \nP.S. Отметил там интересные граффити по пути, на их фоне красивые '
                       'фотокарточки тебе обеспечены 😉  \nСсылка на маршрут: '
                       'https://www.google.com/maps/d/edit?mid=1NVkQ-9REuwp3BRr8FvpO9WGJFCkbd2kw&usp=sharing')
        bot.send_media_group(message.from_user.id,
                             [InputMediaPhoto('https://i.ibb.co/CJFf7DC/TR1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/yygtWRN/TR.jpg'),
                              InputMediaPhoto('https://i.ibb.co/8d7t7yh/IN1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/pj0Hr1t/IN.jpg'),
                              InputMediaPhoto('https://i.ibb.co/4K0W8XJ/GB1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/HzzCvPb/GB.jpg'),
                              InputMediaPhoto('https://i.ibb.co/q5mtCb2/G4.png'),
                              InputMediaPhoto('https://i.ibb.co/qYZLH3d/G3.png'),
                              InputMediaPhoto('https://i.ibb.co/S6p2c3T/G2.jpg'),
                              InputMediaPhoto('https://i.ibb.co/bJvksFX/G1.jpg'),
                              ])
        bot.send_message(message.from_user.id,
                         '1⃣ "ТрактирЪ на Северной" — идеальное место для людей, любящих отдохнуть от души. Более 10 '
                         'сортов свежего, вкуснейшего напитка, обширный ассортимент горячих блюд и всевозможных '
                         'северных закусок не оставят равнодушным ни одного гостя! 😉 \n2⃣ Lounge cafe «Изба New» - '
                         'новое пространство, где каждая минута обретает смысл🌱Место, где рождаются идеи, '
                         'готовится вкусная еда, играет красивая музыка, встречаются любимые и друзья.🌱 Место, '
                         'где человек как никогда близок к природе  \n3⃣ Ресторан-клуб « Золотой Медведь», '
                         'историческое место в ХМАО, открытый  в  1997 году, с высокой кухней Севера. Это охотничий '
                         'домик где гостям предлагают  насладится, лучшей в  Нижневартовске строганиной, закусками из '
                         'дичи, рубаниной из рыбы, диким мясом и разнообразными настойками собственного приготовления '
                         '🥰 \n4⃣ Граффити, которые ты сможешь встретить на своем маршруте. Говорят, на их фоне '
                         'получаются самые удачные фото 🔥 ')
    if message.text == 'Культура':
        url = 'https://i.ibb.co/rHgbG3V/3.png'
        urllib2.urlretrieve(url, '3.png')
        img = open('3.png', 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        bot.send_photo(message.from_user.id, img,
                       'Если хочешь прикоснуться к истории города, проникнуться его национальным колоритом, '
                       'то тебе сюда! ⬆  \nP.S. Отметил там интересные граффити по пути, на их фоне красивые '
                       'фотокарточки тебе обеспечены 😉  \nСсылка на маршрут: '
                       'https://www.google.com/maps/d/edit?mid=1NVkQ-9REuwp3BRr8FvpO9WGJFCkbd2kw&usp=sharing')
        bot.send_media_group(message.from_user.id,
                             [InputMediaPhoto('https://i.ibb.co/5LHhfZ4/SU1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/wpgjnjd/SU.jpg'),
                              InputMediaPhoto('https://i.ibb.co/vPpNQ1S/RK1.jpg'),
                              InputMediaPhoto('https://i.ibb.co/zHLq7RW/RK.jpg'),
                              InputMediaPhoto('https://i.ibb.co/HPQdNtr/G4.png'),
                              InputMediaPhoto('https://i.ibb.co/4KDZXCc/G3.jpg'),
                              InputMediaPhoto('https://i.ibb.co/JQ6z0Wn/G2.jpg'),
                              InputMediaPhoto('https://i.ibb.co/BjRZcqc/G1.jpg'),
                              ])
        bot.send_message(message.from_user.id,
                         '1⃣ Сибирские увалы - парк был организован осенью 1998 г. в Нижневартовском районе ХМАО по '
                         'инициативе Нижневартовского межрайонного комитета по охране окружающей среды. Необходимость '
                         'создания охраняемой природной территории в Нижневартовском районе была вызвана '
                         'стремительным наступлением на дикую природу нефтяных компаний и ростом экологических '
                         'проблем, вызванных этим 🌿 \n2⃣ Музей истории русского быта - историко-бытовой комплекс, '
                         'раскрывающий историю села Нижневартовского с конца XIX до середины XX веков. Инициатива '
                         'создания в Нижневартовске Музея истории русского быта принадлежит старожилам города, '
                         'идею поддержали представители администрации и сотрудники краеведческого музея и в 1990-х '
                         'годах начались работы по созданию музея 🏛 \n3⃣ Граффити, которые ты сможешь встретить на '
                         'своем маршруте. Говорят, на их фоне '
                         'получаются самые удачные фото 🔥 ')

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
