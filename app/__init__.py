import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/hobbies')
def hobbies():
    hobbies = [
        {"name": "Basketball", "description": "Small forward, regional champion."},
        {"name": "Coding", "description": "Building portfolio and ML projects."},
    ]
    return render_template('hobbies.html', title="My Hobbies", hobbies=hobbies)