from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import sqlite3
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import openai
image_chat_bp = Blueprint('image_chat', __name__)

###データベースの構造の定義
Base = declarative_base()
class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    label = Column(String)

###ここに定義していいのかわからないけどlabelを取得する関数
#TODO しゅうたんの担当関数。
def get_label():
    return "cat"
###メッセージを
def get_word_list(user_message):
    text = user_message
    openai.api_key = current_app.config['OPENAI_API_KEY']
    prompt_path = 'flask_app/data/word_list_prompt.txt'
    prompt = ""

    with open(prompt_path) as f:
        prompt = str(f.read())
    
    #日本語
    #with open(prompt_path, 'r', encoding='utf-8') as f:
        #prompt = str(f.read())

    prompt = prompt.format(input=text)
    completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": prompt}
             ])
    responce = completion.choices[0].message['content']
    word_list = responce.split(",")
    return word_list

@image_chat_bp.route('/image_chat')
def chat():
    return render_template('image_chat.index.html')

@image_chat_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image-input' not in request.files:
        return redirect(request.url)

    file = request.files['image-input']

    if file.filename == '':
        return redirect(request.url)
    
    if file:
        ###sqliteデータベースにファイル名と対応するラベルを保存する。
        db_path = current_app.config['SQLALCHEMY_DATABASE_URI']
        engine = create_engine(db_path)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        new_image = Image(file_name=file.filename,label=get_label())
        session.add(new_image)
        session.commit()
        return redirect(url_for('image_chat.chat'))

    return redirect(url_for('image_chat.chat'))
@image_chat_bp.route('/image_chat/send_message', methods=['POST'])
def send_message():
    ###ひとまずデータベースから与えられた単語に一致するデータを拾ってくる。
    ###user_messageは本来単語じゃないのでGPTを使って単語のリストに処理する必要がある。
    user_message = request.form.get('message')
    word_list = get_word_list(user_message)
    db_path = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    #取り出してみる
    result = ""
    for word in word_list:
        query = session.query(Image).filter(Image.label.like(f"%{word}%"))
        images = query.all()
        #とりあえず三件だけ取り出してみる[:num]を調整することで数変えられる。
        for image in images[:3]:
            result+=(str(image.file_name) + '\n')
    return result