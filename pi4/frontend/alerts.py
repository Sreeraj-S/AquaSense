import requests
from config import Config
from models import Alerts
from creation import app

def call_sms_alert(numbers, message):
    # Check if the API key is available
    with app.app_context():
        api_key = Config.SMS_API_KEY
        if not api_key:
            print("SMS alert failed: API key not available.")
            return {"status": "failed", "error": "API key not available."}

        # Check if sms_alert is enabled in the database
        alert = Alerts.query.filter_by(alert_type="sms_alert").first()
        if not alert or alert.state == 0:
            print("SMS alert disabled: sms_alert is not enabled in the database.")
            return {"status": "skipped", "message": "SMS alert is disabled."}
        print('in')
        # Construct the URL with query parameters
        url = (
            f"https://www.fast2sms.com/dev/bulkV2?"
            f"authorization={api_key}&"
            f"route=q&"
            f"message={message}&"
            f"flash=1&"
            f"numbers={','.join(numbers)}"
        )

        headers = {
            "authorization": api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.get(url, headers=headers)  # Using GET instead of POST
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return {"status": "failed", "error": str(e)}
