import json
import os

from backend.models import Document, Dataset, Summary, SummaryGroup, SummariesPair, User
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy


# def init_dataset(db):
#     dataset_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_Single/dataset_Sample_BBC'
#     dataset_name = os.path.split(dataset_path)[1][8:]
#     # Check dataset exist
#     dataset = db.session.query(Dataset).filter_by(name=dataset_name).first()
#     if not dataset:
#         dataset = Dataset(name=dataset_name)
#         db.session.add(dataset)
#         db.session.commit()
#
#     for file in os.listdir(dataset_path):
#         file_path = os.path.join(dataset_path, file)
#         with open(file_path, 'r') as infile:
#             json_result = json.load(infile)
#             # Check document exist
#             document = db.session.query(Document).filter_by(doc_id=json_result['doc_id']).first()
#             if not document:
#                 document = Document(
#                     dataset_id=dataset.id,
#                     doc_id=json_result['doc_id'],
#                     doc_json=json.dumps(json_result)
#                 )
#                 db.session.add(document)
#                 db.session.commit()
#
#
# def init_summary(db):
#     summary_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_Single/summ_Sample_BBC'
#     dataset_name = os.path.split(summary_path)[1][5:]
#     dataset = db.session.query(Dataset).filter_by(name=dataset_name).first()
#     if not dataset:
#         print('Dataset {name} not found in database'.format(name=dataset_name))
#         return
#     for folder in os.listdir(summary_path):
#         is_ref = False
#         if folder.startswith('summ_'):
#             summ_group_name = folder[5:]
#             if 'ref' in summ_group_name:
#                 is_ref = True
#             summary_group = SummaryGroup(name=summ_group_name, dataset_id=dataset.id, is_ref=is_ref,)
#             db.session.add(summary_group)
#             db.session.commit()
#             folder_path = os.path.join(summary_path, folder)
#             for file in os.listdir(folder_path):
#                 with open(os.path.join(folder_path, file), 'r') as infile:
#                     text = ' '.join(infile.readlines()).strip()
#                     summary = Summary(
#                         doc_id=os.path.splitext(file)[0],
#                         text=text,
#                         summary_group_id=summary_group.id
#                     )
#                     db.session.add(summary)
#                     db.session.commit()


def init_database(db):

    user = User(email='admin@localhost', password='localhost')
    db.session.add(user)
    db.session.commit()

    dataset_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_Single/Sample_BBC'
    dataset_name = os.path.split(dataset_path)[1]

    summaries_path = os.path.join(dataset_path, 'summaries')
    documents_path = os.path.join(dataset_path, 'documents')

    # Insert dataset
    dataset = Dataset(name=dataset_name)
    db.session.add(dataset)
    db.session.commit()

    # Insert documents
    for file in os.listdir(documents_path):
        file_path = os.path.join(documents_path, file)
        with open(file_path, 'r') as infile:
            json_result = json.load(infile)
            document = Document(
                dataset_id=dataset.id,
                doc_id=json_result['doc_id'],
                doc_json=json.dumps(json_result)
            )
            db.session.add(document)
            db.session.commit()

    # Insert Summaries
    for folder in os.listdir(summaries_path):
        if folder.startswith('ref'):
            summary_group = SummaryGroup(name='%s_ref_%s' % (dataset_name, folder[4:]),
                                         dataset_id=dataset.id, is_ref=True)
        elif folder.startswith('system'):
            summary_group = SummaryGroup(name='%s_system_%s' % (dataset_name, folder[7:]),
                                         dataset_id=dataset.id, is_ref=False)
        else:
            break
        db.session.add(summary_group)
        db.session.commit()
        ref_path = os.path.join(summaries_path, folder)
        for file in os.listdir(ref_path):
            with open(os.path.join(ref_path, file), 'r') as infile:
                text = ' '.join(infile.readlines()).strip()
                document = db.session.query(Document).filter_by(doc_id=os.path.splitext(file)[0]).first()
                summary = Summary(
                    doc_id=document.id,
                    text=text,
                    summary_group_id=summary_group.id
                )
                db.session.add(summary)
                db.session.commit()

    # Insert Pairs
    ref_summary_groups = db.session.query(SummaryGroup).filter_by(dataset_id=dataset.id, is_ref=True).all()
    system_summary_groups = db.session.query(SummaryGroup).filter_by(dataset_id=dataset.id, is_ref=False).all()

    for ref_summ_group in ref_summary_groups:
        for system_summ_group in system_summary_groups:
            for system_summary in system_summ_group.summaries:
                ref_summary = db.session.query(Summary)\
                    .filter_by(summary_group_id=ref_summ_group.id, doc_id=system_summary.doc_id).first()
                summaries_pair = SummariesPair(
                    ref_summary_id=ref_summary.id,
                    system_summary_id=system_summary.id,
                    dataset_id=dataset.id
                )
                db.session.add(summaries_pair)
                db.session.commit()

    # Create Summary
    # for folder in os.listdir(summaries_path):
    #     is_ref = False
    #     if folder.startswith('summ_'):
    #         summ_group_name = folder[5:]
    #         if 'ref' in summ_group_name:
    #             is_ref = True
    #         summary_group = SummaryGroup(name=summ_group_name, dataset_id=dataset.id, is_ref=is_ref,)
    #         db.session.add(summary_group)
    #         db.session.commit()
    #         folder_path = os.path.join(summary_path, folder)
    #         for file in os.listdir(folder_path):
    #             with open(os.path.join(folder_path, file), 'r') as infile:
    #                 text = ' '.join(infile.readlines()).strip()
    #                 summary = Summary(
    #                     doc_id=os.path.splitext(file)[0],
    #                     text=text,
    #                     summary_group_id=summary_group.id
    #                 )
    #                 db.session.add(summary)
    #                 db.session.commit()


if __name__ == '__main__':
    app = create_app()
    db_app = SQLAlchemy(app)
    init_database(db_app)
    # init_dataset(db_app)
    # init_summary(db_app)
