from flask import Blueprint, render_template, redirect, url_for, request, current_app
import openai
from openai import OpenAI
chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat')
def chat():
    return render_template('chat_index.html')

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    # TODO : APIを叩いて応答を生成する
    AZURE_OPENAI_API_KEY = current_app.config['AZURE_OPENAI_API_KEY']
    AZURE_OPENAI_ENDPOINT = current_app.config['AZURE_OPENAI_ENDPOINT']
    openai.api_key = AZURE_OPENAI_API_KEY
    openai.api_type = "azure"
    openai.api_base = AZURE_OPENAI_ENDPOINT
    openai.api_version = "2023-05-15"

    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": user_message}
             ])
    responce = completion.choices[0].message
    return responce

