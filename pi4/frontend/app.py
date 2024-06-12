import mqtt
from creation import create_app

if __name__ == '__main__':
    app = create_app()
    mqtt.mqtt_start()
    app.run(host="0.0.0.0")
