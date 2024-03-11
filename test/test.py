import unittest
from unittest.mock import patch, MagicMock
from src.main import App

class TestAlwaysPass(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(True)

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_save_event_to_database(self):
        # Mock connection
        mock_connection = MagicMock()
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_connect = MagicMock(return_value=mock_connection)

        with patch('psycopg2.connect', mock_connect):
            self.app.save_event_to_database("2022-01-01", 25.0)

        mock_connect.assert_called_once_with(self.app.DATABASE_URL)
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO public.\"HvacHistory\" (temperature, timestamp, climate_events) VALUES (%s, %s, %s)",
            (25.0, "2022-01-01", self.app.actionType)
        )
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
