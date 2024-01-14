from flask import Blueprint, render_template, redirect, url_for, request

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback')
def feedback():
    return render_template('feedback.index.html')

@feedback_bp.route('/feedback/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    return "Hello World"
