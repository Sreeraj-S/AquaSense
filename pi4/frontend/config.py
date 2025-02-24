from dotenv import load_dotenv
import os
from creation import logger
# Load environment variables from .env file
load_dotenv()

logger.info("Loading environment variables from .env file")

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
        "AVAIL": os.getenv('AVAIL'),
        "PREDICT_AVAIL": os.getenv('PREDICT_AVAIL'),
        "SMART_PUMP": os.getenv('SMART_PUMP'),
        "PH_SENSOR": os.getenv('PH_SENSOR')
    }
    SMART_PUMP_MODEL=os.getenv('SMART_PUMP_MODEL')
    MQTT_KEEPALIVE_INTERVAL = int(os.getenv('MQTT_KEEPALIVE_INTERVAL', 45))
    PREDICT_AVAIL_MODEL=os.getenv('PREDICT_AVAIL_MODEL')
    MOTOR_TIMER=int(os.getenv('MOTOR_TIMER', 7))
    logger.info("Environment variables loaded")
