from flask import Blueprint, render_template, redirect, url_for, request, current_app, jsonify, current_app
import io
import os
import openai
import requests
from flask_app.models import Image

image_chat_bp = Blueprint('image_chat', __name__)

def get_label(image_file):
    vision_base_url = "https://japaneast.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "analyze"
    # リクエストのヘッダーとパラメータ(local)
    subscription_key = current_app.config['AZURE_IMAGE_CAPTIONING_API_KEY']
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    with io.BytesIO(image_file) as image_data:
        response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
    analysis = response.json()
    #responseから説明を取り出す
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    return image_caption

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

@image_chat_bp.route('/image_chat/list', methods=['GET'])
def list():
    images = Image.get_all_images()
    return render_template('image_chat.list.html', images=images)

@image_chat_bp.route('/image_chat/delete', methods=['POST'])
def delete():
    query = ""
    query = request.args.get('file_name')
    print(query)
    if query:
        Image.delete(query)
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
        new_image = Image(file_name=file.filename, label=get_label(file.read()))
        file_path = os.path.join(current_app.config['UPLOAD_FILE_PATH'], file.filename)
        new_image.register()
        file.seek(0)
        file.save(file_path)
        current_app.logger.info("Save " + file.filename + " to database and file system successfully.")
        return redirect(url_for('image_chat.list'))
    return redirect(request.url)

@image_chat_bp.route('/image_chat/send_message', methods=['POST'])
def send_message():
    ###ひとまずデータベースから与えられた単語に一致するデータを拾ってくる。
    ###user_messageは本来単語じゃないのでGPTを使って単語のリストに処理する必要がある。
    user_message = request.form.get('message')
    word_list = get_word_list(user_message)
    #取り出してみる
    result = ""
    file_list = []
    for word in word_list:
        images = Image.get_all_images_by_label(label_name=word)
        #とりあえず三件だけ取り出してみる[:num]を調整することで数変えられる。
        for image in images[:3]:
            file_list.append(image.file_name)
    return jsonify(file_list)