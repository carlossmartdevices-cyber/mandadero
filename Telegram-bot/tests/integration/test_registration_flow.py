import unittest
from unittest.mock import AsyncMock, patch
from app.handlers.registration import register

class TestRegistrationFlow(unittest.TestCase):
    @patch('app.handlers.registration.Update')
    @patch('app.handlers.registration.ContextTypes')
    @patch('app.handlers.registration.verify_user', new_callable=AsyncMock)
    @patch('app.handlers.registration.add_user')
    async def test_registration_flow(self, mock_add_user, mock_verify_user, mock_context, mock_update):
        mock_update.effective_user.id = 123
        mock_update.effective_user.username = 'testuser'
        mock_update.message.reply_text = AsyncMock()
        mock_verify_user.return_value = False
        await register(mock_update, mock_context)
        mock_add_user.assert_called_once_with(123, 'testuser')
        mock_update.message.reply_text.assert_called_once_with('Registration successful!')

if __name__ == '__main__':
    unittest.main()