from robovisor.data_models.Recommendation import UnavailableRecommendation, SpikeRecommendation, MomentumRecommendation, DipRecommendation, SteadinessRecommendation

def momentum_recommendation(ticker, price_fetcher):
    latest_price = price_fetcher.get_latest_value(ticker, "close")
    price_30d = price_fetcher.get_n_day_average(ticker, 30, "close")
    if latest_price == None or price_30d == None:
        return UnavailableRecommendation("No Recommendation")
    if latest_price > 1.05 * price_30d:
        return MomentumRecommendation("Buy",price_30d, latest_price) #f"Buy. The latest price, ${latest_price}, is significantly ahead of its 30 days average, ${price_30d:.2f}"
    else:
        return MomentumRecommendation("Don't Buy", price_30d, latest_price) #f"Do not buy. The latest price, ${latest_price:.2f}, is not significantly ahead of its 30 days average, ${price_30d:.2f}"

def steady_recommendation(ticker, price_fetcher) :
    volatility_30d = price_fetcher.get_n_day_volatility(ticker, 30)
    volume_30d = price_fetcher.get_n_day_average(ticker, 30, "volume")
    print("volatility_30de", volatility_30d)
    print("volume_30d", volume_30d)
    if volatility_30d == None or volume_30d == None:
        return UnavailableRecommendation("No Recommendation")
    if volatility_30d < .02 and volume_30d > 1000000:
        return SteadinessRecommendation("Buy", volatility_30d, volume_30d)
    else:
        return SteadinessRecommendation("Don't Buy", volatility_30d, volume_30d)


def spike_recommendation(ticker, price_fetcher):
    volume_30d = price_fetcher.get_n_day_average(ticker, 30, "volume")
    latest_volume = price_fetcher.get_latest_value(ticker, "volume")
    latest_price = price_fetcher.get_latest_value(ticker, "close")
    yesterdays_price = price_fetcher.get_n_days_ago_value(ticker, 2, "close")
    if latest_volume == None or volume_30d == None or latest_price == None or yesterdays_price == None:
        return UnavailableRecommendation("No Recommendation")
    if latest_volume > 2 * volume_30d and latest_price > yesterdays_price:
        return SpikeRecommendation("Buy", latest_volume, volume_30d, latest_price, yesterdays_price) #f"Buy. The latest volume, {latest_volume}, is much larger than its 30 day average volume, {volume_30d:.2f}, while its latest price, ${latest_price}, is above yesterdays price, ${yesterdays_price}"
    else:
        return SpikeRecommendation("Don't Buy", latest_volume, volume_30d, latest_price, yesterdays_price) #f"Do not buy. The latest volume, {latest_volume}, is not much larger than its 30 day average volume, {volume_30d:.2f}, or its latest price, ${latest_price}, is below yesterdays price, ${yesterdays_price}"


def dip_recommendation(ticker,price_fetcher):
    price_10d_ago = price_fetcher.get_n_days_ago_value(ticker, 10, "low")
    price_5d_ago = price_fetcher.get_n_days_ago_value(ticker, 5, "close")
    latest_price = price_fetcher.get_latest_value(ticker, "close")
    if price_10d_ago == None or price_5d_ago == None or latest_price == None:
        return UnavailableRecommendation("No Recommendation")
    if (price_10d_ago / latest_price) > 1.1 and latest_price > price_5d_ago:
        return DipRecommendation("Buy", price_10d_ago, price_5d_ago, latest_price) #f"Buy. It's price 10 days ago, ${price_10d_ago:.2f}, is 10% greater than its price today ${latest_price}, and its price 5 days ago ${price_5d_ago:.2f}, is lower than the latest price"
    else:
        return DipRecommendation("Don't Buy", price_10d_ago, price_5d_ago, latest_price) #f"Do not buy. It's price 10 days ago, ${price_10d_ago:.2f}, is not 10% greater than its price today ${latest_price}, ot its price 5 days ago ${price_5d_ago:.2f}, is not lower than the latest price"

