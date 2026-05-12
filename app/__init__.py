from flask import Flask
from .config.setup import setup_environs, setup_extensions


app = Flask(__name__)
setup_environs(app)
setup_extensions(app)
