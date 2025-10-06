from models.connection import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # Campo per la password criptata
    high_score = db.Column(db.Integer)
    number_of_plays = db.Column(db.Integer)
    total_points = db.Column(db.Integer)

    def set_password(self, password):
        """Imposta la password criptata."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se la password è corretta."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def pass_data(self):
        user_data = {
            "username": self.username,
            "high_score": self.high_score,
            "number_of_plays": self.number_of_plays,
            "total_points": self.total_points
        }
        return user_data