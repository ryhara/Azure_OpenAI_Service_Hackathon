from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
from openai import AzureOpenAI
from pypdf import PdfReader
import markdown

judge_fairness_chat_bp = Blueprint('judge_fairness_chat', __name__)


@judge_fairness_chat_bp.route('/judge_fairness_chat')
def chat():
    return render_template('judge_fairness_chat.index.html')

@judge_fairness_chat_bp.route('/judge_fairness_chat/send_message/gpt-4', methods=['POST'])
def send_message_4():
    user_message = request.form.get('message')
    pdf_file = request.files.get('pdf')
    text = ''
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        reader = PdfReader(pdf_file)
        text = reader.pages[0].extract_text()
    else:
        text = user_message

    client = AzureOpenAI(
        api_key = current_app.config['OPENAI_API_KEY'],
        azure_endpoint = current_app.config['OPENAI_ENDPOINT'],
        api_version = "2023-05-15"
    )
    ###promptの設定
    prompt_path = 'flask_app/data/fair_prompt.txt'
    prompt = ""
    with open(prompt_path) as f:
        prompt = str(f.read()) ##一応キャスト
    prompt = prompt.format(input=text)
    completion = client.chat.completions.create(
    model='GPT4',
    messages=[
        {"role": "user", "content": prompt}
             ])
    response = completion.choices[0].message.content
    return response

@judge_fairness_chat_bp.route('/judge_fairness_chat/send_message/gpt-3-5', methods=['POST'])
def send_message_3_5():
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

    client = AzureOpenAI(
        api_key = current_app.config['OPENAI_API_KEY'],
        azure_endpoint = current_app.config['OPENAI_ENDPOINT'],
        api_version = "2023-05-15"
    )
    ###promptの設定
    prompt_path = 'flask_app/data/fair_prompt.txt'
    prompt = ""
    with open(prompt_path) as f:
        prompt = str(f.read()) ##一応キャスト
    prompt = prompt.format(input=text)
    completion = client.chat.completions.create(
    model='GPT35TURBO',
    messages=[
        {"role": "user", "content": prompt}
             ])
    response = completion.choices[0].message.content
    md = markdown.Markdown()
    return md.convert(response)
    return response
