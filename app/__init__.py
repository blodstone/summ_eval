import os
from flask import Flask, render_template, send_from_directory, Markup
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
    app = CustomFlask(__name__, instance_relative_config=True, static_folder='../dist/static', template_folder='../dist')
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

    return app