from flask import Flask
from .config import Setup

app = Flask(__name__)
Setup.apply_environs(app)
Setup.init_extensions(app)
Setup.create_admin_user_if_absent(app)
