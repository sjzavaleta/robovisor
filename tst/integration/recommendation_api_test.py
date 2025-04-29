import pytest
from robovisor import create_app, db
from robovisor.models import Price
from datetime import date, timedelta

@pytest.fixture
def test_client():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        today = date.today()
        prices = []
        for i in range(31):
            new_date = today - timedelta(days=i)
            # Prepare data for momentum and spike
            meta_close = 100 + i
            meta_volume = 1000
            if i == 0:
                meta_close = 1000
                meta_volume = 1000000
            prices.append(Price(ticker="META", date=new_date, high=500, low=50, open=meta_close - 1, close=meta_close, volume=meta_volume))

            # Prepare data for dip
            aapl_close = 100 - i
            aapl_volume = 10000000
            if i == 10:
                aapl_close = 120
            prices.append(Price(ticker="AAPL", date=new_date, high=100, low=aapl_close, open=aapl_close - 1, close=aapl_close, volume=aapl_volume))

            # Prepare data for steady
            prices.append(Price(ticker="GOOG", date=new_date, high=100, low=100, open=100, close=100, volume=10000000))

            
            
        db.session.add_all(prices)
        db.session.commit()
    yield app.test_client()

# Test Happy Path. The data was specifically generated to yield buy recommendaitons

def test_momentum_recommendation(test_client):
    response = test_client.get("/api/recommendation/momentum/META")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Buy"

def test_spike_recommendation(test_client):
    response = test_client.get("/api/recommendation/spike/META")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Buy"

def test_steady_recommendation(test_client):
    response = test_client.get("/api/recommendation/steady/GOOG")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Buy"

def test_dip_recommendation(test_client):
    response = test_client.get("/api/recommendation/dip/AAPL")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Buy"

# Test don't buy recommendations. Swap around which ticker we ask recommendations for 

def test_momentum_recommendation_dont(test_client):
    response = test_client.get("/api/recommendation/momentum/GOOG")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Don't Buy"

def test_spike_recommendation_dont(test_client):
    response = test_client.get("/api/recommendation/spike/AAPL")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Don't Buy"

def test_steady_recommendation_dont(test_client):
    response = test_client.get("/api/recommendation/steady/AAPL")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Don't Buy"

def test_dip_recommendation_dont(test_client):
    response = test_client.get("/api/recommendation/dip/GOOG")
    assert response.status_code == 200
    data = response.get_json()
    assert data["action"] == "Don't Buy"

