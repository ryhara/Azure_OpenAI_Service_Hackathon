from flask import Blueprint, render_template, redirect, url_for

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
	return render_template('chat_index.html')