from telegram import Update
from telegram.ext import ContextTypes
from services.logger import setup_logger

logger = setup_logger(__name__) 

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg:
        logger.debug("--- New Message ---")
        logger.debug(f"Text: {msg.text}")
        logger.debug(f"Chat ID: {msg.chat_id}")
        logger.debug(f"Message ID: {msg.message_id}")
        logger.debug(f"Date: {msg.date}")
        logger.debug(f"Thread ID: {msg.message_thread_id}")
        logger.debug(f"Is topic: {msg.is_topic_message}")
        logger.debug(f"Forwarded: {msg.forward_origin is not None}")
        logger.debug(f"From user: {msg.from_user.username if msg.from_user else 'Unknown'}")
