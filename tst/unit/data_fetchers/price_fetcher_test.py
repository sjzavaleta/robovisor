import pytest
from robovisor import create_app, db
from robovisor.models import Price
from datetime import date, timedelta
from robovisor.data_fetchers.price_fetcher import PriceFetcher

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        db.session.remove()

@pytest.fixture
def session_with_prices(app):

    today = date.today()
    prices = [
        Price(ticker="AAPL", date=today - timedelta(days=2), open=100, close=100, high=100, low=100, volume=1000),
        Price(ticker="AAPL", date=today - timedelta(days=1), open=105, close=105, high=105, low=105, volume=2000),
        Price(ticker="AAPL", date=today, open=110, close=110, high=110, low=110, volume=1500)
    ]
    db.session.add_all(prices)

    yield db.session

    db.session.rollback()

# Happy Path

def test_latest_value(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_latest_value("AAPL", "close") == 110

def test_n_days_ago_value(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_n_days_ago_value("AAPL", 2, "close") == 100

def test_n_day_average(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    avg = price_fetcher.get_n_day_average("AAPL", 2, "close")
    assert round(avg, 2) == 107.5

def test_n_day_volatility(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    result = price_fetcher.get_n_day_volatility("AAPL", 3)
    assert round(result,4) == .0011

# Wrong ticker no data

def test_latest_value_none(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_latest_value("MSFT", "close") is None

def test_n_days_ago_value_none(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_n_days_ago_value("MSFT", 2, "close") is None

def test_n_day_average_none(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_n_day_average("MSFT", 2, "close") is None

def test_n_day_volatility_none(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_n_day_volatility("MSFT", 2) is None

# Other cases of no data

def test_insufficent_days_for_volatility(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    result = price_fetcher.get_n_day_volatility("AAPL", -1)
    assert result is None


def test_data_for_date_not_exist(session_with_prices):
    price_fetcher = PriceFetcher(session_with_prices)
    assert price_fetcher.get_n_days_ago_value("AAPL", 20, "close") is None
