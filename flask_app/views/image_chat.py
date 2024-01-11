from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os

image_chat_bp = Blueprint('image_chat', __name__)

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
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('image_chat.chat'))

    return redirect(url_for('image_chat.chat'))

@image_chat_bp.route('/image_chat/send_message', methods=['POST'])
def send_message():
    return 'Hello, World!'