import sys
import os

# Module-ization is not perfect, add src to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from robovisor import create_app

app = create_app()
