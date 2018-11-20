import json
import os
from backend.models import Document, Dataset, Summary, SummaryGroup, db
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy


def init_dataset(db):
    dataset_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_Single/dataset_Sample_BBC'
    # TODO: Dataset name by folder name
    dataset_name = os.path.split(dataset_path)[1][8:]
    dataset = Dataset(name=dataset_name)
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


def init_summary(db):
    summary_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_Single/summ_Sample_BBC'
    dataset_name = os.path.split(summary_path)[1][5:]
    dataset = db.session.query(Dataset).filter_by(name=dataset_name).first()
    if not dataset:
        print('Dataset {name} not found in database'.format(name=dataset_name))
        return
    for folder in os.listdir(summary_path):
        is_ref = False
        if folder.startswith('summ_'):
            summ_group_name = folder[5:]
            if 'ref' in summ_group_name:
                is_ref = True
            summary_group = SummaryGroup(name=summ_group_name, dataset_id=dataset.id, is_ref=is_ref,)
            db.session.add(summary_group)
            db.session.commit()
            folder_path = os.path.join(summary_path, folder)
            for file in os.listdir(folder_path):
                with open(os.path.join(folder_path, file), 'r') as infile:
                    text = ' '.join(infile.readlines()).strip()
                    summary = Summary(
                        doc_id=os.path.splitext(file)[0],
                        text=text,
                        summary_group_id=summary_group.id
                    )
                    db.session.add(summary)
                    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)
    init_dataset(db)
    init_summary(db)
