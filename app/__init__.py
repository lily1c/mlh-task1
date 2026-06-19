import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

pages = [
    {"name": "Home", "url": "/"},
    {"name": "Hobbies", "url": "/hobbies"},
]

about = (
    "I study CompE major Mount Vernon Nazarene University "
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