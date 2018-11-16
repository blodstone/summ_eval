import os
import json
import http
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from backend.models import User, Document, Project, Result, db

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
                return jsonify(document)
    return '', http.HTTPStatus.NO_CONTENT


@api.route('/project/<dataset_name>', methods=['POST'])
def api_project_create(dataset_name):
    if request.method == 'POST':
        data = request.get_json()
        project = Project.create_project(**data, dataset_id=dataset_name)
        if project:
            return '', http.HTTPStatus.CREATED
        else:
            return '', http.HTTPStatus.NO_CONTENT


@api.route('/project/<project_id>', methods=['GET'])
def api_project(project_id):
    project = Project.query.filter_by(project_id=project_id).first()
    if not project:
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return jsonify(project)


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
