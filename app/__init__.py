import logging
import os
from flask import Flask
from .config import get_config

app = Flask(__name__)

app.config['SECRET_KEY'] = get_config("SECRET_KEY")

from .api import api

app.register_blueprint(api)

app.logger.info('App initialized')