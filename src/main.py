"""Imports"""
import os
import logging
import json
import time
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder
import psycopg2

class App:
    """Class for server app"""

    def __init__(self):
        self._hub_connection = None
        self.TICKS = 10
        
        self.actionType = "Normal"
        
        self.PG_USER = os.environ["PG_USER"]
        self.PG_HOST = os.environ["PG_HOST"]
        self.PG_DATABASE = os.environ["PG_DATABASE"]
        self.PG_PASSWORD = os.environ["PG_PASSWORD"]
        self.PG_PORT = os.environ["PG_PORT"]
        
        # To be configured by your team
        self.HOST = os.environ["HOST"] #"http://159.203.50.162"
        self.TOKEN = os.environ["TOKEN"] #"fb5bdbf38ce5d1b4c43b"
        self.T_MAX = os.environ["T_MAX"] #testttttt
        self.T_MIN = os.environ["T_MIN"]
        self.DATABASE_URL = f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}" #os.environ["DB_URL"]

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )
        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            self.take_action(temperature)
            self.save_event_to_database(timestamp, temperature)
        except Exception as err:
            print(err)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac("TurnOnAc")
            self.actionType = "AC"
            print("AC TIME")
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac("TurnOnHeater")
            self.actionType = "HEAT"
            print("HEAT TIME")

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def save_event_to_database(self, timestamp, temperature):
        """Save sensor data into database."""
        connection = None
        curs = None
        try:
            # To implement
            connection = psycopg2.connect(self.DATABASE_URL)
            curs = connection.cursor()
            
            query = "INSERT INTO public.\"HvacHistory\" (temperature, timestamp, climate_events) VALUES (%s, %s, %s)"
            curs.execute(query, (temperature, timestamp, self.actionType))
            
            connection.commit()
            print("Hvac info saved.")
            pass
        except requests.exceptions.RequestException as e:
            # To implement
            pass
        finally:
            if curs is not None:
                curs.close()
            if connection is not None:
                connection.close()


if __name__ == "__main__":
    app = App()
    app.start()
