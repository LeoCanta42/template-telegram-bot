from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from services.logger import setup_logger
from db.todo_db import init_db
from handlers import register_handlers


def main():
    logger = setup_logger()
    init_db()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    register_handlers(application)
    
    logger.info("Bot running...")
    application.run_polling()

if __name__ == '__main__':
    main()