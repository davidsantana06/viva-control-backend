from flask import Flask
from .config import Setup

app = Flask(__name__)
Setup.apply_environs(app)
Setup.init_extensions(app)
