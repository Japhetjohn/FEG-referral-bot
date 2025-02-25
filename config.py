import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the bot token
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("Bot token is missing! Check your .env file.")
