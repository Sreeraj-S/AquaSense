
import numpy as np
import torch

from creation import db, app,logger
from models import AvailMessage
from config import Config
from mqtt import publish




def run_predict_model_inference():
    try:
        device = 'cpu'

        # Load the TorchScript model
        model = torch.jit.load(Config.PREDICT_AVAIL_MODEL)
        model.eval()

        with app.app_context():
            # Fetch the last 7 days of availability data from the database
            results = db.session.query(AvailMessage.payload, AvailMessage.timestamp).order_by(AvailMessage.id.desc()).limit(7).all()
            db.session.close()

            if len(results) < 7:
                logger.error("Not enough data to run the model.")
                return None

            # Convert the last 7 days of availability data to a tensor
            avail_data = []
            days_of_year = []
            for payload, timestamp in results[::-1]:  # Reverse the order to be in chronological order
                avail_data.append(payload if payload is not None else 0)
                days_of_year.append(timestamp.timetuple().tm_yday / 365.0)

            avail_data = np.array(avail_data)
            days_of_year = np.array(days_of_year)
            last_sequence = np.vstack((avail_data, days_of_year)).T
            last_sequence_tensor = torch.tensor(last_sequence, dtype=torch.float32).unsqueeze(0).to(device)
            logger.debug("Last sequence tensor: {}".format(last_sequence_tensor))  # Shape: (1, sequence_length, 2)

        # Perform inference
        with torch.no_grad():
            next_day_avail = model(last_sequence_tensor).item()

        # Print the predicted availability
        predicted_avail = round(next_day_avail)
        logger.debug("Predicted availability for the next day: {}".format(predicted_avail))

        # Send the predicted availability to MQTT
        publish(Config.MQTT_TOPICS["PREDICT_AVAIL"], str(predicted_avail))

        return predicted_avail
    except Exception as e:
        logger.error("Error running the predict model: {}".format(e))
        return None


def run_predict_model():
    result = run_predict_model_inference()
    if result is not None:
        logger.debug("Predict model output: {}".format(result))


def start_predict_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_predict_model, 'interval', hours=24)
    scheduler.start()
    logger.info("Predict scheduler started!")

def stop_predict_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.shutdown()
    logger.info("Scheduler stopped!")

if __name__ == '__main__':
    logger.info("Starting predict model...")
    run_predict_model()
    logger.info("Starting predict scheduler...")
    start_predict_scheduler()


