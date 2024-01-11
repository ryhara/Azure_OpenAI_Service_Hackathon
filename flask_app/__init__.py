from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_app.views.manual import manual_bp
from flask_app.views.judge_fairness_chat import judge_fairness_chat_bp
from flask_app.views.image_chat import image_chat_bp

db = SQLAlchemy()

def create_app():
    # app
    app = Flask(__name__, instance_relative_config=True,
                static_folder='./static', template_folder='./templates')
    app.config.from_pyfile('config.py')
<<<<<<< HEAD
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/pdfs.db'
=======
    app.config['UPLOAD_FOLDER'] = '/app/flask_app/uploads/'
>>>>>>> 84584f3fa114d2379c84253180cd0a52ec1a84bf

    # Database
    db.init_app(app)

    # Blueprint
    app.register_blueprint(manual_bp)
    app.register_blueprint(judge_fairness_chat_bp)
    app.register_blueprint(image_chat_bp)
    return app
