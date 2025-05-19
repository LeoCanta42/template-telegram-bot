from telegram.ext import Application
from telegram.ext import CommandHandler, MessageHandler, filters

from .start import start
from .todo import todo_list, complete, check_forwarded_message, delete_messages_sent
from .debug import debug


def register_handlers(application: Application):
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("todo", todo_list))

    # Message handlers
    application.add_handler(MessageHandler(filters.ALL, debug), group=0)
    application.add_handler(MessageHandler(filters.TEXT, check_forwarded_message), group=1)
    application.add_handler(MessageHandler(filters.TEXT, complete), group=2)
    application.add_handler(MessageHandler(filters.TEXT, delete_messages_sent), group=3)
