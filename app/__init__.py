import os, json
from flask import Flask, render_template, Markup, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

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
    # create and configure the app
    app = CustomFlask(__name__, instance_relative_config=True, static_folder='../instance/dist/static', template_folder='../instance/dist')
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
    )
    # print(os.environ['DATABASE_URL'])
    db = SQLAlchemy(app)

    class Control(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        form_id = db.Column(db.String(80), unique=True, nullable=False)
        is_filled = db.Column(db.Boolean, unique=False, nullable=False)
        doc_id = db.Column(db.String(80), unique=False, nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username


    @app.route('/control')
    def control():
        try:
            return '<h1>It works.</h1>' + Markup.escape(str(a))
        except Exception as e:
            return '<h1>Something is broken.</h1>' + str(e)

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

    return app
