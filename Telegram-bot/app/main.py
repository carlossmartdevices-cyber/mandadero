from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update
from app.config import TOKEN
from app.handlers.start import start
from app.handlers.registration import register
from app.handlers.admin import admin
from app.handlers.callbacks import handle_callback
from app.handlers.messages import handle_message
from app.services.database import init_db
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("register", register))
        application.add_handler(CommandHandler("admin", admin))

        # Add callback query handler for inline keyboards
        application.add_handler(CallbackQueryHandler(handle_callback))

        # Add message handler for text messages (should be last)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()