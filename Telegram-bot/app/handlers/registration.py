from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..services.database import add_user
from ..services.verification import verify_user

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user registration."""
    user = update.effective_user
    if await verify_user(user.id):
        keyboard = [
            [InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")],
            [InlineKeyboardButton("📋 Mi Perfil", callback_data="profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '✅ Ya estás registrado en Mandadero Bot.\n\n'
            '¡Puedes comenzar a usar todos nuestros servicios!',
            reply_markup=reply_markup
        )
    else:
        success = add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        if success:
            keyboard = [
                [InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")],
                [InlineKeyboardButton("📋 Ver Mi Perfil", callback_data="profile")],
                [InlineKeyboardButton("🛍️ Hacer Mi Primer Pedido", callback_data="make_order")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f'🎉 ¡Registro exitoso, {user.first_name}!\n\n'
                '✅ Tu cuenta ha sido creada correctamente.\n'
                '🚀 Ahora puedes usar todos los servicios de Mandadero Bot.',
                reply_markup=reply_markup
            )
        else:
            keyboard = [
                [InlineKeyboardButton("🔄 Intentar de Nuevo", callback_data="register")],
                [InlineKeyboardButton("📞 Contactar Soporte", callback_data="contact")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                '❌ Error en el registro.\n\n'
                'Es posible que ya estés registrado o haya ocurrido un error técnico.',
                reply_markup=reply_markup
            )