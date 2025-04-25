from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Price(db.Model):
    ticker = db.Column(db.String(8), primary_key=False)
    date = db.Column(db.Date, primary_key=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    open = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint('date', 'ticker'),)

class Ticker(db.Model):
    ticker = db.Column(db.String(8), primary_key=True)