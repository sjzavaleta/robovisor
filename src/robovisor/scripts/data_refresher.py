import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from robovisor import create_app
from robovisor.datacollectors.collector import refresh_db

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        refresh_db()