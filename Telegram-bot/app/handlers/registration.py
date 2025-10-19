from telegram import Update
from telegram.ext import ContextTypes
from services.database import add_user
from services.verification import verify_user

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user registration."""
    user = update.effective_user
    if await verify_user(user.id):
        await update.message.reply_text('You are already registered.')
    else:
        add_user(user.id, user.username)
        await update.message.reply_text('Registration successful!')