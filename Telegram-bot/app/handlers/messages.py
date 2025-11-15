from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..services.verification import verify_user
import logging

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages from users.

    If the user is awaiting an order description, capture it and ask for confirmation.
    Otherwise, ensure the user is registered and provide guidance.
    """
    user = update.effective_user
    message_text = update.message.text.strip() if update.message and update.message.text else ""

    # If user is in the middle of creating an order, capture and ask for confirmation
    if context.user_data.get("awaiting_order"):
        context.user_data["pending_order"] = message_text
        context.user_data["awaiting_order"] = False

        keyboard = [
            [InlineKeyboardButton("✅ Confirmar Pedido", callback_data="confirm_order")],
            [InlineKeyboardButton("❌ Cancelar Pedido", callback_data="cancel_order")],
            [InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")]
        ]
        await update.message.reply_text(
            f"Has enviado el siguiente pedido:\n\n{message_text}\n\n¿Deseas confirmar?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Check registration status
    try:
        is_registered = await verify_user(user.id)
    except Exception:
        logger.exception("Error checking verification status")
        is_registered = False

    if not is_registered:
        keyboard = [
            [InlineKeyboardButton("📝 Registrarse", callback_data="register")],
            [InlineKeyboardButton("ℹ️ ¿Qué es Mandadero?", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 ¡Hola! Para usar Mandadero Bot necesitas registrarte primero.\n\n"
            "El registro es rápido y gratuito.",
            reply_markup=reply_markup
        )
        return

    # Fallback: provide guidance or handle as order in future
    await update.message.reply_text(
        "No entendí ese mensaje. Usa /start para abrir el menú o presiona los botones disponibles."
    )