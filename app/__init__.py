import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    work_experiences = [
        {"title": "Software Engineering Intern", "company": "Example Corp",
         "dates": "Jun 2025 – Aug 2025",
         "description": "Built internal tools with Flask and Python."},
        {"title": "IT Support Assistant", "company": "Campus IT",
         "dates": "2024 – 2025",
         "description": "Helped students and staff with technical issues."},
    ]

    educations = [
        {"school": "Mount Vernon", "degree": "High School Diploma",
         "dates": "2023 – 2026",
         "description": "Focus on computer science and mathematics."},
    ]

    hobbies = [
        {"name": "Basketball", "description": "Small forward, regional champion."},
        {"name": "Coding", "description": "Building portfolio and ML projects."},
    ]

    return render_template('index.html',
                           title="MLH Fellow",
                           url=os.getenv("URL"),
                           work_experiences=work_experiences,
                           educations=educations,
                           hobbies=hobbies)