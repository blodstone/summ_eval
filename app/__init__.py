import sys, logging
from flask import Flask, render_template

app = Flask('__name__', static_folder='../dist', template_folder='dist')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')