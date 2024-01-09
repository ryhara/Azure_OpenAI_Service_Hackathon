from flask import Blueprint, render_template, redirect, url_for, request

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    return render_template('chat_index.html')

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    # TODO : APIを叩いて応答を生成する
    return "Hello"
