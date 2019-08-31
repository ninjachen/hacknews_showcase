import requests
import json
from flask import Flask, escape, request
from string import Template

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/top-stories-1')
def top_stories():
    return requests.get('https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty').content


@app.route('/top-stories')
def top_stories():
    ids = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty').content
    template_string = 'https://hacker-news.firebaseio.com/v0/item/$id.json?print=pretty'
    s = Template(template_string)
    stories = []
    for id in ids:
        d = {'id': id}
        url = s.substitute(d)
        story = requests.get(url).content
        stories.append(story)

    json = {
        "stories": stories
    }
    return json.dumps(json)

@app.route('/top-story')
def top_story():
    id = request.args.get("id", -1)
    template_string = 'https://hacker-news.firebaseio.com/v0/item/$id.json?print=pretty'
    s = Template(template_string)
    d = {'id': id}
    url = s.substitute(d)
    return requests.get(url).content
    # return s.substitute(d)
