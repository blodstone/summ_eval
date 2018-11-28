import jwt
import os
from datetime import datetime, timedelta
from flask import jsonify, request

from backend.models import User, Document, AnnotationProject, AnnotationResult, Dataset, DocStatus, db
from . import api


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
    }, os.getenv('SECRET_KEY')
    )
    return jsonify({'token': token.decode('UTF-8')})
