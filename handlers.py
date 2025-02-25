from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

# Start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("💰 My Link", callback_data="my_link"),
        InlineKeyboardButton("📜 My Referrals", callback_data="my_referrals"),
    ], [
        InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚀 Welcome to the FEG Army Referral Bot!\n\n"
        "🔹 Earn rewards by referring friends!\n"
        "🔹 Use the buttons below to track your progress.\n\n"
        "👇 Choose an option:",
        reply_markup=reply_markup
    )

# My Link command
async def my_link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 Your referral link: https://t.me/yourbot?start=123456")

# My Referrals command
async def my_referrals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 You have referred: 5 users")

# Leaderboard command
async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏆 Top 3 referrers:\n1. @user1 - 50 refs\n2. @user2 - 40 refs\n3. @user3 - 30 refs")
