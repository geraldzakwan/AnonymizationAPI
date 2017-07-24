# https://noisy-text.github.io/norm-shared-task.html

# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import warnings
warnings.filterwarnings("ignore")

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
import os
import sys

import fetch_user_profile
import google_search
import access_gmb_corpus
import feature_extraction
import anonymization
import postprocessing
import sentence_similarity
import sample_rule_based
import normalization
import spell_checker
import temporal_phrase_tagger

train_sents = access_gmb_corpus.read_corpus_ner('gmb-2.2.0', '--core')

total_data = len(train_sents)
train_data_size = int(sys.argv[1]) * total_data / 100

# Train sent is 90%, test sent is 10%
test_sents = train_sents[train_data_size:]
train_sents = train_sents[:train_data_size]
# print("Done splitting")

X_train = [feature_extraction.sent2features(s) for s in train_sents]
y_train = [feature_extraction.sent2labels(s) for s in train_sents]

X_test = [feature_extraction.sent2features(s) for s in test_sents]
y_test = [feature_extraction.sent2labels(s) for s in test_sents]
# print("Done sent2features")

if(sys.argv[2] == 'load'):
    load = True
else:
    load = False
filename = 'save_model_crf_gmb_proper_' + sys.argv[1] + '.pkl'

if(not load):
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=1000,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    # Save model
    with open(filename, 'wb') as fid:
        cPickle.dump(crf, fid)
else:
    with open(sys.argv[3], 'rb') as fid:
        crf = cPickle.load(fid)

labels = list(crf.classes_)
# labels.remove('O')

y_pred = crf.predict(X_test)

print ''
print('Accuration:')
print(metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=labels))
print ''
# print('-----------------')
# print('-----------------')

print('Confusion matrix:')
# group B and I results
sorted_labels = sorted(
    labels,
    key=lambda name: (name[1:], name[0])
)
print(metrics.flat_classification_report(
    y_test, y_pred, labels=sorted_labels, digits=3
))
# print('-----------------')
# print('-----------------')

# from collections import Counter
#
# def print_transitions(trans_features):
#     for (label_from, label_to), weight in trans_features:
#         print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))
#
# print("Likely transitions:")
# print_transitions(Counter(crf.transition_features_).most_common()[11:21])
# print ''
# print("Unlikely transitions:")
# print_transitions(Counter(crf.transition_features_).most_common()[-15:-6])
