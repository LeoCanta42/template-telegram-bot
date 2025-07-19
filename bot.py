import db.money_db
import db.todo_db
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from services.logger import setup_logger
import db
from handlers import register_handlers


def main():
    logger = setup_logger()
    db.money_db.init_db()  # Initialize the money database
    db.todo_db.init_db()  # Initialize the todo database
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    register_handlers(application)
    
    logger.info("Bot running...")
    application.run_polling()

if __name__ == '__main__':
    main()