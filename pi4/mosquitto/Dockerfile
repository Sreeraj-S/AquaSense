# Use the official Eclipse Mosquitto image as base
FROM eclipse-mosquitto

# Expose MQTT ports
EXPOSE 1883


COPY mosquitto.conf mosquitto.conf

# Define the entrypoint command to start Mosquitto
CMD ["/usr/sbin/mosquitto", "-c", "mosquitto.conf"]
