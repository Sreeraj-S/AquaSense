FROM python:3.11

WORKDIR /app

ENV SQLALCHEMY_DATABASE_URI=mysql://myuser:mypassword@172.25.0.3/mydatabase

ENV MQTT_BROKER=172.25.0.2
ENV MQTT_PORT=1883t
ENV TOP_FILL=esp32/top/fill
ENV BOTTOM_FILL=esp32/bottom/fill
ENV MOTOR=esp32/motor
ENV AVAIL=esp32/avail
ENV MQTT_KEEPALIVE_INTERVAL=45


COPY . /app
# --no-cache-dir
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app:app.py

CMD ["sh", "-c", "flask db migrate -m \"Initial migration.\" && flask db upgrade && python app.py"]
