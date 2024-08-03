from flask import Blueprint, render_template, redirect, jsonify
from mqtt import publish
from config import Config
from models import DataSensor
from scheduler import run_model
from predict_scheduler import run_predict_model

from creation import logger


main = Blueprint('main', __name__)


@main.route('/')
def index():
    logger.debug("Loading status page")
    return render_template('status.html')

@main.route('/status')
def status():
    logger.debug("Redirecting to status page")
    return redirect("/")

@main.route('/controls')
def control():
    logger.debug("Loading controls page")
    return render_template('controles.html')

@main.route('/ai_result')
def ai_result():
    logger.debug("Loading AI result page")
    return render_template('ai_result.html')

@main.post('/motor/<data>')
def motor_data(data: str):
    if data not in ["on", "off"]:
        logger.error("Invalid data. Only 'on' or 'off' are accepted.")
        return jsonify({"error": "Invalid data. Only 'on' or 'off' are accepted."}), 400
    logger.debug("Received %s data", data)
    publish(Config.MQTT_TOPICS["MOTOR"], 1 if data=="on" else 0)
    logger.info("Motor data published successfully.")
    return jsonify({"message": "Motor data published successfully."}), 200

@main.route('/data')
def get_data():
    logger.debug("Getting data")
    data = {}
    sensors = DataSensor.query.all()
    for sensor in sensors:
        data[sensor.topic] = sensor.payload
    logger.debug("Sending data: %s", data)
    return jsonify(data)

@main.route('/data/ai')
def get_ai_data():
    logger.debug("Getting AI data")
    data = {}
    sensors = DataSensor.query.with_entities(DataSensor.topic, DataSensor.payload, DataSensor.timestamp)\
        .filter(DataSensor.topic.in_([Config.MQTT_TOPICS["PREDICT_AVAIL"], Config.MQTT_TOPICS["SMART_PUMP"]]))\
        .all()
    logger.debug("Sensors: %s", sensors)
    for sensor in sensors:
        tempData = {"result":sensor.payload,"timestamp":str(sensor.timestamp)}
        data[sensor.topic] = tempData
    logger.debug("Data: %s", data)
    return jsonify(data)

@main.route('/switch/state')
def get_switch_state():
    logger.debug("Getting switch state")
    state = DataSensor.query.filter(DataSensor.topic == Config.MQTT_TOPICS["MOTOR"]).first()
    if state:
        logger.debug("State: %s", state.payload)
        return jsonify({"state":state.payload})
    else:
        logger.debug("State: 0")
        return jsonify({"state":0})
    
@main.post('/run/smart-pump')
def run_smart_pump():
    logger.debug("Running smart pump")
    state = DataSensor.query.filter(DataSensor.topic == Config.MQTT_TOPICS["MOTOR"]).first()
    if state and state.payload == 1:
        logger.error("Motor is on. Turn it off for smart pump to work.")
        return jsonify({"error": "Motor is on. Turn it off for smart pump to work."}), 400
    try:
        run_model()
        return jsonify({"message": "Model run successfully."}), 200
    except:
        logger.error("Failed to run the model.")
        return jsonify({"error": "Failed to run the model."}), 400
@main.post('/run/predict-avail')
def run_predict_avail():
    logger.debug("Running predict avail")
    try:
        run_predict_model()
        return jsonify({"message": "Model run successfully."}), 200
    except:
        logger.error("Failed to run the model.")
        return jsonify({"error": "Failed to run the model."}), 400


