from flask import Blueprint, render_template, redirect, url_for, request, current_app, jsonify
import io
import os
import openai
import requests
from flask_app.models import Image
upload_dir_path = '/app/flask_app/uploads/'
image_chat_bp = Blueprint('image_chat', __name__)

def get_label(image_file):
    """
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
    print(image_caption)
    """
    return "penguin"

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

    if file and file.filename != '':
        new_image = Image(file_name=file.filename, label=get_label(file.read()))
        file_path = os.path.join(upload_dir_path,file.filename)
        new_image.register()
        file.save(file_path)
        return redirect(url_for('image_chat.chat'))
    return redirect(request.url)

@image_chat_bp.route('/image_chat/send_message', methods=['POST'])
def send_message():
    ###ひとまずデータベースから与えられた単語に一致するデータを拾ってくる。
    ###user_messageは本来単語じゃないのでGPTを使って単語のリストに処理する必要がある。
    user_message = request.form.get('message')
    word_list = get_word_list(user_message)
    #取り出してみる
    result = ""
    path_list = []
    for word in word_list:
        images = Image.get_all_images_by_label(label_name=word)
        #とりあえず三件だけ取り出してみる[:num]を調整することで数変えられる。
        for image in images[:3]:
            file_path = os.path.join(upload_dir_path,image.file_name)
            path_list.append(file_path)
    return jsonify(path_list)