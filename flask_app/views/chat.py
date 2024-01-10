from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import openai
from PyPDF2 import PdfReader
chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat')
def chat():
    return render_template('chat_index.html')

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    # user_message かpdf_fileどちらかは必須で入る。
    # pdf_fileは最終的にtextに変換される。
    # user_messageがない場合はpdf_fileが入っているので、デフォルトのメッセージを入れる。
    user_message = request.form.get('message')
    if user_message is None:
        # TODO : デフォルトのメッセージはいいものを考える（英語）。
        user_message = 'この文章について、解説してください'
    pdf_file = request.files.get('pdf')
    text = ''
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        reader = PdfReader(pdf_file)
        text = reader.pages[0].extract_text()
    AZURE_OPENAI_API_KEY = current_app.config['AZURE_OPENAI_API_KEY']
    AZURE_OPENAI_ENDPOINT = current_app.config['AZURE_OPENAI_ENDPOINT']
    os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
    os.environ["OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    #openai.api_type = "azure"
    #openai.api_base = os.environ.get('OPENAI_ENDPOINT')
    #openai.api_version = "2023-05-15"

    completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": user_message}
             ])
    responce = completion.choices[0].message['content']
    return "おはよう！"
