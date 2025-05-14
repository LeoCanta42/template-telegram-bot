from telegram.ext import Application
from telegram.ext import CommandHandler, MessageHandler, filters

from .start import start
from .todo import todo_list, complete, check_forwarded_message
from .debug import debug


def register_handlers(application: Application):
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("todo", todo_list))
    application.add_handler(CommandHandler("done", complete))

    # Message handlers
    application.add_handler(MessageHandler(filters.ALL, debug), group=0)
    application.add_handler(MessageHandler(filters.TEXT, check_forwarded_message), group=1)
