import telebot
import requests
import json

TOKEN = "6117486820:AAF-wcAI2j-fnQ_i5nPzUqMWlRAE3xB-qYo"

"""red = redis.Redis(
    host='localhost',
    port=6379
) """

bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD'
}

class ConvertionExeptions(Exception):



    @bot.message_handler(commands=['start', 'help'])
    def help(message: telebot.types.Message):
        text = "Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \n Увидеть список всех доступных валют: /values"
        bot.reply_to(message, text)

    @bot.message_handler(commands=['values'])
    def values(message: telebot.types.Message):
        text = "Доступные валюты: "
        for key in keys.keys():
            text = '\n'.join((text, key, ))
        bot.reply_to(message, text)

    @bot.message_handler(content_types=['text', ])
    def convert(message: telebot.types.Message):
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionExeptions('Слишком много параметров')

        quote, base, amount = values

        if quote == base:
            raise ConvertionExeptions(f'Невозможно перевести одинаковые валюты {base}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        total_base = json.loads(r.content)[keys[base]]
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()