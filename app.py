from flask import Flask
from flask import render_template
from flask import url_for
from routes.web import app as bp_web
# from models.connection import db
# from models.model import User
from flask_migrate import Migrate
from flask_login import LoginManager
# from routes.auth import app as bp_auth

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp_default)
app.register_blueprint(bp_api, url_prefix="/api")
app.register_blueprint(bp_auth, url_prefix="/auth")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///labo1.db")
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user_callback(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default secret key") # random is also good for single instances

if __name__ == "__main__":
    app.run(debug=True)


import wikipediaapi
import requests

# url = "https://en.wikipedia.org/w/api.php"

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

print(response.status_code)
print(response.text)

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
