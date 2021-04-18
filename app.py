import Controller.anime
import os
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)
load_dotenv()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/anime/create', methods=['POST'])
def anime_create():
    return Controller.anime.create()
