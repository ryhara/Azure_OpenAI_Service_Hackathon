from flask import Flask, render_template
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__, instance_relative_config=True,
                static_folder='./static', template_folder='./templates')
    app.config.from_pyfile('config.py')
    return app
