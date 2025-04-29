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
        """fetcher = PriceFetcher()
        
        if request.method == "POST":
            ticker = request.form.get("ticker", "").upper().strip()
            momentum_rec = recommender.momentum_recommendation(ticker, fetcher)
            spike_rec = recommender.spike_recommendation(ticker, fetcher)
            steady_rec = recommender.steady_recommendation(ticker, fetcher)
            dip_rec = recommender.dip_recommendation(ticker, fetcher)
            results = {
                "Has Momentum": momentum_rec.format_reason(),
                "Spiking": spike_rec.format_reason(),
                "Holding Stead": steady_rec.format_reason(),
                "Buy the Dip": dip_rec.format_reason(),
            }
            return render_template("researcher.html", results=results, ticker=ticker)
        return render_template("researcher.html", results=None)
    

    @app.route("/browser")
    def browser():
        top_momentum = [('AAPL', 100)]#get_top_n_by_heuristic(momentum_recommendation, n=10)
        top_spike = [('META', 99)]#get_top_n_by_heuristic(spike_recommendation, n=10)
        return render_template("browser.html", momentum=top_momentum, spike=top_spike)"""
    
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
    