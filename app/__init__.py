from flask import Flask, render_template

app = Flask('__name__', static_folder='../dist/static', template_folder='../dist')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')