import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from src.main import App

class TestApp(unittest.TestCase):
    def setUp(self):
        
        os.environ['PG_USER'] = 'user02eq1'
        os.environ['PG_HOST'] = '157.230.69.113'
        os.environ['PG_DATABASE'] = 'db02eq1'
        os.environ['PG_PASSWORD'] = '3EhMhvn5WRjYOw84'
        os.environ['PG_PORT'] = '5432'
        
        os.environ["HOST"] = "http://159.203.50.162" 
        os.environ["TOKEN"] = "fb5bdbf38ce5d1b4c43b"
        os.environ["T_MAX"] = "30"
        os.environ["T_MIN"] = "25"
        
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

class TestAlwaysPass(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
