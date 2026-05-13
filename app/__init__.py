from flask import Flask
from .config.setup import apply_environs, init_extensions


app = Flask(__name__)
apply_environs(app)
init_extensions(app)
