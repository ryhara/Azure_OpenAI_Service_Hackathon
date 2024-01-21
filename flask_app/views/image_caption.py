import openai
from flask import Blueprint, render_template, redirect, url_for, request, current_app, jsonify, current_app
from flask_app.models import Image
import requests
import base64



def get_image_caption(image_path):
    vision_base_url = "https://japaneast.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "analyze"

    api_key = current_app.config['OPENAI_API_KEY']
    #openai.api_type = "azure"
    #openai.api_base = current_app.config['OPENAI_ENDPOINT']
    #subscription_key = current_app.config['AZURE_IMAGE_CAPTIONING_API_KEY']
    #openai.api_key = current_app.config['OPENAI_API_KEY']
    
    prompt_path = 'flask_app/data/caption_prompt.txt' #プロンプトは割と適当
    prompt = ""

    with open(prompt_path) as f:
      prompt = str(f.read())

    with open(image_path, 'rb') as image_file:
     image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    #headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/json'}
    #params = {'visualFeatures': 'Categories,Description,Color'}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": prompt,
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{image_data}"
                }
              }
            ]
          }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    analysis = response.json()
    image_caption = analysis['choices'][0]['message']['content']
    return image_caption


def text_embedding(input):
  response = openai.Embedding.create(
    model='text-embedding-ada-002',
    input=input
  )
  return response["data"][0]["embedding"]