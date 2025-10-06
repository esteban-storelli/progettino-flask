from flask import Blueprint
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from time import sleep

import wikipediaapi
import requests

from utils.article import Article


app = Blueprint("default", __name__)

def get_random_article():
    headers = {
        "User-Agent": "progettino-flask/1.0 (esteban.storelli@samtrevano.ch)"
    }

    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "format": "json",
            "action": "query",
            "list": "random",
            "rnlimit": 1,
            "rnnamespace": 0
        },
        headers=headers
    )

    title = response.json()['query']['random'][0]['title']

    wiki = wikipediaapi.Wikipedia(user_agent=headers["User-Agent"], language='en')

    page = wiki.page(title)
    article = Article(title=title, body=page.text)
    return article

def get_article_by_title(title: str):
    headers = {
        "User-Agent": "progettino-flask/1.0 (esteban.storelli@samtrevano.ch)"
    }

    wiki = wikipediaapi.Wikipedia(user_agent=headers["User-Agent"], language='en')
    page = wiki.page(title)

    if not page.exists():
        return None

    article = Article(title=title, body=page.text)
    return article

@app.route("/game")
def start_game():
    return continue_game(start=True)


@app.route("/guess", methods=["POST"])
def guess_answer():
    higher_or_lower = request.form["button"]
    guess = 0
    if higher_or_lower == "higher":
        guess = 1
    elif higher_or_lower == "lower":
        guess = -1
    # 0 = Numero uguale di parole = Si vince in entrambi i casi
    if guess == session["correct_answer"] or session["correct_answer"] == 0:
        return continue_game(start=False)
    else:
        return render_template("/game_over.html", score=session["score"])

def continue_game(start: bool):
    sleep(1)
    article1 = None
    article2 = None
    if start:
        article1 = get_random_article()
        article2 = get_random_article()
        session["score"] = 0
    else:
        article1 = get_article_by_title(session["next_article_title"])
        article2 = get_random_article() 
        session["score"] += 1
    session["next_article_title"] = article2.title
    if article1.word_count > article2.word_count:
        session["correct_answer"] = -1
    elif article1.word_count < article2.word_count:
        session["correct_answer"] = 1
    else:
        session["correct_answer"] = 0
    return render_template("/game.html", article1=article1, article2=article2, score=session["score"])