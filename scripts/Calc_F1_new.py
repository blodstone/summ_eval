#%%
import os

import pandas as pd
from flask_sqlalchemy import SQLAlchemy

from backend.models import Dataset, Document, Summary, \
    SummaryGroup, EvaluationResult, SummaryStatus, EvaluationProject
from backend.app import create_app

#%%
# Loading data from database

# proj_name = 'Inf Doc Highlight TConvs2s'
# proj_name = 'Inf Doc Highlight PTGen'
# proj_name = 'Inf Doc Highlight Ref'
# proj_name = 'Inf Doc No Highlight TConvs2s'
# proj_name = 'Inf Doc No Highlight PTGen'
# proj_name = 'Inf Doc No Highlight Ref'
# proj_name = 'Inf Ref TConvs2s'
proj_name = 'Inf Ref PTGen'

app = create_app()
db = SQLAlchemy(app)
results_dir = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/results'
q_results = db.session.query(EvaluationResult, SummaryStatus, Summary, EvaluationProject, Document)\
    .join(SummaryStatus).join(EvaluationProject).join(Summary).join(Document)\
    .filter(EvaluationProject.name == proj_name).all()
precs = []
recalls = []
f_1s = []
data = {}
for result, _, _, _, doc in q_results:
    precs.append(result.prec)
    recalls.append(result.recall)
    f_1s.append((result.prec*result.recall)/(0.5*result.prec+0.5*result.recall))
data = {
    'precision': pd.Series(precs),
    'recall': pd.Series(recalls),
    'f1': pd.Series(f_1s),
}
df_result = pd.DataFrame(data)
df_result.describe().to_csv(os.path.join(results_dir, '%s_result.csv' % proj_name))
