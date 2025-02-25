import sqlite3
from telegram import Update
from telegram.ext import CallbackContext

# 🏆 Leaderboard Command
def leaderboard(update: Update, context: CallbackContext):
    conn = sqlite3.connect("data/referrals.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, points FROM users ORDER BY points DESC LIMIT 10")
    top_users = cursor.fetchall()
    conn.close()

    if not top_users:
        update.message.reply_text("❌ No users found in the leaderboard.")
        return

    leaderboard_text = "🏆 *Leaderboard (Top 10)* 🏆\n\n"
    for rank, (username, points) in enumerate(top_users, 1):
        leaderboard_text += f"{rank}. {username} - {points} points\n"

    update.message.reply_text(leaderboard_text, parse_mode="Markdown")

# 👥 My Referrals Command
def my_referrals(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    conn = sqlite3.connect("data/referrals.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM referrals WHERE referrer_id = ?", (user_id,))
    referral_count = cursor.fetchone()[0]
    conn.close()

    if referral_count == 0:
        update.message.reply_text("😕 You haven't referred anyone yet.")
    else:
        update.message.reply_text(f"👥 You have referred *{referral_count}* users!", parse_mode="Markdown")
