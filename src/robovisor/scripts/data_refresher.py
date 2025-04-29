import sys
import os

print("cwd",str(os.getcwd()))
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from robovisor import create_app
from robovisor.datacollectors.collector import refresh_db

if __name__ == "__main__":
    # This is just a wrapper to run the refresh script, but we have to create an app anyway
    app = create_app()

    with app.app_context():
        refresh_db()