from telegram.ext import ApplicationBuilder, MessageHandler, filters
from config import BOT_TOKEN
from services.logger import setup_logger
from handlers.echo import echo

logger = setup_logger()

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register the echo handler
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    logger.info("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()