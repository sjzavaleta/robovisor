import os
import sys
from sqlalchemy import inspect
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from robovisor import create_app, db
from robovisor.datacollectors.collector import backfill_db

# This script is run by the "release" phase of heroku before starting the app. It detects an empty db and backfills it if they aren't available

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    if "price" not in tables or "ticker" not in tables:
        try:
            backfill_db()
        except Exception as e:
            logging.error(f"Backfill failed: {e}")
