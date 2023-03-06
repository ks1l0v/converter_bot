import telebot
import requests
import re
from config import *

bot = telebot.TeleBot(TOKEN)


@bot.channel_post_handler()
def send_message(message):
    valuta = requests.get('https://cbu.uz/ru/arkhiv-kursov-valyut/json/').json()
    yuan = re.findall(r'\d+\s*[юЮ][Аа][Нн]*\w+', message.text)

    if yuan:
        final_text = ''
        split_text = re.split(r'\d+\s*[юЮ][Аа][Нн]*\w+', message.text)
        i = n = 0

        while len(split_text) > i and len(yuan) > n:
            final_text += split_text[i] + yuan[n] + \
                          f'({(int(yuan[i].split(" ")[0]) * float(valuta[14]["Rate"]))} сум)'
            i, n = i+1, n+1

        while len(split_text) > i:
            final_text += split_text[i]
            i += 1

        while len(yuan) > n:
            final_text += str(yuan[n]) + f'({(int(yuan[i].split(" ")[0]) * float(valuta[14]["Rate"]))} сум)'
            n += 1

        bot.edit_message_text(final_text, message.chat.id, message.id)



bot.polling(none_stop=True)