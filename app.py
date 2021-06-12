import Controller.judge
import os
from dotenv import load_dotenv
from flask import Flask
from Middleware.auth import assert_auth

app = Flask(__name__)
load_dotenv()


@app.route('/')
def index():
    with open('./index.html', 'r') as f:
        return f.read()


@app.route('/judge/create', methods=['POST'])
@assert_auth
def judge_create():
    return Controller.judge.create()


@app.route('/judge/status/<task_id>', methods=['GET'])
def judge_status(task_id):
    return Controller.judge.status(task_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
