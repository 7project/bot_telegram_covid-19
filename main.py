import COVID19Py
import telebot
import logging
from config import *
from telebot import apihelper
from datetime import datetime


log = logging.getLogger('telebot')
log.setLevel(logging.INFO)
fh = logging.FileHandler("/var/log/tg_telebot.log", 'a', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)


covid_19 = COVID19Py.COVID19()

# PROXY = '154.16.202.22:8080'
# apihelper.proxy = {
#     'http': 'http://' + PROXY,
#     'https': 'https://' + PROXY,
# }

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    send_text = f'<b>Бот статистики COVID-19. Будь начеку, {message.from_user.first_name}!</b>\nВремя проверки - <b>{datetime.now()}</b>\n' \
                f'Введите страну из списка (США, Испания, Италия, Германия, Китай, Франция, Иран, Англия, Турция, Росcия, Япония, Украина):'
    send_chanel = f'<b>Бот статистики COVID-19.</b>\nВремя проверки - <b>{datetime.now()}</b>\n' \
                  f'Введите страну из списка (США, Испания, Италия, Германия, Китай, Франция, Иран, Англия, Турция, Росcия, Япония, Украина):'
    bot.send_message(message.chat.id, send_text, parse_mode='html')
    # bot.send_message('@covid19word', send_chanel, parse_mode='html')
    log.info(f'Called bot.. name: {message.from_user.first_name}, command: /start')


@bot.message_handler(commands=['map'])
def map(message):
    send_text = f'<b>Карта статистики COVID-19 в мире. Будь начеку, {message.from_user.first_name} - мой руки, сиди дома!</b>\nВремя проверки - <b>{datetime.now()}</b>\n' \
                f'<a href="https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6">Word maps! Press.. me </a>'
    send_chanel = f'<b>Карта статистики COVID-19 в мире.</b>\nВремя проверки - <b>{datetime.now()}</b>\n' \
                  f'<a href="https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6">Word maps! Press.. me </a>'
    bot.send_message(message.chat.id, send_text, parse_mode='html')
    # bot.send_message('@covid19word', send_chanel, parse_mode='html')
    log.info(f'Called bot.. name: {message.from_user.first_name}, command: /map')


@bot.message_handler(content_types=['text'])
def mess(message):
    out_message = ''
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'россия':
        location = covid_19.getLocationByCountryCode('RU')
    elif get_message_bot == 'сша':
        location = covid_19.getLocationByCountryCode('US')
    elif get_message_bot == 'украина':
        location = covid_19.getLocationByCountryCode('UA')
    elif get_message_bot == 'италия':
        location = covid_19.getLocationByCountryCode('IT')
    elif get_message_bot == 'испания':
        location = covid_19.getLocationByCountryCode('ES')
    elif get_message_bot == 'китай':
        location = covid_19.getLocationByCountryCode('CN')
        out_message = f'<u>Данные не корректны!</u>\n<b> Заболевших на 03.04.2020 в Китае: 82 574</b>\n' \
                      f'<u>Данные не корректны!</u>\n<b> Заболевших на 07.04.2020 в Китае: 82 718</b>'
        bot.send_message(message.chat.id, out_message, parse_mode='html')
        # bot.send_message('@covid19word', out_message, parse_mode='html')
        out_message = ''
    elif get_message_bot == 'германия':
        location = covid_19.getLocationByCountryCode('DE')
    elif get_message_bot == 'франция':
        location = covid_19.getLocationByCountryCode('FR')
        out_message = f'<u>Данные не корректны!</u>\n<b> Заболевших на 03.04.2020 в Франции: 90 848</b>\n' \
                      f'<u>Данные не корректны!</u>\n<b> Заболевших на 07.04.2020 в Франции: 98 984</b>'
        bot.send_message(message.chat.id, out_message, parse_mode='html')
        # bot.send_message('@covid19word', out_message, parse_mode='html')
        out_message = ''
    elif get_message_bot == 'иран':
        location = covid_19.getLocationByCountryCode('IR')
    elif get_message_bot == 'япония':
        location = covid_19.getLocationByCountryCode('JP')
    elif get_message_bot == 'англия':
        location = covid_19.getLocationByCountryCode('GB')
        out_message = f'<u>Данные не корректны!</u>\n<b> Заболевших на 03.04.2020 в Англии: 42 479</b>\n' \
                      f'<u>Данные не корректны!</u>\n<b> Заболевших на 07.04.2020 в Англии: 52 301</b>'
        bot.send_message(message.chat.id, out_message, parse_mode='html')
        # bot.send_message('@covid19word', out_message, parse_mode='html')
        out_message = ''
    elif get_message_bot == 'турция':
        location = covid_19.getLocationByCountryCode('TR')
    else:
        location = covid_19.getLatest()
        out_message = f'<u>Данные по всему миру:</u>\n<b> Заболевшие: </b>{location["confirmed"]}'
        log.info(f'Called bot.. name: {message.from_user.first_name}, not_command(message):{get_message_bot}')


    if out_message == '':
        date = location[0]['last_updated'].split('T')
        time = date[1].split('.')
        country_population = location[0]["country_population"]
        people_confirmed = location[0]["latest"]["confirmed"]
        percentage_patients_country = (int(people_confirmed) * 100) / int(country_population)
        out_message = f'<b>Страна - {get_message_bot}</b>\n\n' \
                      f'<b>Время запуска проверки - {datetime.now()}</b>\n' \
                      f'<b>Статистика, обновлено (вчера)* в {time[0]} UTC -5</b>\n\n' \
                      f'<b>Население страны - {location[0]["country_population"]:,}</b>\n' \
                      f'<b>Подтверждены всего - {location[0]["latest"]["confirmed"]} *</b>\n' \
                      f'<b>Погибли - {location[0]["latest"]["deaths"]} * </b>\n\n' \
                      f'<b>Процент заболевших в стране - {percentage_patients_country:.7f} % *</b>'

        print(f'Name: {message.from_user.first_name}, Date: {datetime.now()}')
        log.info(f'Called bot.. name: {message.from_user.first_name}, command: {get_message_bot}')


    bot.send_message(message.chat.id, out_message, parse_mode='html')
    # bot.send_message('@covid19word', out_message, parse_mode='html')

while True:
    try:
        bot.polling(none_stop=True)
        break
    except Exception as e:
        log.exception(f'Exception bot.. message: {e}.')


# счетчик
# count_exp = 0
# while True:
#     try:
#         count_exp = 0
#         bot.polling()
#     except Exception as exp:
#         count_exp += 1
#         print(exp)
#         if count_exp == 3:
#             break
