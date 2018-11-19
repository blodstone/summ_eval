import os
import json
import http
import jwt
import urllib.parse
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from backend.models import User, Document, Project, Result, Dataset, DocStatus, db

api = Blueprint('api', 'api', url_prefix='', static_folder='../../instance/dist/static')


# API
@api.route('/document/<doc_id>', methods=['GET'])
def api_document_get(doc_id):
    if request.method == 'GET':
        doc_json = Document.get_dict(doc_id)
        if doc_json:
            return jsonify(doc_json), http.HTTPStatus.Ok


@api.route('/document/get_one', methods=['GET'])
def api_document_get_one():
    documents = Document.query.all()
    for document in documents:
        for doc_status in document.doc_statuses:
            n_results = len(Result.query.filter_by(id=doc_status.id).all())
            if doc_status.total_exp_results == n_results:
                continue
            else:
                return jsonify(document.to_dict())
    return '', http.HTTPStatus.NO_CONTENT


@api.route('/project/<project_id>/single_doc', methods=['GET'])
def api_project_single_doc(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        for doc_status in project.doc_statuses:
            n_results = len(Result.query.filter_by(id=doc_status.id).all())
            if doc_status.total_exp_results == n_results:
                continue
            else:
                doc_json = Document.get_dict(doc_status.doc_id)
                return jsonify(dict(doc_json=doc_json,
                                    doc_status_id=doc_status.id))


@api.route('/project', methods=['POST'])
def api_project_create():
    if request.method == 'POST':
        data = request.get_json()
        project = Project.create_project(**data)
        if project:
            return '', http.HTTPStatus.CREATED
        else:
            return '', http.HTTPStatus.CONFLICT


@api.route('/project/<project_id>', methods=['GET'])
def api_project_get(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return jsonify(project)


@api.route('/project/save_annotation', methods=['POST'])
def api_project_save_annotation():
    data = request.get_json()
    result = Result.create_result(**data)
    if result:
        return '', http.HTTPStatus.CREATED
    else:
        return '', http.HTTPStatus.CONFLICT


@api.route('/project/<project_id>/close', methods=['POST'])
def api_project_close(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project or project.is_active is False:
        return '', http.HTTPStatus.NOT_MODIFIED
    else:
        for doc_status in project.doc_statuses:
            results = Result.query.filter_by(status_id=doc_status.id).all()
            results_json = {}
            for result in results:
                results_json[result.id] = result.result_json
            if len(results_json) != 0:
                Document.add_results(doc_status.doc_id, results_json)
                DocStatus.close(doc_status.id)
        Project.deactivate(project_id)
        return '', http.HTTPStatus.OK


@api.route('/project/all_progress', methods=['GET'])
def api_project_progress():
    projects = Project.query.filter_by(is_active=True).all()
    if len(projects) == 0:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        result_json = {'projects': []}
        for project in projects:
            project_json = project.to_dict()
            project_json['dataset_name'] = \
                Dataset.query.filter_by(id=project.dataset_id).first().name
            total_n_results = 0
            total_total_exp_results = 0
            for doc_status in project.doc_statuses:
                n_results = Result.query.filter_by(status_id=doc_status.id).count()
                total_n_results += n_results
                total_total_exp_results += doc_status.total_exp_results
            if project.type == 'Highlight':
                form = 'annotation'
            elif project.type == 'Informativeness':
                form = 'inf_eval'
            project_json['progress'] = total_n_results/total_total_exp_results
            project_json['no'] = len(result_json['projects']) + 1

            project_json['link'] = urllib.parse.urljoin(
                request.host_url,
                '#/{form}/{id}'.format(id=project_json['id'], form=form))
            result_json['projects'].append(project_json)
        return jsonify(result_json)


@api.route('/dataset/<dataset_name>', methods=['GET'])
def api_dataset_get_single(dataset_name):
    dataset = Dataset.query.filter_by(name=dataset_name).first()
    if not dataset:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return jsonify(dataset.to_dict())


@api.route('/dataset', methods=['GET'])
def api_dataset_get_names():
    datasets = Dataset.query.all()
    if not datasets:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        result = dict()
        result['names'] = []
        for dataset in datasets:
            result['names'].append(dataset.name)
        return jsonify(result)


@api.route('/doc_status/progress/<doc_status_id>', methods=['GET'])
def api_doc_status_progress(doc_status_id):
    doc_status = DocStatus.query.filter_by(id=doc_status_id).first()
    if not doc_status:
        return '', http.HTTPStatus.NO_CONTENT
    n_results = len(Result.query.filter_by(id=doc_status.id).all())
    progress = "{0:.2f}".format(n_results/doc_status.total_exp_results)
    return jsonify(dict(progress=progress))


@api.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    user = User.authenticate(**data)
    print(user)
    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
    print('login success!')
    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, api.config['SECRET_KEY']
    )
    return jsonify({'token': token.decode('UTF-8')})
