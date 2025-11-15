#!/usr/bin/env python3
"""
Mandadero Telegram Bot - Production Entry Point
Optimized for PM2 deployment on Hostinger
"""

import sys
import os
import signal
import logging
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
# Ensure the project root is on sys.path so we can import the `app` package
sys.path.insert(0, str(app_dir.parent))

try:
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
    from telegram import Update
    from app.config import TOKEN
    from app.handlers.start import start
    from app.handlers.registration import register
    from app.handlers.admin import admin
    from app.handlers.callbacks import handle_callback
    from app.handlers.messages import handle_message
    from app.services.database import init_db
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all dependencies are installed: pip3 install -r requirements.txt")
    sys.exit(1)

# Configure logging for production
log_dir = app_dir.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global application instance for graceful shutdown
application = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}. Shutting down gracefully...")
    if application:
        application.stop()
    sys.exit(0)

def main() -> None:
    """Start the bot with production configuration."""
    global application
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        logger.info("🤖 Starting Mandadero Telegram Bot...")
        
        # Validate configuration
        if not TOKEN:
            logger.error("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
            sys.exit(1)
        
        # Initialize database
        logger.info("🗄️ Initializing database...")
        init_db()
        logger.info("✅ Database initialized successfully")
        
        # Create the Application
        logger.info("🔧 Creating Telegram application...")
        application = Application.builder().token(TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("register", register))
        application.add_handler(CommandHandler("admin", admin))
        
        # Add callback query handler for inline keyboards
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Add message handler for text messages (should be last)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ All handlers registered (commands, callbacks, messages)")
        
        # Start the bot
        logger.info("🚀 Starting bot polling...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Ignore old updates on restart
        )
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()