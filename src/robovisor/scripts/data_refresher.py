import sys
import os

print("cwd",str(os.getcwd()))
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from robovisor import create_app
from robovisor.datacollectors.collector import refresh_db

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        refresh_db()