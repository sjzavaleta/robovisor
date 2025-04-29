import pytest
from unittest.mock import Mock
from robovisor.data_analyzers import recommender
from robovisor.data_models.Recommendation import MomentumRecommendation, SteadinessRecommendation, SpikeRecommendation, DipRecommendation, UnavailableRecommendation

### Momentum Recommendation


@pytest.fixture
def mock_fetcher():
    return Mock()

def test_momentum_buy(mock_fetcher):
    mock_fetcher.get_latest_value.return_value = 110
    mock_fetcher.get_n_day_average.return_value = 100
    expected = MomentumRecommendation("Buy", 100, 110,)
    assert recommender.momentum_recommendation("AAPL", mock_fetcher) == expected

def test_momentum_dont_buy(mock_fetcher):
    mock_fetcher.get_latest_value.return_value = 104
    mock_fetcher.get_n_day_average.return_value = 100
    expected = MomentumRecommendation("Don't Buy", 100, 104)
    assert recommender.momentum_recommendation("AAPL", mock_fetcher) == expected

def test_momentum_unavailable(mock_fetcher):
    mock_fetcher.get_latest_value.return_value = None
    mock_fetcher.get_n_day_average.return_value = 100
    expected = UnavailableRecommendation("No Recommendation")
    assert recommender.momentum_recommendation("AAPL", mock_fetcher) == expected


### Steadiness Recommendation

def test_steady_buy(mock_fetcher):
    mock_fetcher.get_n_day_volatility.return_value = 0.015
    mock_fetcher.get_n_day_average.return_value = 1200000
    expected = SteadinessRecommendation("Buy", 0.015, 1200000)
    assert recommender.steady_recommendation("AAPL", mock_fetcher) == expected

def test_steady_dont_buy(mock_fetcher):
    mock_fetcher.get_n_day_volatility.return_value = 0.03
    mock_fetcher.get_n_day_average.return_value = 800000
    expected = SteadinessRecommendation("Don't Buy", 0.03, 800000)
    assert recommender.steady_recommendation("AAPL", mock_fetcher) == expected

def test_steady_unavailable(mock_fetcher):
    mock_fetcher.get_n_day_volatility.return_value = None
    mock_fetcher.get_n_day_average.return_value = 1000000
    expected = UnavailableRecommendation("No Recommendation")
    assert recommender.steady_recommendation("AAPL", mock_fetcher) == expected

### Spike Recommendation

def test_spike_buy(mock_fetcher):
    mock_fetcher.get_n_day_average.return_value = 500000
    mock_fetcher.get_latest_value.side_effect = [1200000, 110]
    mock_fetcher.get_at_least_n_days_ago_value.return_value = 100
    expected = SpikeRecommendation("Buy", 1200000, 500000, 110, 100)
    assert recommender.spike_recommendation("AAPL", mock_fetcher) == expected

def test_spike_dont_buy(mock_fetcher):
    mock_fetcher.get_n_day_average.return_value = 600000
    mock_fetcher.get_latest_value.side_effect = [1000000, 95]
    mock_fetcher.get_at_least_n_days_ago_value.return_value = 100
    expected = SpikeRecommendation("Don't Buy", 1000000, 600000, 95, 100)
    assert recommender.spike_recommendation("AAPL", mock_fetcher) == expected

def test_spike_unavailable(mock_fetcher):
    mock_fetcher.get_n_day_average.return_value = None
    mock_fetcher.get_latest_value.return_value = 100
    mock_fetcher.get_at_least_n_days_ago_value.return_value = 100
    expected = UnavailableRecommendation("No Recommendation")
    assert recommender.spike_recommendation("AAPL", mock_fetcher) == expected

### Dip Recommendation

def test_dip_buy(mock_fetcher):
    mock_fetcher.get_at_least_n_days_ago_value.side_effect = [111, 90]
    mock_fetcher.get_latest_value.return_value = 100
    expected = DipRecommendation("Buy", 111, 90, 100)
    assert recommender.dip_recommendation("AAPL", mock_fetcher) == expected

def test_dip_dont_buy(mock_fetcher):
    mock_fetcher.get_at_least_n_days_ago_value.side_effect = [115, 112]
    mock_fetcher.get_latest_value.return_value = 110
    expected = DipRecommendation("Don't Buy", 115, 112, 110)
    assert recommender.dip_recommendation("AAPL", mock_fetcher) == expected

def test_dip_unavailable(mock_fetcher):
    mock_fetcher.get_at_least_n_days_ago_value.side_effect = [None, 100]
    mock_fetcher.get_latest_value.return_value = 110
    expected = UnavailableRecommendation("No Recommendation")
    assert recommender.dip_recommendation("AAPL", mock_fetcher) == expected
