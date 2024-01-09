from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os

chat_bp = Blueprint('chat', __name__)
API_KEY = os.getenv('API_KEY')

@chat_bp.route('/chat')
def chat():
    return render_template('chat_index.html')

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    API_KEY = current_app.config['API_KEY']
    ENDPOINT = current_app.config['ENDPOINT']
    # TODO : APIを叩いて応答を生成する
    return "Hello"
