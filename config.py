import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ensure token is present
if not BOT_TOKEN:
    raise ValueError("⚠️ BOT_TOKEN is missing! Check your .env file.")

DB_NAME = "data/referrals.db"  # Path to SQLite database
