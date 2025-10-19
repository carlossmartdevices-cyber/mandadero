from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin commands."""
    if str(update.effective_user.id) == ADMIN_ID:
        await update.message.reply_text('Admin commands available.')
    else:
        await update.message.reply_text('You are not authorized to use this command.')