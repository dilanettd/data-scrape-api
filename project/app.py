import logging
from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from apifairy import APIFairy
from flask_marshmallow import Marshmallow

from config import Config


cors = CORS()
apifairy = APIFairy()
app = Flask(__name__)
ma = Marshmallow()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# ----------------------------
# Application Factory Function
# ----------------------------


def create_app(config_class=Config):
    app.config.from_object(config_class)

    register_blueprints(app)
    initialize_extensions(app)

    @app.route("/")
    def index():  # pragma: no cover
        return redirect(url_for("apifairy.docs"))

    @app.after_request
    def after_request(response):
        # Werkzeu sometimes does not flush the request body so we do it here
        request.get_data()
        return response

    return app


# ----------------
# Helper Functions
# ----------------


def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    if app.config["USE_CORS"]:  # pragma: no branch
        cors.init_app(app)

    apifairy.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    # Import the blueprints
    from .errors import errors
    from .api import linkedin

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(errors)
    app.register_blueprint(linkedin, url_prefix="/api/linkedin")
