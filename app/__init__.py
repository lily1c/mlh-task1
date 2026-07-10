import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import MySQLDatabase
from .writing import get_articles
from playhouse.shortcuts import model_to_dict
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField
from flask import render_template

import datetime 
load_dotenv()
app = Flask(__name__)



mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

pages = [
    {"name": "Home", "url": "/"},
    {"name": "Hobbies", "url": "/hobbies"},
    {"name": "Map", "url": "/map"},
    {"name": "Writing", "url": "/writing"},
]

about = (
    "I'm a Computer Engineering junior at Mount Vernon Nazarene University "
    "(Mathematics minor) with a strong foundation in programming, robotics, "
    "network engineering, embedded systems, and AI. I'm a Production Engineering "
    "Fellow on the MLH x Meta track and an AI4ALL Ignite '26 fellow. I love "
    "building practical, scalable solutions and exploring how AI can create "
    "inclusive, real-world impact. Currently seeking research and internship "
    "opportunities in network engineering, embedded systems, and AI/ML engineering."
)

work_experiences = [
    {"title": "Production Engineering Fellow", "company": "Meta x Major League Hacking",
     "dates": "Jun 2026 – Present",
     "description": "Building reliable, scalable systems with Linux, networking, automation, and SRE practices alongside a global cohort and Meta mentors."},
    {"title": "Co-Founder, Growth & Infrastructure (DevOps/SRE)", "company": "Peechz",
     "dates": "Jan 2026 – Present",
     "description": "Helping build a video-first marketplace connecting builders with recruiters and capital; focused on growth and infrastructure."},
    {"title": "AI/ML Research Intern", "company": "AI4ALL",
     "dates": "Aug 2025 – Mar 2026",
     "description": "Built a deepfake-detection dual-model ensemble (Inception v3 + ViT) reaching 92% accuracy using PyTorch, CNNs, and transfer learning."},
    {"title": "Summer IT Technician – DTS & Motherboard Support", "company": "Mount Vernon Nazarene University",
     "dates": "May 2025 – May 2026",
     "description": "Provided IT support via service tickets, set up new systems, and assisted with student account onboarding using Jira and Cisco Meraki."},
    {"title": "ML/AI Researcher (SPUR 2025)", "company": "Mount Vernon Nazarene University",
     "dates": "May 2025 – Aug 2025",
     "description": "Built an ML pipeline (XGBoost + polynomial regression, R² > 0.94) on live sensor data for solar-panel optimization, achieving an 8–9% efficiency gain."},
    {"title": "Signal Team – Network Support", "company": "Mount Vernon Nazarene University",
     "dates": "Sep 2024 – May 2025",
     "description": "Monitored and troubleshot campus Wi-Fi, supported students with connectivity, and optimized network performance with ITS engineers."},
]

educations = [
    {"school": "Mount Vernon Nazarene University", "degree": "B.S. Computer Engineering (Mathematics minor)",
     "dates": "Sep 2024 – Dec 2026",
     "description": "Coursework in programming, robotics, network engineering, embedded systems, and AI."},
    {"school": "Columbia University", "degree": "Certificate — Machine Learning I",
     "dates": "Jan 2026 – Mar 2026",
     "description": "Supervised and unsupervised ML: regression, classification, and maximum likelihood."},
]

hobbies = [
    {"name": "Photography",
     "description": "Capturing moments and experimenting with composition and light.",
     "image": "https://images.unsplash.com/photo-1452780212940-6f5c0d14d848?w=600"},
    {"name": "Running",
     "description": "Staying grounded with outdoor runs — consistency over intensity.",
     "image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600"},
    {"name": "Mentoring & Volunteering",
     "description": "Leading sessions for students navigating college applications and tech careers.",
     "image": "https://images.unsplash.com/photo-1544027993-37dbfe43562a?w=600"},
    {"name": "Building side projects",
     "description": "Tinkering with AI/ML and infrastructure projects outside class.",
     "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600"},
]

visited = [
    {"place": "Mount Vernon, Ohio, USA", "lat": 40.3934, "lng": -82.4857, "note": "Home base — MVNU"},
    {"place": "Providence, Rhode Island, USA", "lat": 41.8240, "lng": -71.4128, "note": "Rhode Island"},
    {"place": "Seattle, Washington, USA", "lat": 47.6062, "lng": -122.3321, "note": "Seattle"},
    {"place": "Charlotte, North Carolina, USA", "lat": 35.2271, "lng": -80.8431, "note": "North Carolina"},
    {"place": "Detroit, Michigan, USA", "lat": 42.3314, "lng": -83.0458, "note": "Detroit"},
    {"place": "New York, USA", "lat": 40.7128, "lng": -74.0060, "note": "MLH × Meta Fellowship"},
    {"place": "San Francisco, USA", "lat": 37.7749, "lng": -122.4194, "note": "AI4ALL"},
    {"place": "Chicago, USA", "lat": 41.8781, "lng": -87.6298, "note": "GDG Summit"},
    {"place": "Turkmenistan", "lat": 38.9697, "lng": 59.5563, "note": "Where my journey started"},
]


@app.route('/')
def index():
    return render_template('index.html', title="Assol Abasova", url=os.getenv("URL"),
                           pages=pages, about=about,
                           work_experiences=work_experiences,
                           educations=educations, hobbies=hobbies)


@app.route('/hobbies')
def hobbies_page():
    return render_template('hobbies.html', title="My Hobbies",
                           pages=pages, hobbies=hobbies)


@app.route('/map')
def visited_map():
    return render_template('map.html', title="Places I've Visited",
                           pages=pages, visited=visited)

@app.route('/writing')
def writing_page():
    return render_template('writing.html', title="Writing",
                           pages=pages, articles=get_articles())

@app.route('/timeline')
def timeline_page():
    return render_template('timeline.html')

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    deleted = TimelinePost.delete().where(TimelinePost.id == post_id).execute()
    if deleted:
        return {'deleted': post_id}
    return {'error': f'post {post_id} not found'}, 404

