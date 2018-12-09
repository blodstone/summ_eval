from backend.models import EvaluationResult, SummaryGroup, SummaryStatus, Summary, EvaluationProject
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy
from scripts.Krippendorff import krippendorff_alpha, interval_metric, ratio_metric

def calc(db):
    results = db.session.query(EvaluationResult).all()
    precision = {}
    recall = {}
    precision_coders = {}
    recall_coders = {}
    for result in results:
        summ_status = db.session.query(SummaryStatus).get(result.status_id)
        project = db.session.query(EvaluationProject).get(summ_status.proj_id)
        summ = db.session.query(Summary).get(summ_status.summary_id)
        summ_group = db.session.query(SummaryGroup).get(summ.summary_group_id)
        name = '%s_%s' % (summ_group.name, project.highlight)
        if name not in precision:
            precision[name] = {
                'total': 0,
                'count': 0,
                'average': 0.0,
                'value': {},
                'doc_id': '',
            }
        precision[name]['total'] += result.precision
        precision[name]['count'] += 1
        precision[name]['average'] = precision[name]['total']/ \
                                     precision[name]['count']
        if summ.doc_id not in precision[name]['value']:
            precision[name]['value'][summ.doc_id] = []
        precision[name]['value'][summ.doc_id].append(result.precision)

        if name not in recall:
            recall[name] = {
                'total': 0,
                'count': 0,
                'average': 0.0,
                'value': {},
                'doc_id': '',
            }
        recall[name]['total'] += result.recall
        recall[name]['count'] += 1
        recall[name]['average'] = recall[name]['total']/ \
                                  recall[name]['count']
        if summ.doc_id not in recall[name]['value']:
            recall[name]['value'][summ.doc_id] = []
        recall[name]['value'][summ.doc_id].append(result.recall)

    for group_name, data in precision.items():
        coders = []
        for doc_id, n_value in data['value'].items():
            all_docs = data['value'].keys()
            for idx, value in enumerate(n_value):
                docs = {}
                docs[doc_id] = value
                for d in all_docs:
                    if d != doc_id:
                        docs[d] = '*'
                coders.append(docs)
        precision_coders[group_name] = coders
    # print(precision_coders)
    # print(precision)
    # for group_name, data in precision_coders.items():
    #     pass
    #     # print(precision_coders[group_name])
    #     print(group_name)
    #     print("interval metric: %.3f" % krippendorff_alpha(precision_coders[group_name], interval_metric, missing_items='*'))
    #     print('Average: ' + str(precision[group_name]['average']))

    for group_name, data in recall.items():
        coders = []
        for doc_id, n_value in data['value'].items():
            all_docs = data['value'].keys()
            # print(len(n_value))
            for idx, value in enumerate(n_value):
                docs = {}
                docs[doc_id] = value
                for d in all_docs:
                    if d != doc_id:
                        docs[d] = '*'
                coders.append(docs)
        recall_coders[group_name] = coders
    # print(recall_coders)
    # print(recall)
    print('RECALL')
    for group_name, data in recall_coders.items():
        pass
        # print(recall_coders[group_name])
        print(group_name)
        print("interval metric: %.3f" %
              krippendorff_alpha(recall_coders[group_name], interval_metric, missing_items='*'))
        print('Average: ' + str(recall[group_name]['average']))
    # for group_name, data in recall.items():
    #     print(group_name)
    #     print(recall[group_name]['value'])
    # for group_name, data in precision.items():
    #     print(group_name)
    #     print(precision[group_name]['value'])


if __name__ == '__main__':
    app = create_app()
    db_app = SQLAlchemy(app)
    calc(db_app)
