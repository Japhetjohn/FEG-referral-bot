import telebot
from config import TOKEN, MAIN_TOKEN_CHANNEL, TWITTER_LINK, PARTNERSHIP_CHANNELS
from database import add_user, get_user, add_points, add_wallet, get_wallets

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    user_id = message.from_user.id
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None  

    add_user(user_id, referrer_id)

    referral_link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
    bot.send_message(user_id, f"📌 Your referral link: {referral_link}\n\n"
                              "✅ Complete these tasks:\n"
                              f"- Join the [Telegram group]({MAIN_TOKEN_CHANNEL})\n"
                              f"- Follow us on [Twitter]({TWITTER_LINK})\n"
                              f"- Join our partners: {', '.join(PARTNERSHIP_CHANNELS)}",
                              parse_mode="Markdown")

@bot.message_handler(commands=['addwallet'])
def add_wallet_command(message):
    try:
        wallet_address = message.text.split()[1]
        add_wallet(message.from_user.id, wallet_address)
        bot.send_message(message.chat.id, "✅ Wallet address added successfully!")
    except IndexError:
        bot.send_message(message.chat.id, "⚠️ Please provide a wallet address.\nUsage: `/addwallet <wallet_address>`", parse_mode="Markdown")

@bot.message_handler(commands=['exportwallets'])
def export_wallets(message):
    wallets = get_wallets()
    with open("data/wallets.csv", "w") as file:
        file.write("UserID, WalletAddress\n")
        for user_id, wallet in wallets:
            file.write(f"{user_id}, {wallet}\n")

    with open("data/wallets.csv", "rb") as file:
        bot.send_document(message.chat.id, file)
