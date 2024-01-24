from flask import Blueprint, render_template, redirect, url_for, request, current_app, jsonify, current_app
import io
import os
import openai
import requests
import base64
from flask_app.models import Image,sampleDB
from PIL import Image as Im
from io import BytesIO
from flask_app.models import encode_image,get_image_caption,text_embedding
image_chat_bp = Blueprint('image_chat', __name__)
database = sampleDB()
def get_label(image_file):
    ##ファイルのencode
    file_content = image_file.read()
    #base64にする前にリサイズしなきゃいけない気がする。
    file_content = Im.open(BytesIO(file_content))
    new_width = 90
    new_height = 90
    resized_image = file_content.resize((new_width, new_height))
    buffer = BytesIO()
    resized_image.save(buffer, format='PNG')
    file_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    ##OpenAIの呼び出し
    image_caption = get_image_caption(b64_image=file_base64)
    return image_caption
###この関数使わない
"""
def get_word_list(user_message):
    text = user_message
    openai.api_key = current_app.config['OPENAI_API_KEY']
    openai.api_type = "azure"
    openai.api_base = current_app.config['OPENAI_ENDPOINT']
    openai.api_version = "2023-05-15"
    prompt_path = 'flask_app/data/word_list_prompt.txt'
    prompt = ""

    with open(prompt_path) as f:
        prompt = str(f.read())

    #日本語
    #with open(prompt_path, 'r', encoding='utf-8') as f:
        #prompt = str(f.read())

    prompt = prompt.format(input=text)
    completion = openai.ChatCompletion.create(
    deployment_id='GPT35TURBO',
    messages=[
        {"role": "user", "content": prompt}
             ])
    responce = completion.choices[0].message['content']
    word_list = responce.split(",")
    return word_list
"""
@image_chat_bp.route('/image_chat/list', methods=['GET'])
def list():
    images = Image.get_all_images()
    return render_template('image_chat.list.html', images=images)

@image_chat_bp.route('/image_chat/delete', methods=['POST'])
def delete():
    query = ""
    query = request.args.get('file_name')
    if query:
        #database = sampleDB()
        Image.delete(query)
        #database.delete(file_name=query)
        os.remove(os.path.join(current_app.config['UPLOAD_FILE_PATH'], query))
        current_app.logger.info("Delete " + query + " from database and file system successfully.")
    return redirect(url_for('image_chat.list'))

@image_chat_bp.route('/image_chat')
def chat():
    return render_template('image_chat.index.html')

@image_chat_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image-input' not in request.files:
        current_app.logger.warning("No file part")
        return redirect(request.url)
    file = request.files['image-input']

    if file and file.filename != '':
        label = get_label(file)
        new_image = Image(file_name=file.filename, label=label)
        if Image.isInSameName(file.filename):
            current_app.logger.warning("Same file name exists")
            return jsonify({"error": "Same file name exists"}), 400
        database = sampleDB()
        database.insert(file_name=file.filename,
                        label=label)
        file_path = os.path.join(current_app.config['UPLOAD_FILE_PATH'], file.filename)
        new_image.register()
        file.seek(0)
        file.save(file_path)
        current_app.logger.info("Save " + file.filename + " to database and file system successfully.")
        return jsonify({"message": "Upload image successfully."}), 200
    return jsonify({"error": "Upload image failed."}), 400

@image_chat_bp.route('/image_chat/send_message', methods=['POST'])
def send_message():
    ###ひとまずデータベースから与えられた単語に一致するデータを拾ってくる。
    ###user_messageは本来単語じゃないのでGPTを使って単語のリストに処理する必要がある。
    user_message = request.form.get('message')
    #word_list = get_word_list(user_message)
    #取り出してみる
    #result = ""
    database = sampleDB()
    print("user_message is {}".format(user_message))
    file_list = database.search(str(user_message),k=1)
    """
    以下使わない関数
    for word in word_list:
        images = Image.get_all_images_by_label(label_name=word)
        #とりあえず三件だけ取り出してみる[:num]を調整することで数変えられる。
        for image in images[:3]:
            file_list.append(image.file_name)
    """
    print(file_list)
    return jsonify(file_list)