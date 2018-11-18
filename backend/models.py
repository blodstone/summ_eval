import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Document(db.Model):
    __tablename__ = 'document'

    doc_id = db.Column(db.String(25), primary_key=True, nullable=False)
    doc_json = db.Column(db.Text, nullable=False)
    doc_statuses = db.relationship('DocStatus', backref='document', lazy=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=True)

    @classmethod
    def get_dict(cls, doc_id):
        if not doc_id:
            return None
        document = cls.query.filter_by(doc_id=doc_id).first()
        return document.doc_json

    def to_dict(self):
        return self.doc_json


class DocStatus(db.Model):
    __tablename__ = 'doc_status'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('document.doc_id'), nullable=False)
    proj_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    totalExpResults = db.Column(db.Integer, nullable=False)
    results = db.relationship('Result', backref='doc_status', lazy=True)


class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)
    result_json = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('doc_status.id'), nullable=False)

    @classmethod
    def create_result(cls, **kwargs):
        result = Result(
            result_json=json.dumps(kwargs['result_json']), status_id=kwargs['status_id'])
        db.session.add(result)
        db.session.commit()
        return result


class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    documents = db.relationship('Document', backref='dataset', lazy=True)
    projects = db.relationship('Project', backref='dataset', lazy=True)

    def to_dict(self):
        return dict(name=self.name)


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    doc_statuses = db.relationship('DocStatus', backref='project', lazy=True)

    @classmethod
    def create_project(cls, **kwargs):
        dataset = Dataset.query.filter_by(name=kwargs['dataset_name']).first()
        if not dataset:
            return None
        else:
            project = Project(name=kwargs['name'], type=kwargs['type'], dataset_id=dataset.id)
            db.session.add(project)
            db.session.commit()
            for document in dataset.documents:
                doc_status = DocStatus(
                    proj_id=project.id,
                    doc_id=document.doc_id,
                    totalExpResults=kwargs['totalExpResults'])
                db.session.add(doc_status)
                db.session.commit()
            return project

    def to_dict(self):
        return dict(id=self.id, name=self.name, type=self.type, created_at=self.created_at)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
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
