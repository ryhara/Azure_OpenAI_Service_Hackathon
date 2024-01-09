from flask import Blueprint, render_template, redirect, url_for, request, current_app

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    return render_template('chat_index.html')

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    AZURE_OPENAI_API_KEY = current_app.config['AZURE_OPENAI_API_KEY']
    AZURE_OPENAI_ENDPOINT = current_app.config['AZURE_OPENAI_ENDPOINT']
    # TODO : APIを叩いて応答を生成する
    return "Hello"
