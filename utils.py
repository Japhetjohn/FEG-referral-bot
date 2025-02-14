import logging

logging.basicConfig(filename="logs/bot.log", level=logging.INFO)

def log_event(event):
    """Logs bot events to a file."""
    logging.info(event)
