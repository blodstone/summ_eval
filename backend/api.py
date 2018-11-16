import os
import json
import http
from flask import Blueprint, jsonify, request
from backend.models import User, Document

api = Blueprint('api', 'api', url_prefix='', static_folder='../../instance/dist/static')


# API
@api.route('/document/<doc_id>', methods=['GET', 'POST'])
def api_document(doc_id):
    if request.method == 'GET':
        doc_json = Document.get_dict(doc_id)
        if doc_json:
            return jsonify(doc_json), http.HTTPStatus.Ok

@api.route('/document/get_one', methods=['GET'])
def api_document_get_one():
    pass

@api.route('/json', methods=['POST'])
def send_json():
    file = open(os.path.join(api.static_folder, "gold_doc/doc.json"), "r")
    data = json.load(file)
    return jsonify(data)

@app.route('/save_annotation', methods=['POST'])
def save_annotation():
    result = request.get_json('highlights')
    if result:
        file = open(os.path.join(app.static_folder, "gold_doc/annotated.json"), "w")
        json.dump(result, file, sort_keys=False, indent=2)
    else:
        print('Empty result')
    return '', 204

@app.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/login', methods=['POST'])
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
    }, app.config['SECRET_KEY']
    )
    return jsonify({'token': token.decode('UTF-8')})
