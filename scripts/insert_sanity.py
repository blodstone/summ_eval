import json
import os

from backend.models import Document
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)
    folder = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/Raw'
    for file in os.listdir(folder):
        # print(file)
        if 'json' in file:
            file_path = os.path.join(folder, file)
            doc_id = os.path.splitext(file)[0]
            with open(file_path, 'r') as infile:
                data = json.load(infile)
                doc = db.session.query(Document).filter_by(doc_id=doc_id).first()
                doc.sanity_statement = data['statement']
                doc.sanity_answer = data['answer']
                db.session.commit()

