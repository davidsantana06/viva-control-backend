from flask import Flask
from .config.setup import apply_environs, init_extensions, init_container


app = Flask(__name__)
apply_environs(app)
init_extensions(app)
init_container(app)
