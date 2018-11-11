import os
import json
from datetime import datetime, timedelta
from functools import wraps
from backend.models import db, User

import jwt
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, make_response, request
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))


def create_app(test_config=None):
    # Load .env file (create one if it doesn't exist)
    load_dotenv(os.path.join('../', '.env'))

    # create and configure the app
    app = CustomFlask(__name__, instance_relative_config=True,
                      static_folder='../../instance/dist/static',
                      template_folder='../../instance/dist')
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
    )

    db.init_app(app)


    def token_required(f):
        @wraps(f)
        def _verify(*args, **kwargs):
            auth_headers = request.headers.get('Authorization', '').split()
            invalid_msg = {
                'message': 'Invalid token. Registration and / or authentication required',
                'authenticated': False
            }
            expired_msg = {
                'message': 'Expired token. Re-authentication required.',
                'authenticated': False
            }
            if len(auth_headers) != 2:
                return jsonify(invalid_msg), 401

            try:
                token = auth_headers[1]
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = User.query.filter_by(email=data['sub']).first()
                if not user:
                    raise RuntimeError('User not found')
                return f(user, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify(expired_msg), 401
            except (jwt.InvalidTokenError, Exception) as e:
                print(e)
                return jsonify(invalid_msg), 401

        return _verify

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/app.js')
    def send_app_js():
        headers = {"Content-Disposition": "attachment; filename=%s" % 'app.js'}
        path = os.path.join(app.instance_path, 'dist', 'app.js')
        with open(path, 'r') as f:
            body = f.read()
        return make_response((body, headers))

    # API
    @app.route('/annotation_json', methods=['POST'])
    def send_annotation_json():
        file = open(os.path.join(app.static_folder, "gold_doc/annotated.json"), "r")
        data = json.load(file)
        return jsonify(data)

    @app.route('/json', methods=['POST'])
    def send_json():
        file = open(os.path.join(app.static_folder, "gold_doc/doc.json"), "r")
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

    return app
