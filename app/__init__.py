import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

work_experiences = [
    {
        "title": "Software Intern",
        "company": "Example Corp",
        "dates": "Summer 2024",
        "description": "Built internal tools with Python and Flask.",
    },
    {
        "title": "Teaching Assistant",
        "company": "My University",
        "dates": "2023 - Present",
        "description": "Helped students with computer science coursework.",
    },
]

education = [
    {
        "school": "My University",
        "degree": "B.S. Computer Science",
        "dates": "2022 - Present",
    },
]

hobbies = [
    {"name": "Photography"},
    {"name": "Hiking"},
    {"name": "Reading"},
]

pages = [
    {"endpoint": "index", "name": "Home", "url": "/"},
    {"endpoint": "hobbies", "name": "Hobbies", "url": "/hobbies"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        work_experiences=work_experiences,
        education=education,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="My Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies,
        pages=pages,
    )
