import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Document(db.Model):
    __tablename__ = 'document'

    doc_id = db.Column(db.String(25), primary_key=True)
    doc_json = db.Column(db.Text, nullable=False)
    doc_statuses = db.relationship('Doc_Status', backref='document', lazy=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=True)
    @classmethod
    def get_dict(cls, doc_id):
        if not doc_id:
            return None
        document = cls.query.filter_by(doc_id=doc_id).first()
        return json.loads(document.json)


class DocStatus(db.Model):
    __tablename__ = 'doc_status'

    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('document.doc_id'), nullable=False)
    pro_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    numberOfAnnotations = db.Column(db.Integer, nullable=False)
    results = db.relationship('Result', backref='doc_status', lazy=True)


class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)
    result_json = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('doc_status.id'), nullable=False)


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    docs = db.relationship('Document', backref='dataset', lazy=True)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'), method='sha256')

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
