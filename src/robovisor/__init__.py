from flask import Flask, request, g
from time import time
from robovisor.models import db
from robovisor.config import DevelopmentConfig, TestingConfig, ProductionConfig
import os
import sys
import logging
from sqlalchemy import inspect

def create_app():
    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'templates'))
    app = Flask(__name__, template_folder=template_path)

    # Configure app by environment
    # Mostly thais sets the db 
    env = os.getenv("FLASK_ENV", "development")
    print("Got env", env)
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "test": TestingConfig,
    }
    app.config.from_object(config_map[env])
    if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1)

    db.init_app(app)

    # Configure the logger, preferring verbose info level logging
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Set automatic API timing logs
    @app.before_request
    def start_timer():
        g.start_time = time()

    @app.after_request
    def log_request(response):
        duration = time() - g.start_time
        app.logger.info(f"{request.method} {request.path} {response.status_code} took {duration:.3f}s")
        return response

    # Detect if db needs backfilling or updating
    with app.app_context():
        if env == "development":
            inspector = inspect(db.session.bind)
            tables = inspector.get_table_names()
            if "price" not in tables or "ticker" not in tables:
                print("Dev environment detected, creating missing tables...")
                db.create_all()

                from robovisor.datacollectors.collector import backfill_db
                backfill_db()

        from robovisor.views import register_routes
        register_routes(app)

    return app
