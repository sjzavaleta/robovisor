from robovisor import create_app
from robovisor.datacollectors.collector import refresh_db

app = create_app()

with app.app_context():
    refresh_db()