from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
import time

app = Flask(__name__)
socketio = SocketIO(app)


MQTT_BROKER = "172.25.0.2"
MQTT_PORT = 1883
MQTT_TOPICS = ["esp32/top/fill", "esp32/bottom/fill","esp32/motor"]
MQTT_KEEPALIVE_INTERVAL = 45

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    for topic in MQTT_TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    socketio.emit('mqtt_message', {'topic': msg.topic, 'data': msg.payload.decode("utf-8")})

mqtt_client =  mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    mqtt_client.loop_start() 

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    mqtt_client.loop_stop()

if __name__ == '__main__':
    socketio.run(app, debug=True)
