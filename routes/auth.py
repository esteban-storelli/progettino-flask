from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from models.connection import db
from models.user import User

app = Blueprint("auth", __name__)

@app.route("/register")
def show_register_page():
    return render_template("register.html", user=current_user)

@app.route("/login")
def show_login_page():
    return render_template("login.html", user=current_user)

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    if not email or not username or not password or not confirm:
        flash("Please fill out all fields.")
        return redirect(url_for("auth.show_register_page"))

    if password != confirm:
        flash("Passwords do not match.")
        return redirect(url_for("auth.show_register_page"))
    stmt = db.select(User).filter_by(username=username)

    stmt = db.select(User).filter_by(email=email)
    existing_email = db.session.execute(stmt).scalar_one_or_none()
    if existing_email:
        flash("Email already registered.")
        return redirect(url_for("auth.show_register_page"))
    
    existing_username = db.session.execute(stmt).scalar_one_or_none()
    if existing_username:
        flash("Username already taken.")
        return redirect(url_for("auth.show_register_page"))

    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect(url_for("auth.show_profile"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    stmt = db.select(User).filter_by(email=email)
    user: User = db.session.execute(stmt).scalar_one_or_none()

    if user:
        if user.check_password(password=password):
              login_user(user)
              return redirect(url_for("auth.show_profile"))
        else:
            flash("Invalid password.")
            return redirect(url_for("auth.login"))
    else:
        flash("Invalid username.")
        return redirect(url_for("auth.login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("default.show_main_page"))

@app.route("/profile")
@login_required
def show_profile():
    return render_template("/profile.html", user=current_user)