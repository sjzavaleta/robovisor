import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from robovisor import create_app, db
from robovisor.datacollectors.collector import backfill_db

app = create_app()

with app.app_context():
    try:
        backfill_db()
    except Exception as e:
        print(f"Backfill failed: {e}")
