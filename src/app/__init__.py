from flask import Flask
from src.app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    return app
