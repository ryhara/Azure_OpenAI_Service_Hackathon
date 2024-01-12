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
    # user_messageかpdf_fileどちらかは必須で入る。
    # pdfがない場合user_messageをtextとして使う, ２つ入力がある場合はpdfを優先する
    user_message = request.form.get('message')
    pdf_file = request.files.get('pdf')
    text = ''
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        reader = PdfReader(pdf_file)
        text = reader.pages[0].extract_text()
    else:
        text = user_message

    openai.api_key = current_app.config['OPENAI_API_KEY']
    #openai.api_type = "azure"
    #openai.api_base = current_app.config['OPENAI_ENDPOINT']
    #openai.api_version = "2023-05-15"
    ###promptの設定
    ## TODO : 英語のpromptのほうが提出時には良いかも
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
