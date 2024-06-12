import mqtt
from creation import create_app
app = create_app()
if __name__ == '__main__':
    mqtt.mqtt_start()
    app.run(host="0.0.0.0")
