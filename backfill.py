import os
import sys
from sqlalchemy import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from robovisor import create_app, db
from robovisor.datacollectors.collector import backfill_db

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    if "price" not in tables or "ticker" not in tables:
        try:
            backfill_db()
        except Exception as e:
            print(f"Backfill failed: {e}")
