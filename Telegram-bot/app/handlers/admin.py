from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..config import ADMIN_ID

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle admin commands with inline menu."""
    if str(update.effective_user.id) == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("👥 Gestionar Usuarios", callback_data="admin_users")],
            [InlineKeyboardButton("📊 Estadísticas", callback_data="admin_stats")],
            [InlineKeyboardButton("📦 Gestionar Pedidos", callback_data="admin_orders")],
            [InlineKeyboardButton("💰 Configurar Precios", callback_data="admin_prices")],
            [InlineKeyboardButton("📢 Enviar Mensaje Masivo", callback_data="admin_broadcast")],
            [InlineKeyboardButton("⚙️ Configuración", callback_data="admin_settings")],
            [InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '🔧 **Panel de Administración**\n\n'
            'Selecciona una opción para gestionar el bot:',
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")],
            [InlineKeyboardButton("📞 Contactar Soporte", callback_data="contact")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '❌ No tienes permisos de administrador.\n\n'
            'Si crees que esto es un error, contacta al soporte.',
            reply_markup=reply_markup
        )