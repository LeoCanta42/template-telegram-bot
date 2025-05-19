from telegram import Update
from telegram.ext import ContextTypes
from services.logger import setup_logger

logger = setup_logger(__name__)

def forwarded_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        isForwarded = update.message and update.message.forward_origin is not None
        if not isForwarded:
            logger.debug("Message is not forwarded, ignoring.")
            return True
        return await func(update, context, *args, **kwargs)
    return wrapper

def topic_only(topic_id: int):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if update.message and update.message.is_topic_message and update.message.message_thread_id == topic_id:
                return await func(update, context, *args, **kwargs)
            else:
                logger.debug(f"Message not in topic {topic_id}, ignoring.")
                return True
        return wrapper
    return decorator

def reply_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.message and update.message.reply_to_message:
            return await func(update, context, *args, **kwargs)
        else:
            logger.debug("Message is not a reply, ignoring.")
            return True
    return wrapper

def reply_only_in_topic(topic_id: int):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            if update.message and update.message.reply_to_message and update.message.is_topic_message and update.message.message_thread_id == topic_id:
                if update.message.reply_to_message.message_id != topic_id:
                    return await func(update, context, *args, **kwargs)
            else:
                logger.debug(f"Message is not a real reply in topic {topic_id}, ignoring.")
                return True
        return wrapper
    return decorator
        
def auto_delete_message(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        result = await func(update, context, *args, **kwargs)
        if update.message:
            logger.debug(f"Auto-deleting message: {update.message.message_id}")
            await update.message.delete()
        return result
    return wrapper