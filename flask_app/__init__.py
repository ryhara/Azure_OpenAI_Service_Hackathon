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
    app.config['UPLOAD_FOLDER'] = '/app/flask_app/uploads/'
    

=======
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/pdfs.db'
    app.config['UPLOAD_FOLDER'] = '/app/flask_app/uploads/'
>>>>>>> d2f0e814470fd6853af5101418ae402a6da35d90

    # Database
    db.init_app(app)

    # Blueprint
    app.register_blueprint(manual_bp)
    app.register_blueprint(judge_fairness_chat_bp)
    app.register_blueprint(image_chat_bp)

