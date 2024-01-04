from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # app
    app = Flask(__name__, instance_relative_config=True,
                static_folder='./static', template_folder='./templates')
    app.config.from_pyfile('config.py')

    # Database
    db.init_app(app)

    # Blueprint
    from flask_app.views.sample import sample_bp
    app.register_blueprint(sample_bp)
    return app
