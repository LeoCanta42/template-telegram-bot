from telegram import Update
from telegram.ext import ContextTypes
from services.logger import setup_logger

logger = setup_logger(__name__)

def forwarded_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        isForwarded = update.message and update.message.forward_origin is not None
        if not isForwarded:
            return
        return await func(update, context, *args, **kwargs)
    return wrapper