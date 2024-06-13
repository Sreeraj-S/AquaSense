import torch
import time
import requests

from creation import db, app,logger
from models import DataSensor
from config import Config
from mqtt import publish
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

def start_motor():
    try:
        response_on = requests.post("http://127.25.0.4:5000/motor/on")
        if response_on.status_code == 200:
            logger.info("Motor turned on.")
        else:
            logger.warning("Failed to turn on the motor.")
    except Exception as e:
        logger.error("Error starting motor: %s", e)

def stop_motor():
    try:
        response_off = requests.post("http://127.25.0.4:5000/motor/off")
        if response_off.status_code == 200:
            logger.info("Motor turned off.")
        else:
            logger.warning("Failed to turn off the motor.")
    except Exception as e:
        logger.error("Error stopping motor: %s", e)

def run_model_inference():
    try:
        device = 'cpu'

        # Load the TorchScript model
        model = torch.jit.load(Config.SMART_PUMP_MODEL)
        model.eval()

        with app.app_context():
            # Fetch payloads for the required topics
            topics = [
                Config.MQTT_TOPICS["AVAIL"],
                Config.MQTT_TOPICS["PREDICT_AVAIL"],
                Config.MQTT_TOPICS["BOTTOM_FILL"],
                Config.MQTT_TOPICS["TOP_FILL"]
            ]
            data = {topic: 0 for topic in topics}  # Initialize with default values

            results = db.session.query(DataSensor.topic, DataSensor.payload).filter(DataSensor.topic.in_(topics)).all()
            db.session.close()

            # Update data with actual values retrieved from the database
            for topic, payload in results:
                data[topic] = payload if payload is not None else 0

        # Ensure the input tensor is in the correct order and process the values
        avail = data[Config.MQTT_TOPICS["AVAIL"]]
        predict_avail = data[Config.MQTT_TOPICS["PREDICT_AVAIL"]]
        bottom_fill = data[Config.MQTT_TOPICS["BOTTOM_FILL"]] / 100
        top_fill = data[Config.MQTT_TOPICS["TOP_FILL"]] / 100

        test_input = torch.tensor([avail, predict_avail, bottom_fill, top_fill]).to(device)

        # Perform inference
        with torch.no_grad():
            outputs = model(test_input)

        # Convert the output to the desired scale and print
        result = int(outputs.item() * 5)
        logger.info("Output: %d", result)

        # Send the output to MQTT
        publish(Config.MQTT_TOPICS["SMART_PUMP"], str(result))

        return result
    except Exception as e:
        logger.error("Error running the model: %s", e)
        return None

def run_model():
    result = run_model_inference()
    if result is not None:
        logger.info("Model output: %d", result)
        start_motor_timer(result)

def start_motor_timer(duration):
    try:
        duration = duration*Config.MOTOR_TIMER
        scheduler = BackgroundScheduler()
        scheduler.add_job(stop_motor, 'date', run_date=datetime.now() + timedelta(minutes=duration))
        start_motor()
        scheduler.start()
        logger.info(f"Motor timer started for {duration} minutes.")
    except Exception as e:
        logger.error("Error starting motor timer: %s", e)

def stop_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.shutdown()
    logger.info("Scheduler stopped!")

def start_scheduler():
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_model, 'interval', hours=1)
    scheduler.start()
    logger.info("Scheduler started!")

if __name__ == '__main__':
    run_model()
    try:
        start_scheduler()
    finally:
        stop_scheduler()
