from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MQTT_BROKER = os.getenv('MQTT_BROKER')
    MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
    MQTT_TOPICS = {
        "TOP_FILL": os.getenv('TOP_FILL'),
        "BOTTOM_FILL": os.getenv('BOTTOM_FILL'),
        "MOTOR": os.getenv('MOTOR'),
        "AVAIL": os.getenv('AVAIL')
    }
    MQTT_KEEPALIVE_INTERVAL = int(os.getenv('MQTT_KEEPALIVE_INTERVAL', 45))
