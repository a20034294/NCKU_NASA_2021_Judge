import Controller.anime
import os
from dotenv import load_dotenv
from flask import Flask
from Middleware.auth import assert_auth

app = Flask(__name__)
load_dotenv()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/anime/create', methods=['POST'])
@assert_auth
def anime_create():
    return Controller.anime.create()


@app.route('/anime/status/<task_id>', methods=['GET'])
@assert_auth
def anime_status(task_id):
    return Controller.anime.status(task_id)
