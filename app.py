from flask import Flask
from flask import render_template
from flask import url_for
from routes.web import app as bp_web
from routes.auth import app as bp_auth
from models.connection import db
from flask_migrate import Migrate
from flask_login import LoginManager
from models.user import User

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp_web)
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

