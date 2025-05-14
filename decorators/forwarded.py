from telegram import Update
from telegram.ext import ContextTypes

def forwarded_only(func):
    def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.message or not hasattr(update.message,'forward_origin'):
            return
        return func(update, context, *args, **kwargs)
    return wrapper