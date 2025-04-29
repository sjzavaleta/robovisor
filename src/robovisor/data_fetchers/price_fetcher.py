from robovisor.models import Price, db
from datetime import date, timedelta
from sqlalchemy import func
import numpy as np
import logging

class PriceFetcher():
    def __init__(self, session=None):
        if session:
            self.session = session
        else:
            self.session = db.session

    def get_latest_value(self, ticker, column):
        logging.info(f"Getting latest {column} value of {ticker}")
        return (
                db.session.query(getattr(Price, column))
                .filter_by(ticker=ticker)
                .order_by(Price.date.desc())
                .limit(1)
                .scalar()
            )

    def get_n_days_ago_value(self, ticker, n, column):
        logging.info(f"Getting {column} value of {ticker} {n} days ago")
        n_days = timedelta(days=n)
        n_days_ago = date.today() - n_days
        return (
                db.session.query(getattr(Price, column))
                .filter_by(ticker=ticker)
                .filter(Price.date >= n_days_ago)
                .order_by(Price.date)
                .limit(1)
                .scalar()
            )


    def get_n_day_average(self, ticker, n, column):
        logging.info(f"Getting average {column} value of {ticker} for the last {n} days")
        n_days = timedelta(days=n)
        n_days_ago = date.today() - n_days

        n_day_avg = (
            db.session.query(func.avg(getattr(Price, column)))
            .filter(Price.ticker == ticker)
            .filter(Price.date > n_days_ago)
            .scalar()
        )
        return n_day_avg

    def get_n_day_volatility(self, ticker, n):
        logging.info(f"Getting the price volatility of {ticker} for the last {n} days")
        n_days = timedelta(days=n+1) # Todays volatility is based on yesterdays price
        n_days_ago = date.today() - n_days

        rows = (
            db.session.query(Price.close)
            .filter(Price.ticker == ticker)
            .filter(Price.date >= n_days_ago)
            .order_by(Price.date)
            .all()
        )

        if len(rows) < 2:
            return None

        prices = [row.close for row in rows]
        returns = np.diff(np.log(prices)) 
        volatility = np.std(returns)

        return volatility