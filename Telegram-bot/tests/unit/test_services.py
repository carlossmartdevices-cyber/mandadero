import unittest
from unittest.mock import patch
from app.services.database import add_user, get_user
from app.services.verification import verify_user

class TestServices(unittest.TestCase):
    @patch('app.services.database.cursor')
    def test_add_user(self, mock_cursor):
        add_user(123, 'testuser')
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (id, username) VALUES (?, ?)", (123, 'testuser'))

    @patch('app.services.database.cursor')
    def test_get_user(self, mock_cursor):
        mock_cursor.fetchone.return_value = (123, 'testuser')
        user = get_user(123)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id = ?", (123,))
        self.assertEqual(user, (123, 'testuser'))

    @patch('app.services.verification.get_user')
    async def test_verify_user(self, mock_get_user):
        mock_get_user.return_value = (123, 'testuser')
        result = await verify_user(123)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()