import mqtt
from creation import create_app,logger
from scheduler import start_scheduler
from predict_scheduler import start_predict_scheduler

if __name__ == '__main__':
    
    logger.info("Starting the application")
    app = create_app()
    logger.info("Starting the MQTT client")
    mqtt.mqtt_start()
    logger.info("Starting the predict scheduler")
    start_predict_scheduler()
    logger.info("Starting the scheduler")
    start_scheduler()
    logger.info("Starting the application server")
    app.run(host="0.0.0.0")
    logger.info("Stopping the application server")
    logger.info("Stopping the MQTT client")
    mqtt.mqtt_stop()
    logger.info("Stopping the predict scheduler")
    logger.info("Stopped!!!")

    
