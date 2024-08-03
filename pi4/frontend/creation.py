import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

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

        logger.info("Database models created successfully")

    # Import and register blueprints/routes
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    logger.info("Blueprints and routes registered successfully")

    return app



