import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Document(db.Model):
    __tablename__ = 'document'

    doc_id = db.Column(db.String(25), primary_key=True, nullable=False)
    doc_json = db.Column(db.Text, nullable=False)
    has_highlight = db.Column(db.Boolean, nullable=False, default=False)
    doc_statuses = db.relationship('DocStatus', backref='document', lazy=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=True)

    @classmethod
    def get_dict(cls, doc_id):
        if not doc_id:
            return None
        document = cls.query.filter_by(doc_id=doc_id).first()
        return json.loads(document.doc_json)

    @classmethod
    def add_results(cls, doc_id, results):
        document = cls.query.filter_by(doc_id=doc_id).first()
        doc_json = json.loads(document.doc_json)
        doc_json['results'] = results
        document.doc_json = json.dumps(doc_json)
        document.has_highlight = True
        db.session.commit()

    def to_dict(self):
        return self.doc_json


class DocStatus(db.Model):
    __tablename__ = 'doc_status'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    total_exp_results = db.Column(db.Integer, nullable=False)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('document.doc_id'), nullable=False)
    proj_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    results = db.relationship('AnnotationResult', backref='doc_status', lazy=True)

    @classmethod
    def close(cls, id):
        doc_status = cls.query.filter_by(id=id).first()
        doc_status.is_closed = True
        db.session.commit()


class SummaryGroup(db.Model):
    __tablename__ = 'summary_group'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_ref = db.Column(db.Boolean, nullable=False, default=False)
    summaries = db.relationship('Summary', backref='summary_group', lazy=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)


class Summary(db.Model):
    __tablename__ = 'summary'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    summary_group_id = db.Column(db.Integer, db.ForeignKey('summary_group.id'), nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('document.doc_id'), nullable=False)
    summary_statuses = db.relationship('SummaryStatus', backref='summary', lazy=True)


class SummaryStatus(db.Model):
    __tablename__ = 'summary_status'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    summary_id = db.Column(db.Integer, db.ForeignKey('summary.id'), nullable=False)
    total_exp_results = db.Column(db.Integer, nullable=False)
    proj_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    @classmethod
    def close(cls, id):
        summary_status = cls.query.filter_by(id=id).first()
        summary_status.is_closed = True
        db.session.commit()


class EvaluationResult(db.Model):
    __tablename__ = 'evaluation_result'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)
    precision = db.Column(db.REAL, nullable=False, default=0.0)
    recall = db.Column(db.REAL, nullable=False, default=0.0)
    fluency = db.Column(db.REAL, nullable=False, default=0.0)
    status_id = db.Column(db.Integer, db.ForeignKey('summary_status.id'), nullable=False)


class AnnotationResult(db.Model):
    __tablename__ = 'annotation_result'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)
    result_json = db.Column(db.Text, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('doc_status.id'), nullable=False)

    @classmethod
    def create_result(cls, **kwargs):
        result = AnnotationResult(
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
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    doc_statuses = db.relationship('DocStatus', backref='project', lazy=True)
    summary_statuses = db.relationship('SummaryStatus', backref='project', lazy=True)

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
                if project.type == 'Highlight':
                    doc_status = DocStatus(
                        proj_id=project.id,
                        doc_id=document.doc_id,
                        total_exp_results=kwargs['total_exp_results'])
                    db.session.add(doc_status)
                    db.session.commit()
                elif project.type == 'Evaluation':
                    pass
            return project

    @classmethod
    def deactivate(cls, id):
        project = cls.query.filter_by(id=id).first()
        project.is_active = False
        db.session.commit()

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
