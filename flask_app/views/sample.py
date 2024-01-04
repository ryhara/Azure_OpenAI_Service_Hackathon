from flask import Blueprint, render_template

sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/sample')
def sample():
	return render_template('index.html')