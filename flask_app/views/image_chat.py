from flask import Blueprint, render_template, redirect, url_for, request

image_chat_bp = Blueprint('image_chat', __name__)

# TODO : 設定画面の実装
@image_chat_bp.route('/image_chat')
def chat():
    return render_template('image_chat.index.html')

@image_chat_bp.route('/register_image', methods=['POST'])
def register_image():
    # TODO : 画像の登録処理
    return "aaa"

