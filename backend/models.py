import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Document(db.Model):
    __tablename__ = 'document'

    doc_id = db.Column(db.String(25), primary_key=True)
    json = db.Column(db.Text, nullable=False)
    is_highlighted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, doc_id, json):
        self.doc_id = doc_id
        self.json = json

    @classmethod
    def get_dict(cls, doc_id):
        if not doc_id:
            return None
        document = cls.query.filter_by(doc_id=doc_id).first()
        return json.loads(document.json)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id,
                    email=self.email,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))
