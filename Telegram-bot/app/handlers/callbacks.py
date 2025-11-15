from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from .start import start
from .registration import register
from ..services.database import get_user
import logging

logger = logging.getLogger(__name__)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callback queries.

    Supported callback_data values: main_menu, register, profile, make_order,
    confirm_order, cancel_order, my_orders, prices, contact, help, about.
    """
    query = update.callback_query
    if not query:
        return

    data = query.data
    user = update.effective_user

    await query.answer()

    try:
        if data == "main_menu":
            await start(update, context)

        elif data == "register":
            await register(update, context)

        elif data == "profile":
            user_record = get_user(user.id)
            if user_record:
                text = (
                    f"📋 Tu perfil:\n\nID: {user_record.id}\nUsuario: @{user_record.username or 'N/A'}\n"
                    f"Nombre: {user_record.first_name or 'N/A'} {user_record.last_name or ''}\n"
                    f"Verificado: {'Sí' if user_record.is_verified else 'No'}"
                )
            else:
                text = "📋 No se encontró tu perfil. Usa /register para crear una cuenta."
            keyboard = [[InlineKeyboardButton("🏠 Menú Principal", callback_data="main_menu")]]
            await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

        elif data == "make_order":
            context.user_data["awaiting_order"] = True
            keyboard = [[InlineKeyboardButton("❌ Cancelar", callback_data="cancel_order")]]
            await query.message.reply_text(
                "📝 Por favor, envía la descripción de tu pedido.",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )

        elif data == "confirm_order":
            pending = context.user_data.get("pending_order")
            if not pending:
                await query.message.reply_text("❌ No hay ningún pedido pendiente para confirmar.")
                return
            await query.message.reply_text(f"✅ Pedido confirmado:\n\n{pending}\n\nNos pondremos en contacto pronto.")
            context.user_data.pop("pending_order", None)
            context.user_data.pop("awaiting_order", None)

        elif data == "cancel_order":
            context.user_data.pop("pending_order", None)
            context.user_data.pop("awaiting_order", None)
            await query.message.reply_text("❌ Pedido cancelado. Si deseas, puedes iniciar uno nuevo desde el menú.")

        elif data == "my_orders":
            await query.message.reply_text("📦 Aquí aparecerán tus pedidos (próximamente).")

        elif data == "prices":
            await query.message.reply_text("💰 Nuestras tarifas disponibles bajo petición.")

        elif data == "contact":
            await query.message.reply_text("📞 Contacto: soporte@mandadero.example")

        elif data == "help":
            await query.message.reply_text("ℹ️ Usa el menú para navegar. Si necesitas ayuda, contacta al soporte.")

        elif data == "about":
            await query.message.reply_text("🚚 Mandadero - Servicio de entrega. ¡Haz tu primer pedido!")

        else:
            logger.info(f"Unknown callback data: {data}")
            await query.message.reply_text("Comando desconocido. Usa el menú principal.")

    except Exception:
        logger.exception("Error handling callback")
        try:
            await query.message.reply_text("❌ Ocurrió un error al procesar tu acción. Intenta de nuevo más tarde.")
        except Exception:
            pass
