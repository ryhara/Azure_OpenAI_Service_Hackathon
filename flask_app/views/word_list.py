from flask import Blueprint, render_template, redirect, url_for, request, current_app
import os
import openai

def send_message():
    user_message = request.form.get('message')
    text = ''
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
