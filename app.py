import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте! Я бот, конвертирующий валюту. \n \
Посмотреть список доступных валют: /values\n \
Увидеть пример заполнения сообщения для конвертации валют: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.send_message(message.chat.id,'Доступние валюты для конвертации:', keys)


@bot.message_handler(commands=['help'])
def instruction(message: telebot.types.Message):
    text = 'Для для того, чтобы я выполнил свою работу введите сообщение в формате: \n \n Название продаваемой валюты <пробел> \n \
Название покупаемой валюты <пробел> \n \
Количество продаваемой валюты <пробел> \n \n Пример сообщения: евро рубль 1'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Кол-во введенных параметров больше трех. Пожалуйста, прочитайте еще раз способ заполнения сообщения для моей корректной работы')

        quote, base, amount = value
        total_base = CryptoConverter.get_price(quote, base, amount)
    except Exception as dar:
        bot.reply_to(message, f'Не получается выполнить задачу\n {dar}')
    except ConvertionException as dar:
        bot.reply_to(message, f'Увы, вы неправильно ввели данные\n {dar}')

    else:
        text = f'Итого {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()