from openai import AzureOpenAI
from flask import Blueprint, render_template, redirect, url_for, request, current_app, jsonify, current_app
from flask_app.models import Image
import requests
import base64

def encode_image(image_path):
   with open(image_path,"rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_caption(image_path):
    azure_endpoint =  current_app['OPENAI_ENDPOINT']+"/openai/deployments/GPT4/chat/completions?api-version=2023-12-01-preview"
    api_key = current_app.config['OPENAI_API_KEY']
    gpt4_turbo_vision = "gpt-4-vision-preview"
    prompt = "please describe this image."
    b64_image = encode_image(image_path)
    client = AzureOpenAI(
       api_key = api_key,
       azure_endpoint = azure_endpoint,
       api_version = "2023-12-01-preview"
    )
    response = client.chat.completions.create(
       model = gpt4_turbo_vision,
       messages=[
          {
             "role":"user",
             "content":[
                {
                   "type":"text",
                   "text":prompt
                },
                {
                   "type":"image_url",
                   "image_url":{
                      "url":f"data:image/jpeg;base64,{b64_image}",
                      "detail":"low"
                   }
                }
             ]
          }
       ],
       max_tokens=30
    )
    image_caption = str(response.choices[0].message.content)
    return image_caption


def text_embedding(input):
  api_key = current_app.config['OPENAI_API_KEY']
  azure_endpoint = current_app.config['OPENAI_ENDPOINT']
  client = AzureOpenAI(
       api_key = api_key,
       azure_endpoint = azure_endpoint,
       api_version = "2023-05-15"
    )
  response = client.embeddings.create(
     model='ADA',
     input=input
  )
  return response.data[0].embedding