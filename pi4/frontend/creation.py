from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
app = Flask(__name__)

def create_app():
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    from models import (
        TopFillMessage,
        BottomFillMessage,
        AvailMessage,
        MotorMessage
    )
    from models import TopFillMessage, BottomFillMessage, AvailMessage, MotorMessage

    # Import and register blueprints/routes
    from routes import main as main_blueprint

    # Import and start MQTT
    
    import mqtt
    app.register_blueprint(main_blueprint)

    
    return app
