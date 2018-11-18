import os
import json
import http
import jwt
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
            if doc_status.totalExpResults == n_results:
                continue
            else:
                return jsonify(document.to_dict())
    return '', http.HTTPStatus.NO_CONTENT


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
    progress = "{0:.2f}".format(n_results/doc_status.totalExpResults)
    return jsonify(dict(progress=progress))


@api.route('/json', methods=['POST'])
def send_json():
    file = open(os.path.join(api.static_folder, "gold_doc/doc.json"), "r")
    data = json.load(file)
    return jsonify(data)


@api.route('/save_annotation', methods=['POST'])
def save_annotation():
    result = request.get_json('highlights')
    if result:
        file = open(os.path.join(api.static_folder, "gold_doc/annotated.json"), "w")
        json.dump(result, file, sort_keys=False, indent=2)
    else:
        print('Empty result')
    return '', 204


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
