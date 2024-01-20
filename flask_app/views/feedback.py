from flask import Blueprint, render_template, redirect, url_for, request

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback')
def feedback():
    return render_template('feedback.index.html')

@feedback_bp.route('/feedback/send_message/gpt-3-5', methods=['POST'])
def send_message_3_5():
    user_message = request.form.get('message')
    return "Feedback GPT3.5 function is not implemented yet."

@feedback_bp.route('/feedback/send_message/gpt-4', methods=['POST'])
def send_message_4():
    user_message = request.form.get('message')
    return "Feedback GPT 4 function is not implemented yet."
