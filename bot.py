import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN is missing! Check your .env file.")

# Database path
DB_NAME = "data/referrals.db"


# 🚀 Start Command
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or f"User_{user_id}"
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Ensure the users table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        username TEXT,
        referrer_id INTEGER
    )''')
    
    # Check if user already exists
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Insert new user into the database
        referrer_id = context.args[0] if context.args else None  # Get referral ID if available
        cursor.execute("INSERT INTO users (user_id, username, referrer_id) VALUES (?, ?, ?)", 
                       (user_id, username, referrer_id))
        conn.commit()
    
    conn.close()
    
    await update.message.reply_text(f"👋 Welcome {username}!\n\nUse /mylink to get your referral link.")


# 🔗 Get My Referral Link
async def my_link(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"🔗 Your referral link: https://t.me/YourBotUsername?start={user_id}")


# 👥 Get My Referrals (Fixed)
async def my_referrals(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,))
    referral_count = cursor.fetchone()[0]

    conn.close()

    if referral_count > 0:
        await update.message.reply_text(f"👥 You have referred {referral_count} users!")
    else:
        await update.message.reply_text("🚀 You haven't referred anyone yet. Share your link with /mylink!")


# 🏆 Leaderboard (Fixed)
async def leaderboard(update: Update, context: CallbackContext):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT username, COUNT(*) AS referrals FROM users WHERE referrer_id IS NOT NULL GROUP BY referrer_id ORDER BY referrals DESC LIMIT 10")
    top_users = cursor.fetchall()

    conn.close()

    if top_users:
        leaderboard_text = "🏆 Top Referrers:\n\n"
        for rank, (username, count) in enumerate(top_users, 1):
            leaderboard_text += f"{rank}. {username} - {count} referrals\n"
    else:
        leaderboard_text = "🚀 No referrals yet. Start inviting users!"

    await update.message.reply_text(leaderboard_text)


# 💰 Wallet Command (Store & Retrieve Wallet Address)
async def wallet(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Ensure wallet table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallets (
        user_id INTEGER PRIMARY KEY,
        wallet_address TEXT
    )''')

    # Check if user provided a wallet address
    if context.args:
        wallet_address = context.args[0]
        cursor.execute("INSERT OR REPLACE INTO wallets (user_id, wallet_address) VALUES (?, ?)", (user_id, wallet_address))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ Your wallet address has been saved: `{wallet_address}`")
    else:
        # Retrieve wallet address
        cursor.execute("SELECT wallet_address FROM wallets WHERE user_id = ?", (user_id,))
        wallet = cursor.fetchone()
        conn.close()

        if wallet:
            await update.message.reply_text(f"💰 Your registered wallet address: `{wallet[0]}`")
        else:
            await update.message.reply_text("⚠️ You haven't added a wallet yet. Use `/wallet YOUR_ADDRESS`")


# 🔥 Main Bot Function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Add Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mylink", my_link))
    app.add_handler(CommandHandler("myreferrals", my_referrals))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("wallet", wallet))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
