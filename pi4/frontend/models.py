from creation import db

class DataSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic=db.Column(db.String(500), nullable=False)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class TopFillMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class BottomFillMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class MotorMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class AvailMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class PredictAvailMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class SmartPumpMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
