FROM python:3.11

WORKDIR /app

ENV SQLALCHEMY_DATABASE_URI=mysql://myuser:mypassword@172.25.0.3/mydatabase

ENV MQTT_BROKER=172.25.0.2
ENV MQTT_PORT=1883
ENV TOP_FILL=esp32/top/fill
ENV BOTTOM_FILL=esp32/bottom/fill
ENV MOTOR=esp32/motor
ENV AVAIL=esp32/avail
ENV PREDICT_AVAIL=esp32/predict_avail
ENV SMART_PUMP=esp32/smart_pump
ENV SMART_PUMP_MODEL=mlmodel/SmartWaterPumpModel.pt
ENV PREDICT_AVAIL_MODEL=mlmodel/PredictWaterAvailModel.pt
ENV MQTT_KEEPALIVE_INTERVAL=45
ENV MOTOR_TIMER=1

COPY . /app
# 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app:app.py

CMD ["python","app.py"]
