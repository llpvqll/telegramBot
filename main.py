import config
import telebot
import requests
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

response = requests.get(config.API_link).json()

lst = []

lst.append(response)
print(lst)


@bot.message_handler(commands=['start', 'help'])
def text_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_usd = types.KeyboardButton("USD")
    button_cad = types.KeyboardButton("EUR")
    button_pln = types.KeyboardButton("RUR")
    button_mxn = types.KeyboardButton("BTC")
    markup.add(button_pln, button_mxn, button_cad, button_usd)
    msg = bot.send_message(message.chat.id, "Find out about the current exchange rate", reply_markup=markup)
    bot.register_next_step_handler(msg, process_coin_step)


def process_coin_step(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)

        for coin in lst:
            for item in coin:
                if message.text == item["ccy"]:

                    bot.send_message(message.chat.id, print_coin(item['buy'], item['sale']), reply_markup=markup, parse_mode="Markdown")

                    print(item['ccy'])
    except Exception as e:
        bot.reply_to(message, "ooops!")


def print_coin(buy, sale):
    '''Displaying the course to the user'''
    return f"Purchase rate: {str(buy)} \nSelling rate: {sale}"


bot.polling(none_stop=True)