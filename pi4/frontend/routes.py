from flask import Blueprint, render_template, redirect, jsonify
from mqtt import publish
from config import Config
from models import DataSensor

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('status.html')

@main.route('/status')
def status():
    return redirect("/")

@main.route('/controls')
def control():
    return render_template('controles.html')

@main.post('/motor/<data>')
def motor_data(data: str):
    if data not in ["on", "off"]:
        return jsonify({"error": "Invalid data. Only 'on' or 'off' are accepted."}), 400
    print(data)
    publish(Config.MQTT_TOPICS["MOTOR"], 1 if data=="on" else 0)
    return jsonify({"message": "Motor data published successfully."}), 200

@main.route('/data')
def get_data():
    data = {}
    sensors = DataSensor.query.all()
    for sensor in sensors:
        data[sensor.topic] = sensor.payload
    return jsonify(data)

@main.route('/switch/state')
def get_switch_state():
    state = DataSensor.query.filter(DataSensor.topic == Config.MQTT_TOPICS["MOTOR"]).first()
    return jsonify({"state":state.payload})

