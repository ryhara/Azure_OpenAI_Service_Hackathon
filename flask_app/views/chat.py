from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import openai
chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat')
def chat():
    return render_template('chat_index.html')

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form.get('message')
    AZURE_OPENAI_API_KEY = current_app.config['AZURE_OPENAI_API_KEY']
    AZURE_OPENAI_ENDPOINT = current_app.config['AZURE_OPENAI_ENDPOINT']
    os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
    os.environ["OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
    
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    openai.api_type = "azure"
    openai.api_base = os.environ.get('OPENAI_ENDPOINT')
    openai.api_version = "2023-05-15"

    completion = openai.ChatCompletion.create(
    deployment_id="GPT35TURBO",
    messages=[
        {"role": "user", "content": user_message}
             ])
    responce = completion.choices[0].message['content']
    return responce
