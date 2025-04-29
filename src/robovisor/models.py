from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# This is more data than I need, but its everything available in the API and I might need it later
class Price(db.Model):
    ticker = db.Column(db.String(8), primary_key=False)
    date = db.Column(db.Date, primary_key=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    open = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    # Compound key on ticker and date
    __table_args__ = (db.PrimaryKeyConstraint('date', 'ticker'),)

# It seems useful to me to have an easily accessible list of tickers
class Ticker(db.Model):
    ticker = db.Column(db.String(8), primary_key=True)