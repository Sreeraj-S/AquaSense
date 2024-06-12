from creation import db,app
import paho.mqtt.client as mqtt
from config import Config
from models import MotorMessage,AvailMessage,TopFillMessage,DataSensor,BottomFillMessage


MQTT_BROKER = Config.MQTT_BROKER
MQTT_PORT = Config.MQTT_PORT
MQTT_TOPICS = Config.MQTT_TOPICS
MQTT_KEEPALIVE_INTERVAL = Config.MQTT_KEEPALIVE_INTERVAL

subscribed_topics = set()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in MQTT_TOPICS.values():
        if topic not in subscribed_topics:
            print(topic)
            client.subscribe(topic)
            subscribed_topics.add(topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    with app.app_context():  # Ensure application context is available
        try:
            existing_data = db.session.query(DataSensor).filter_by(topic=msg.topic).first()
            db.session.commit()

            if existing_data:
                print('n')
                existing_data.payload = msg.payload.decode("utf-8")
                print(existing_data.payload)
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
            
            elif msg.topic == MQTT_TOPICS["TOP_FILL"]:
                top_fill_message = TopFillMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(top_fill_message)
            
            elif msg.topic == MQTT_TOPICS["BOTTOM_FILL"]:
                bottom_fill_message = BottomFillMessage(payload=int(msg.payload.decode("utf-8")))
                db.session.add(bottom_fill_message)

            db.session.commit()
        except Exception as e:
            print("Error:", e)
            print("out")
        # Commit changes to the database


        


        

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def mqtt_start():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    mqtt_client.loop_start()

def mqtt_stop():
    mqtt_client.loop_stop()


def publish(topic, data):
    mqtt_client.publish(topic, data)


