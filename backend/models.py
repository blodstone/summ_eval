import json
import uuid
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()


class ProjectType(Enum):
    ANNOTATION = 'Annotation'
    EVALUATION = 'Evaluation'


class ProjectCategory(Enum):
    INFORMATIVENESS = 'Informativeness'
    FLUENCY = 'Fluency'
    HIGHLIGHT = 'Highlight'


class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    doc_id = db.Column(db.String(25), nullable=False)
    doc_json = db.Column(db.Text, nullable=False)
    has_highlight = db.Column(db.Boolean, nullable=False, default=False)

    doc_statuses = db.relationship('DocStatus', backref='document', lazy=True)

    dataset_id = db.Column(db.INTEGER, db.ForeignKey('dataset.id'), nullable=True)

    @classmethod
    def get_dict(cls, id):
        if not id:
            return None
        document = cls.query.get(id)
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

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    total_exp_results = db.Column(db.Integer, nullable=False)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)

    doc_id = db.Column(db.INTEGER, db.ForeignKey('document.id'), nullable=False)
    proj_id = db.Column(db.INTEGER, db.ForeignKey('annotation_project.id'), nullable=False)

    results = db.relationship('AnnotationResult', backref='doc_status', lazy=True)

    @classmethod
    def close(cls, id):
        doc_status = cls.query.filter_by(id=id).first()
        doc_status.is_closed = True
        db.session.commit()


class SummaryGroup(db.Model):
    __tablename__ = 'summary_group'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_ref = db.Column(db.Boolean, nullable=False, default=False)

    dataset_id = db.Column(db.INTEGER, db.ForeignKey('dataset.id'), nullable=False)
    summaries = db.relationship('Summary', backref='summary_group', lazy=True)


class Summary(db.Model):
    __tablename__ = 'summary'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)

    summary_group_id = db.Column(db.INTEGER, db.ForeignKey('summary_group.id'), nullable=False)
    doc_id = db.Column(db.INTEGER, db.ForeignKey('document.id'), nullable=False)

    summary_statuses = db.relationship('SummaryStatus', backref='summary', lazy=True)


class SummariesPair(db.Model):
    __tablename__ = 'summaries_pair'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)

    ref_summary_id = db.Column(db.INTEGER, db.ForeignKey('summary.id'), nullable=False)
    system_summary_id = db.Column(db.INTEGER, db.ForeignKey('summary.id'), nullable=False)
    dataset_id = db.Column(db.INTEGER, db.ForeignKey('dataset.id'), nullable=False)


class SummaryStatus(db.Model):
    __tablename__ = 'summary_status'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    total_exp_results = db.Column(db.Integer, nullable=False)

    summary_id = db.Column(db.INTEGER, db.ForeignKey('summary.id'), nullable=False)
    proj_id = db.Column(db.INTEGER, db.ForeignKey('evaluation_project.id'), nullable=False)

    results = db.relationship('EvaluationResult', backref='summary_status', lazy=True)

    @classmethod
    def close(cls, id):
        summary_status = cls.query.get(id)
        summary_status.is_closed = True
        db.session.commit()


class EvaluationResult(db.Model):
    __tablename__ = 'evaluation_result'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)
    precision = db.Column(db.REAL, nullable=False, default=0.0)
    recall = db.Column(db.REAL, nullable=False, default=0.0)
    fluency = db.Column(db.REAL, nullable=False, default=0.0)

    status_id = db.Column(db.INTEGER, db.ForeignKey('summary_status.id'), nullable=False)

    @classmethod
    def create_result(cls, **kwargs):
        result = None
        if kwargs['category'] == ProjectCategory.INFORMATIVENESS:
            result = EvaluationResult(
                precision=kwargs['precision'], recall=kwargs['recall'], status_id=kwargs['status_id'])
            db.session.add(result)
            db.session.commit()
        elif kwargs['category'] == ProjectCategory.FLUENCY:
            result = EvaluationResult(fluency=kwargs['fluency'], status_id=kwargs['status_id'])
            db.session.add(result)
            db.session.commit()
        return result


class AnnotationResult(db.Model):
    __tablename__ = 'annotation_result'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    finished_at = db.Column(db.DateTime, default=datetime.utcnow)
    result_json = db.Column(db.Text, nullable=False)

    status_id = db.Column(db.INTEGER, db.ForeignKey('doc_status.id'), nullable=False)

    @classmethod
    def create_result(cls, **kwargs):
        result = AnnotationResult(
            result_json=json.dumps(kwargs['result_json']), status_id=kwargs['status_id'])
        db.session.add(result)
        db.session.commit()
        return result


class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    documents = db.relationship('Document', backref='dataset', lazy=True)
    annotation_projects = db.relationship('AnnotationProject', backref='dataset', lazy=True)
    evaluation_projects = db.relationship('EvaluationProject', backref='dataset', lazy=True)

    def to_dict(self):
        return dict(name=self.name)


class BaseProject(object):
    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(25), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    @declared_attr
    def dataset_id(cls):
        return db.Column(db.INTEGER, db.ForeignKey('dataset.id'), nullable=False)

    @classmethod
    def deactivate(cls, id):
        project = cls.query.get(id)
        project.is_active = False
        db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id, name=self.name, category=self.category,
            created_at=self.created_at, finished_at=self.finished_at,
            is_active=self.is_active
        )


class AnnotationProject(db.Model, BaseProject):
    __tablename__ = 'annotation_project'

    doc_statuses = db.relationship('DocStatus', backref='project', lazy=True)

    @classmethod
    def create_project(cls, **kwargs):
        dataset = Dataset.query.filter_by(name=kwargs['dataset_name']).first()
        # noinspection PyArgumentList
        project = AnnotationProject(name=kwargs['name'], category=kwargs['category'], dataset_id=dataset.id)
        db.session.add(project)
        db.session.commit()
        for document in dataset.documents:
            doc_status = DocStatus(
                proj_id=project.id,
                doc_id=document.id,
                total_exp_results=kwargs['total_exp_results'])
            db.session.add(doc_status)
            db.session.commit()
        return project


class EvaluationProject(BaseProject, db.Model):
    __tablename__ = 'evaluation_project'

    summ_group_id = db.Column(db.INTEGER, db.ForeignKey('summary_group.id'), nullable=False)
    summ_statuses = db.relationship('SummaryStatus', backref='project', lazy=True)

    @classmethod
    def create_project(cls, **kwargs):
        dataset = Dataset.query.filter_by(name=kwargs['dataset_name']).first()
        if not dataset:
            return None
        summ_group = SummaryGroup.query.filter_by(name=kwargs['summ_group_name']).first()
        if not summ_group:
            return None
        # noinspection PyArgumentList
        project = EvaluationProject(
            name=kwargs['name'], category=kwargs['category'], dataset_id=dataset.id, summ_group_id=summ_group.id)
        db.session.add(project)
        db.session.commit()
        for summary in summ_group.summaries:
            summ_status = SummaryStatus(
                proj_id=project.id,
                summary_id=summary.id,
                total_exp_results=kwargs['total_exp_results'])
            db.session.add(summ_status)
            db.session.commit()
        return project


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False)
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
