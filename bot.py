import logging
import asyncio
import nest_asyncio
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers import start_command, my_link_command, my_referrals_command, leaderboard_command

# Fix event loop issues in Python 3.12
nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
app = Application.builder().token(BOT_TOKEN).build()

# Register bot commands
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("mylink", my_link_command))
app.add_handler(CommandHandler("myreferrals", my_referrals_command))
app.add_handler(CommandHandler("leaderboard", leaderboard_command))

async def main():
    """Main function to run the bot."""
    logger.info("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Run the bot
