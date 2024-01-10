from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import openai
from pypdf import PdfReader

judge_fairness_chat_bp = Blueprint('judge_fairness_chat', __name__)


@judge_fairness_chat_bp.route('/judge_fairness_chat')
def chat():
    return render_template('judge_fairness_chat.index.html')

@judge_fairness_chat_bp.route('/judge_fairness_chat/send_message', methods=['POST'])
def send_message():
    # user_message かpdf_fileどちらかは必須で入る。
    # pdfがない場合user_messageをtextとして使う
    # TODO : pdfとuser_messageの両方がある場合はuser_messageをoptionの指示として使う
    user_message = request.form.get('message')
    pdf_file = request.files.get('pdf')
    text = ''
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        reader = PdfReader(pdf_file)
        text = reader.pages[0].extract_text()
    else:
        text = user_message
    AZURE_OPENAI_API_KEY = current_app.config['AZURE_OPENAI_API_KEY']
    AZURE_OPENAI_ENDPOINT = current_app.config['AZURE_OPENAI_ENDPOINT']
    os.environ["OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
    os.environ["OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    #openai.api_type = "azure"
    #openai.api_base = os.environ.get('OPENAI_ENDPOINT')
    #openai.api_version = "2023-05-15"
    ###promptの設定
    prompt_path = 'flask_app/data/fair_prompt.txt'
    prompt = ""
    with open(prompt_path) as f:
        prompt = str(f.read()) ##一応キャスト
    prompt = prompt.format(input=text)
    completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": prompt}
             ])
    responce = completion.choices[0].message['content']
    return responce
