"""
WSGI entry point for Vercel deployment.
This file imports the Flask app from the backend module and exposes it
as the WSGI application that Vercel will run.
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the Flask app from backend.server
from server import app

# Expose the app for WSGI servers
application = app

if __name__ == "__main__":
    app.run()
