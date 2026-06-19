import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

pages = [
    {"name":"Home", "url":"/"},
   # {"name":"Hobbies", "url":"/hobbies"},

]

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), pages=pages)

