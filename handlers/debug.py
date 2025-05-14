from telegram import Update
from telegram.ext import ContextTypes
from services.logger import setup_logger

logger = setup_logger(__name__) 

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if msg:
        logger.info("--- New Message ---")
        logger.info(f"Text: {msg.text}")
        logger.info(f"Chat ID: {msg.chat_id}")
        logger.info(f"Message ID: {msg.message_id}")
        logger.info(f"Date: {msg.date}")
        logger.info(f"Thread ID: {msg.message_thread_id}")
        logger.info(f"Is topic: {msg.is_topic_message}")
        logger.info(f"Forwarded: {msg.forward_origin is not None}")
        logger.info(f"From user: {msg.from_user.username if msg.from_user else 'Unknown'}")
