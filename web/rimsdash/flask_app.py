"""Initialize Flask app."""
from flask import Flask

# Import Dash application
from rimsdash.dashboard.user_app import create_dashboard


"""
Base app as vanilla flask
with dash app nested inside
"""

"""Construct core Flask application with embedded Dash app."""
app = Flask(__name__, instance_relative_config=False)

with app.app_context():
    # Import parts of our core Flask app
    #import rimsdash.routes

    app = create_dashboard(app)

def entry_dev():
    app.run()

if __name__ == "__main__":
    app.run()