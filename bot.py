import telebot

BOT_TOKEN = "7621286461:AAFG7MCDH4o4q7_xtWl1wI-e0Ts0lEZvmiA"
bot = telebot.TeleBot(BOT_TOKEN)

def start_bot():
    bot.polling(none_stop=True)

start_bot()
