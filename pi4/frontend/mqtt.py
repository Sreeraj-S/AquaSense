
from creation import db,app,logger
import paho.mqtt.client as mqtt
from config import Config
from models import MotorMessage,AvailMessage,TopFillMessage,DataSensor,BottomFillMessage,PredictAvailMessage
from scheduler import run_model


MQTT_BROKER = Config.MQTT_BROKER
MQTT_PORT = Config.MQTT_PORT
MQTT_TOPICS = Config.MQTT_TOPICS
MQTT_KEEPALIVE_INTERVAL = Config.MQTT_KEEPALIVE_INTERVAL

subscribed_topics = set()


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    for topic in MQTT_TOPICS.values():
        if topic not in subscribed_topics:
            client.subscribe(topic)
            subscribed_topics.add(topic)

def on_message(client, userdata, msg):
    with app.app_context():  # Ensure application context is available
        try:
            existing_data = db.session.query(DataSensor).filter_by(topic=msg.topic).first()
            db.session.commit()

            if existing_data:
                existing_data.payload = msg.payload.decode("utf-8")
                logger.info(existing_data.payload)
                db.session.commit()
            else:
                data_sensor = DataSensor(topic=msg.topic, payload=int(msg.payload.decode("utf-8")))
                db.session.add(data_sensor)
                db.session.commit()
            if msg.topic == MQTT_TOPICS["MOTOR"]:
                motor_message = MotorMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(motor_message)
            
            elif msg.topic == MQTT_TOPICS["AVAIL"]:
                avail_message = AvailMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(avail_message)
            elif msg.topic == MQTT_TOPICS["PREDICT_AVAIL"]:
                predict_avail_message = PredictAvailMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(predict_avail_message)
            
            elif msg.topic == MQTT_TOPICS["SMART_PUMP"]:
                predict_avail_message = PredictAvailMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(predict_avail_message)
            
            elif msg.topic == MQTT_TOPICS["TOP_FILL"]:
                top_fill_message = TopFillMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(top_fill_message)
                if top_fill_message > 90 and db.session.query(DataSensor).filter(DataSensor.topic == MQTT_TOPICS["MOTOR"]).first().payload == 1:
                    publish(MQTT_TOPICS["MOTOR"], 0)
                if top_fill_message < 10 and db.session.query(DataSensor).filter(DataSensor.topic == MQTT_TOPICS["MOTOR"]).first().payload == 0:
                    run_model()
            elif msg.topic == MQTT_TOPICS["BOTTOM_FILL"]:
                bottom_fill_message = BottomFillMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(bottom_fill_message)
                

            db.session.commit()
        except Exception as e:
            logger.error("Error:", e)
            logger.error("out")
        # Commit changes to the database


        


        

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def mqtt_start():
    logger.info("Connecting to MQTT broker...")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqtt_client.loop_start()
    logger.info("Connected to MQTT broker.")

def mqtt_stop():
    logger.info("Disconnecting from MQTT broker...")
    mqtt_client.loop_stop()
    logger.info("Disconnected from MQTT broker.")


def publish(topic, data):
    mqtt_client.publish(topic, data)



