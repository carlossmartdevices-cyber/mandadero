import unittest
from unittest.mock import AsyncMock, patch
from app.handlers.start import start
from app.handlers.registration import register
from app.handlers.admin import admin

class TestHandlers(unittest.TestCase):
    @patch('app.handlers.start.Update')
    @patch('app.handlers.start.ContextTypes')
    async def test_start(self, mock_context, mock_update):
        mock_update.message.reply_text = AsyncMock()
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with('Hi! Use /register to register.')

    @patch('app.handlers.registration.Update')
    @patch('app.handlers.registration.ContextTypes')
    @patch('app.handlers.registration.verify_user', new_callable=AsyncMock)
    @patch('app.handlers.registration.add_user')
    async def test_register(self, mock_add_user, mock_verify_user, mock_context, mock_update):
        mock_update.effective_user.id = 123
        mock_update.effective_user.username = 'testuser'
        mock_update.message.reply_text = AsyncMock()
        mock_verify_user.return_value = False
        await register(mock_update, mock_context)
        mock_add_user.assert_called_once_with(123, 'testuser')
        mock_update.message.reply_text.assert_called_once_with('Registration successful!')

    @patch('app.handlers.admin.Update')
    @patch('app.handlers.admin.ContextTypes')
    async def test_admin(self, mock_context, mock_update):
        mock_update.effective_user.id = 1
        mock_update.message.reply_text = AsyncMock()
        await admin(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with('Admin commands available.')

if __name__ == '__main__':
    unittest.main()