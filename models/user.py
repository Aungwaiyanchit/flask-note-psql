from db import db
from flask_bcrypt import generate_password_hash
import uuid


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.String(80), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(80))
    password = db.Column(db.String(100))
    
    notes = db.relationship('NoteModel', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, 10).decode('utf-8')

    def json(self): 
        return {
            "id": self.id,
            "username": self.username,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()