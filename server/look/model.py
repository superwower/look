from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    faces = db.relationship("Face")

class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    face_id = db.Column()
