#%%
import pandas as pd
import json
import pickle
from backend.models import Document
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy
app = create_app()
db = SQLAlchemy(app)
results = db.session.query(Document).all()
results = pickle.load(open('/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/DB_BackUp/document.pickle', 'rb'))
#%%
for result in results:
    true_doc = db.session.query(Document).filter_by(id=result.id).first()
    true_doc.doc_json = result.doc_json
    db.session.commit()
