from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import sqlite3
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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
    db_path = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Image).filter(Image.label.like(f"%{user_message}%"))
    #取り出してみる
    images = query.all()
    result = ""
    for image in images:
        result+=(str(image.file_name) + '\n')
    return result