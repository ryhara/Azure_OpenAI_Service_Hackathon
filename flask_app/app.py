from flask import render_template
from flask_app import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('home.index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
