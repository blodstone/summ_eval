import os
import pandas as pd
import json

from backend.models import EvaluationResult, SummaryStatus, Summary, Document
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy

if __name__ == '__main__':
    app = create_app()
    db = SQLAlchemy(app)
    file_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/mturk/working/Batch_3494982_batch_results.csv'
    df = pd.read_csv(file_path, delimiter=',')

    for i in df.index:
        code = df['Answer.surveycode'][i]
        result = db.session\
            .query(EvaluationResult, SummaryStatus, Summary, Document) \
            .join(SummaryStatus) \
            .join(Summary) \
            .join(Document) \
            .filter(
            EvaluationResult.mturk_code.like('%' + code + '%')).first()
        if result:
            validity = result[0].validity
            if validity:
               feedback = ''
            else:
                feedback = 'Sorry, but you gave the wrong answer to the statement "%s". The correct answer is %s' % (result[3].sanity_statement, result[3].sanity_answer)
            if result[0].prec == 50.0 and result[0].recall == 50.0:
                validity = False
                feedback = 'You did not touch the precision and recall slider at all.'
            if validity:
                df['Approve'][i] = 'x'
            else:
                df['Reject'][i] = feedback
    df.to_csv(file_path, header=df.columns.values)
