from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..services.verification import verify_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with main menu when the command /start is issued."""
    user = update.effective_user
    is_registered = await verify_user(user.id)
    
    welcome_text = f"🎉 ¡Hola {user.first_name}! Bienvenido a Mandadero Bot\n\n"
    
    if is_registered:
        welcome_text += "✅ Ya estás registrado. ¿Qué te gustaría hacer?"
        keyboard = [
            [InlineKeyboardButton("📋 Mi Perfil", callback_data="profile")],
            [InlineKeyboardButton("🛍️ Hacer Pedido", callback_data="make_order")],
            [InlineKeyboardButton("📦 Mis Pedidos", callback_data="my_orders")],
            [InlineKeyboardButton("💰 Precios", callback_data="prices")],
            [InlineKeyboardButton("📞 Contacto", callback_data="contact")],
            [InlineKeyboardButton("ℹ️ Ayuda", callback_data="help")]
        ]
    else:
        welcome_text += "👋 Para comenzar, necesitas registrarte:"
        keyboard = [
            [InlineKeyboardButton("📝 Registrarse", callback_data="register")],
            [InlineKeyboardButton("ℹ️ ¿Qué es Mandadero?", callback_data="about")],
            [InlineKeyboardButton("📞 Contacto", callback_data="contact")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)