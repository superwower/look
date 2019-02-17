from flask_sqlalchemy import SQLAlchemy
from typing import Any

db = SQLAlchemy()  # type: Any


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    face_id = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('faces', lazy=True))
