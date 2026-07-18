import os
import sys
import datetime

from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Liya.member import member as liya

load_dotenv()
app = Flask(__name__)

team = [
    liya,
]

pages = [
    {"endpoint": "index", "name": "Home", "url": "/"},
    {"endpoint": "hobbies", "name": "Hobbies", "url": "/hobbies"},
]

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost], safe=True)

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        team=team,
        pages=pages,
    )


@app.route("/hobbies")
def hobbies_page():
    return render_template(
        "hobbies.html",
        title="My Hobbies",
        url=os.getenv("URL"),
        team=team,
        pages=pages,
    )

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return 'Invalid name', 400

    if not email or '@' not in email:
        return 'Invalid email', 400

    if not content:
        return 'Invalid content', 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_post': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
@app.route("/timeline")
def timeline():
    return render_template('timeline.html', title="Timeline")
