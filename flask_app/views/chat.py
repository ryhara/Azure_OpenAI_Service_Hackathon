from flask import Blueprint, render_template, redirect, url_for, request, current_app
from openai import AzureOpenAI

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
    # client = AzureOpenAI(
    #     api_version = "2023-12-01-preview",
    #     api_key = AZURE_OPENAI_API_KEY,
    #     azure_endpoint = AZURE_OPENAI_ENDPOINT
    # )

    # completion = client.chat.completions.create(
    #     model="GPT35TURBO16K",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": user_message,
    #         },
    #     ],
    # )
    # response_message = completion.choices[0].message.content
    response_message = "Hello World!"
    return response_message
