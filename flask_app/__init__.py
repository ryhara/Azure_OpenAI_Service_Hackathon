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
    from flask_app.views.manual import manual_bp
    from flask_app.views.chat import chat_bp
    from flask_app.views.setting import setting_bp
    app.register_blueprint(manual_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(setting_bp)
    return app
