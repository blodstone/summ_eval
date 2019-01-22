from nltk.util import ngrams
from itertools import chain
import pandas as pd

MAX_LEN = 30
df_ngrams = pd.DataFrame([])


def numH(w, H):
    result = 0
    for h in H:
        h_words = list(chain(*[x.split() for x in h]))
        if w in h_words:
            result += len(h_words) / MAX_LEN
    return result


def beta(n, g, w, H):
    numerator = 0
    denominator = 0
    m = len(w)
    for i in range(m-n+1):
        total_NumH = 0
        for j in range(i, i+n):
            if w[i:i+n] == list(g):
                total_NumH += numH(w[j], H)
        total_NumH /= 10
        total_NumH /= n
        numerator += total_NumH
    for i in range(m-n+1):
        if w[i:i+n] == list(g):
            denominator += 1
    return numerator/denominator


def R_rec(n, S, D, H):
    n_gram_D = list(ngrams(D, n))
    n_gram_S = list(ngrams(S, n))

    numerator = 0
    for g in n_gram_S:
        if g in n_gram_D:
            numerator += beta(n, g, D, H)
    denominator = 0
    for g in n_gram_D:
        denominator += beta(n, g, D, H)
    return numerator/denominator

doc = 'a b c b'

H = [
    ['a b', 'c', 'b'],
    ['a', 'b'],
    ['a', 'b c']
]

summ = 'a b d'

recs = []
doc_ids = []
test_num = 0
doc_texts = doc.split()
rec = R_rec(2, summ.split(), doc_texts, H)
print(rec)