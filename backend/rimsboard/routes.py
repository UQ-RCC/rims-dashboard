"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app

if False:
    #homepage currently routes straight to dash app

    # Defining the home page of our site
    @app.route("/")  # this sets the route to this page
    def home():
        return "Hello! this is the main page <h1>HELLO</h1>"  # some basic inline html

    @app.route('/')
    def home():
        """Landing page."""
        return render_template(
            'index.jinja2',
            title='Plotly Dash Flask Tutorial',
            description='Embed Plotly Dash into your Flask applications.',
            template='home-template',
            body="This is a homepage served with Flask."
        )

