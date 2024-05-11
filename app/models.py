from app import db
from sqlalchemy import Numeric

from sqlalchemy import func, event, DDL

class eat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(500), nullable=True)
    comment = db.Column(db.String(150), nullable=True)
    time_delta = db.Column(db.Interval, nullable=True)  # Allow null values
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())
    weight = db.Column(db.Float(precision=4), nullable=True)

