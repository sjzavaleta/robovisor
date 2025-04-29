from flask import render_template, request, jsonify
from robovisor.models import db
from robovisor.data_analyzers import recommender
from robovisor.data_fetchers.price_fetcher import PriceFetcher

def register_routes(app):
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/researcher", methods=["GET", "POST"])
    def researcher():
        return render_template("researcher.html")
    
### Data APIs

    @app.route("/api/recommendation/momentum/<ticker>", methods=["GET"])
    def momentum_recommendation(ticker):
        fetcher = PriceFetcher()
        rec = recommender.momentum_recommendation(ticker, fetcher)
        return jsonify(rec.to_dict())

    @app.route("/api/recommendation/spike/<ticker>", methods=["GET"])
    def spike_recommendation(ticker):
        fetcher = PriceFetcher()
        rec = recommender.spike_recommendation(ticker, fetcher)
        return jsonify(rec.to_dict())
    

    @app.route("/api/recommendation/steady/<ticker>", methods=["GET"])
    def steady_recommendation(ticker):
        fetcher = PriceFetcher()
        rec = recommender.steady_recommendation(ticker, fetcher)
        return jsonify(rec.to_dict())
    

    @app.route("/api/recommendation/dip/<ticker>", methods=["GET"])
    def dip_recommendation(ticker):
        fetcher = PriceFetcher()
        rec = recommender.dip_recommendation(ticker, fetcher)
        return jsonify(rec.to_dict())
    