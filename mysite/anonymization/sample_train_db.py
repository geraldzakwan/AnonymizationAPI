import matplotlib.pyplot as plt
plt.style.use('ggplot')

from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import cPickle
import MySQLdb
import db_cfg
import sys

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(1)]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

db = MySQLdb.connect (
    host = db_cfg.mysql_local['host'],
    user = db_cfg.mysql_local['user'],
    passwd = db_cfg.mysql_local['passwd'],
    db = db_cfg.mysql_local['db']
)

cur = db.cursor()

cur.execute('SELECT * FROM ner_annotated_corpus_conll2002_esp')

train_sents = []

for row in cur.fetchall():
    train_sents.append(row)

db.close()

# for items in train_sents:
#     print(items)

# Ini doang yg perlu diganti
train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))
# for items in train_sents:
#     print(type(items[0]))
#     print('------------------')
test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))

X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]

X_test = [sent2features(s) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents]

if(True):
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    # Save model
    with open(sys.argv[1], 'wb') as fid:
        cPickle.dump(crf, fid)

    print('Accuration:')
    y_pred = crf.predict(X_test)
    print(metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=labels))
    print('-----------------')
    print('-----------------')
    print()
    print()

else:
    with open('saved_model_CRF.pkl', 'rb') as fid:
        crf = cPickle.load(fid)
