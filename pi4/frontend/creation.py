from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app.config.from_object('config.Config')
    from models import (
    TopFillMessage,
    BottomFillMessage,
    AvailMessage,
    MotorMessage
)
    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Import and register blueprints/routes
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


