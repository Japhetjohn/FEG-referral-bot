import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

print("Starting FEG Army Token Referral Bot...")

try:
    bot.polling(non_stop=True, timeout=60, long_polling_timeout=60)
except Exception as e:
    print(f"Bot encountered an error: {e}")
