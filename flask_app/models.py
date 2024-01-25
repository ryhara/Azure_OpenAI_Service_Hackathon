from flask_app import db
from sqlalchemy import Column, Integer, String
import chromadb
from chromadb.config import Settings
from openai import AzureOpenAI
from flask import Blueprint, render_template, redirect, url_for, request, current_app, jsonify, current_app
import requests
import base64



class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, unique=True)
    label = db.Column(db.String)

    def __init__(self, file_name, label):
        self.file_name = file_name
        self.label = label

    def __repr__(self):
        return '<Image %r>' % self.file_name

    def register(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, file_name):
        if file_name:
            db.session.query(cls).filter(cls.file_name == file_name).delete()
            db.session.commit()

    @classmethod
    def get_all_images_by_label(cls, label_name):
        return cls.query.filter(cls.label.like(f"%{label_name}%")).all()

    @classmethod
    def get_all_images(cls):
        return cls.query.all()

    @classmethod
    def count_images(cls):
        return cls.query.count()

    @classmethod
    def isInSameName(cls, file_name):
        return cls.query.filter(cls.file_name == file_name).count() > 0
    

####ここから先新しいchromaDBの設定に関する記述
class sampleDB:
  def __init__(self):
    self.db = chromadb.Client(
       Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="/app/instance/chroma"
        )
    )
    self.collection = self.db.get_or_create_collection(name="image",
                                                  )
  def search(self,query,k):
    collection = self.db.get_or_create_collection(name="image",
                                                  )
    query = self.__get_embedding(query)
    results = collection.query(
    query_embeddings=[query], 
    n_results=k
    )
    return results['ids'][0]
  def insert(self,file_name,label):
    ##file_nameは一意に定まらなければ自動的に削除される
    collection = self.db.get_or_create_collection(name="image",
                                                  metadata={"hnsw:space":"cosine"})
    collection.add(
    ids=[file_name], 
    documents=[label],
    embeddings=self.__get_embedding(label)
               )
    return 1
  def delete(self,file_name):
     collection = self.db.get_or_create_collection(name="image",
                                                  metadata={"hnsw:space":"cosine"})
     collection.delete(ids = [file_name])
     return 1
  def __get_embedding(self,text):
    api_key = current_app.config['OPENAI_API_KEY']
    azure_endpoint = current_app.config['OPENAI_ENDPOINT']
    client = AzureOpenAI(
       api_key = api_key,
       azure_endpoint = azure_endpoint,
       api_version = "2023-05-15"
    )
    response = client.embeddings.create(
     model='ADA',
     input=text
    )
    return response.data[0].embedding

###ここから先image_captionについての記述
def encode_image(image_path):
   with open(image_path,"rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_caption(b64_image):
    azure_endpoint =  current_app.config['OPENAI_ENDPOINT']+"/openai/deployments/GPT4/chat/completions?api-version=2023-12-01-preview"
    api_key = current_app.config['OPENAI_API_KEY']
    gpt4_turbo_vision = "gpt-4-vision-preview"
    prompt = "please describe this image."
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
       max_tokens=15
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