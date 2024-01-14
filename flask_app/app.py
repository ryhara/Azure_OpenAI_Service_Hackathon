from flask import render_template
from flask_app import create_app
from flask_app.models import db, Image


app = create_app()
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
