import json
import os
from backend.models import Document, Dataset
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

def init_dataset(db):
    dataset_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset/xsum-extracts-from-downloads'
    dataset = Dataset(name='Sample_BBC')
    db.session.add(dataset)
    db.session.commit()
    for file in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, file)
        with open(file_path, 'r') as infile:
            json_result = json.load(infile)
            document = Document(
                dataset_id=dataset.id,
                doc_id=json_result['doc_id'],
                doc_json=json.dumps(json_result)
            )
            db.session.add(document)
            db.session.commit()


