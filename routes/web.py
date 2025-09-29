from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

import wikipediaapi
import requests



app = Blueprint("default", __name__)

def get_random_articles(count=2):
    headers = {
        "User-Agent": "progettino-flask/1.0 (esteban.storelli@samtrevano.ch)"
    }

    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "format": "json",
            "action": "query",
            "list": "random",
            "rnlimit": count,
            "rnnamespace": 0
        },
        headers=headers
    )

    titles = [item['title'] for item in response.json()['query']['random']]

    wiki = wikipediaapi.Wikipedia(user_agent=headers["User-Agent"], language='en')

    for title in titles:
        page = wiki.page(title)
        print(f"Title: {title}\n")
        if page.exists():
            print(page.text)
        else:
            print("Page not found.")
        word_count = len(page.text.split())
        print(f"Word count: {word_count}\n")