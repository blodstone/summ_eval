#%%
"""
Extract results from database and then perform analysis on top of to draw insights
"""
import json

import pandas as pd
from flask_sqlalchemy import SQLAlchemy

from backend.models import Dataset, Document, Summary, SummaryGroup
from backend.app import create_app

#%%
# Loading data from database
summary_name = 'BBC_system_tconvs2s'
app = create_app()
db = SQLAlchemy(app)
results_dir = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/results'
q_results = db.session.query(Summary, SummaryGroup, Document, Dataset) \
    .join(Document).join(SummaryGroup).join(Dataset) \
    .filter(Dataset.name == 'BBC', SummaryGroup.name == summary_name).all()
#%%
# Process data from database into components and components' type
def parse(doc_json):
    """
    Parse document into components (list of all tokens) and comp_types (list of types for all tokens)
    """
    components = []
    comp_types = []
    index = []
    for sent in doc_json['sentences']:
        for idx, token in enumerate(sent['tokens']):
            aWord = token['word'].lower()
            if token['word'] == '-LRB-':
                aWord = '('
            elif token['word'] == '-RRB-':
                aWord = ')'
            elif token['word'] == '``':
                aWord = '"'
            elif token['word'] == '\'\'':
                aWord = '"'
            components.append(aWord)
            if aWord.strip() == '':
                comp_types.append('whitespace')
            else:
                comp_types.append('word')
            index.append(len(index))
            if idx != len(sent['tokens']) - 2:
                components.append(' ')
                comp_types.append('whitespace')
                index.append(len(index))
    data = {
        'content': pd.Series(components),
        'type': pd.Series(comp_types),
        'index': pd.Series(index),
    }
    return pd.DataFrame(data)

df_doc_prop = pd.DataFrame([])

summary = []
doc_id = []
for summ, _, doc, _ in q_results:
    doc_json = json.loads(doc.doc_json)
    df_doc_prop = df_doc_prop.append(parse(doc_json).assign(doc_id=doc_json['doc_id']))
    summary.append(summ.text.split())
    doc_id.append(doc.doc_id)
df_doc = pd.DataFrame(df_doc_prop[df_doc_prop['type'] != 'whitespace'].groupby('doc_id').count())
df_doc = df_doc.assign(word_len=lambda x: x.content).drop(columns=['type', 'content'])
df_summ = pd.DataFrame({
    'doc_id': pd.Series(doc_id),
    'summ': pd.Series(summary)
})
df_summ.index = df_summ['doc_id']
df_doc = df_doc.join(df_summ, lsuffix='_df_doc', rsuffix='_df_summ')
#%%
# Retrieve highlights
def process_doc(results):
    """
    Build indexes and texts for the given document
    """
    indexes = []
    texts = []
    for result_id, data in results.items():
        for h_id, highlight in data['highlights'].items():
            if highlight['text'] == '':
                continue
            indexes.append(highlight['indexes'])
            texts.append(highlight['text'].lower())
    data = {'indexes': pd.Series(indexes), 'text': pd.Series(texts)}
    return pd.DataFrame(data)

df_h = pd.DataFrame([])
for summ, _, doc, _ in q_results:
    doc_json = json.loads(doc.doc_json)
    df_h = df_h.append(process_doc(doc_json['results']).assign(doc_id=doc_json['doc_id']))

#%%
# Calculate word overlap ratio between document and highlights
from itertools import chain

df_doc = df_doc.assign(doc_text=lambda x: df_doc_prop[df_doc_prop['type'] == 'word'].groupby('doc_id')['content'].apply(list))
df_doc = df_doc.assign(h_idxs=lambda x: df_h.groupby('doc_id').apply(lambda x: list(set(chain(*x.indexes)))))

df_doc = df_doc.assign(doc_idxs=lambda x: df_doc_prop[df_doc_prop['type']=='word'].groupby('doc_id')['index'].apply(list))

df_doc = df_doc.assign(h_len=lambda x: df_doc[['h_idxs']].apply(lambda x: len(x['h_idxs']), axis=1))

df_doc = df_doc.assign(
    doc_h_overlap=lambda x: df_doc[['h_idxs', 'doc_idxs']]
        .apply(lambda x: set(x['doc_idxs']) & set(x['h_idxs']), axis=1)
        .apply(lambda x: len(list(x))))

df_doc = df_doc.assign(
    doc_h_overlap_recall=lambda x: df_doc.doc_h_overlap/df_doc.word_len)

df_doc = df_doc.assign(
    doc_h_overlap_precision=lambda x: df_doc.doc_h_overlap/df_doc.h_len)

df_doc = df_doc.assign(
    doc_h_overlap_F1=lambda x: 2*df_doc.doc_h_overlap_recall*df_doc.doc_h_overlap_precision/(df_doc.doc_h_overlap_recall+df_doc.doc_h_overlap_precision))
#%%
# Calculate word overlap ratio between summary and highlights

df_doc = df_doc.assign(h_text=lambda x: df_h.groupby('doc_id').apply(lambda x: ' '.join(x.text).split()))

from nltk.util import ngrams
for i in range(1, 4):
    kwargs_1 = {
        'summ_h_%s_gram' % i: lambda x: df_doc[['summ', 'h_text']].apply(
        lambda x: set(ngrams(x['h_text'], i)) & set(ngrams(x['summ'], i)), axis=1).apply(lambda x: len(list(x)))
    }
    kwargs_2 = {
        'summ_h_overlap_%s_gram_recall' % i: lambda x: df_doc[['h_text', 'summ_h_%s_gram' % i]].apply(lambda x: x['summ_h_%s_gram' % i] / len(list(set(ngrams(x['h_text'], i)))), axis=1)
    }
    kwargs_3 = {
        'summ_h_overlap_%s_gram_precision' % i: lambda x: df_doc[['summ', 'summ_h_%s_gram' % i]].apply(
            lambda x: x['summ_h_%s_gram' % i] / len(list(set(ngrams(x['summ'], i)))), axis=1)
    }
    kwargs_4 = {
        'summ_h_overlap_%s_gram_F1' % i: lambda x: 2*df_doc['summ_h_overlap_%s_gram_precision' % i]*df_doc['summ_h_overlap_%s_gram_recall' % i]/(df_doc['summ_h_overlap_%s_gram_precision' % i]+df_doc['summ_h_overlap_%s_gram_recall' % i])
    }
    df_doc = df_doc.assign(**kwargs_1)
    df_doc = df_doc.assign(**kwargs_2)
    df_doc = df_doc.assign(**kwargs_3)
    df_doc = df_doc.fillna(0)
    df_doc = df_doc.assign(**kwargs_4)
    df_doc = df_doc.fillna(0)
#%%
# Calculate word overlap ratio between summary and doc
for i in range(1, 4):
    kwargs_1 = {
        'summ_doc_%s_gram' % i: lambda x: df_doc[['summ', 'doc_text']].apply(
        lambda x: set(ngrams(x['doc_text'], i)) & set(ngrams(x['summ'], i)), axis=1).apply(lambda x: len(list(x)))
    }
    kwargs_2 = {
        'summ_doc_overlap_%s_gram_recall' % i: lambda x: df_doc[['doc_text', 'summ_doc_%s_gram' % i]].apply(lambda x: x['summ_doc_%s_gram' % i] / len(list(set(ngrams(x['doc_text'], i)))), axis=1)
    }
    kwargs_3 = {
        'summ_doc_overlap_%s_gram_precision' % i: lambda x: df_doc[['summ', 'summ_doc_%s_gram' % i]].apply(
            lambda x: x['summ_doc_%s_gram' % i] / len(list(set(ngrams(x['summ'], i)))), axis=1)
    }
    kwargs_4 = {
        'summ_doc_overlap_%s_gram_F1' % i: lambda x: 2*df_doc['summ_doc_overlap_%s_gram_precision' % i]*df_doc['summ_doc_overlap_%s_gram_recall' % i]/(df_doc['summ_doc_overlap_%s_gram_precision' % i]+df_doc['summ_doc_overlap_%s_gram_recall' % i])
    }
    df_doc = df_doc.assign(**kwargs_1)
    df_doc = df_doc.assign(**kwargs_2)
    df_doc = df_doc.assign(**kwargs_3)
    df_doc = df_doc.fillna(0)
    df_doc = df_doc.assign(**kwargs_4)
    df_doc = df_doc.fillna(0)

#%%
# Saving result to csv files
import numpy as np
import os

result_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/results'

df_doc.to_csv(os.path.join(result_path, '%s_df_doc.csv' % summary_name))

df_result = pd.DataFrame(df_doc.describe(include=[np.number]))
df_result.to_csv(os.path.join(result_path, '%s_df_result.csv' % summary_name))
