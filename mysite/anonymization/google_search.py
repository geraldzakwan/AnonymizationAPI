# Reference:
# https://github.com/google/google-api-python-client/blob/master/samples/customsearch/main.py

import sys
import random
from apiclient.discovery import build

# api_key = 'AIzaSyDkSCA8agvst49gtKEjrxRnI57lCqV9vBM'
api_key = 'AIzaSyBB6XFgrejB0CwyDzbKPnabx62tcJQY_-k'
cx_key = '013692161269702497108:vgnkfyixhmo'

def get_total_results(word):
    service = build("customsearch", "v1", developerKey=api_key)

    res = service.cse().list(q=word, cx=cx_key,).execute()

    total_results = float(res['queries']['request'][0]['totalResults'])

    return total_results

def co_occurence(word1, word2):
    and_total_results = get_total_results(word1 + " AND " + word2)
    or_total_results = get_total_results(word1 + " OR " + word2)
    ret = and_total_results/or_total_results
    # ret = random.random()

    print('-----')
    print(word1, word2)
    print(ret)
    print('-----')
    print(and_total_results)
    print(or_total_results)

    return ret

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        sys.exit('Supply first word and second word')
    print(co_occurence(sys.argv[1], sys.argv[2]))


# from itertools import chain
#
# import nltk
# import sklearn
# import scipy.stats
# from sklearn.metrics import make_scorer
# from sklearn.cross_validation import cross_val_score
# from sklearn.grid_search import RandomizedSearchCV
#
# import sklearn_crfsuite
# from sklearn_crfsuite import scorers
# from sklearn_crfsuite import metrics
#
# def word2features(sent, i):
#     word = sent[i][0]
#     postag = sent[i][1]
#
#     features = {
#         'bias': 1.0,
#         'word.lower()': word.lower(),
#         'word[-3:]': word[-3:],
#         'word[-2:]': word[-2:],
#         'word.isupper()': word.isupper(),
#         'word.istitle()': word.istitle(),
#         'word.isdigit()': word.isdigit(),
#         'postag': postag,
#         'postag[:2]': postag[:2],
#     }
#     if i > 0:
#         word1 = sent[i-1][0]
#         postag1 = sent[i-1][1]
#         features.update({
#             '-1:word.lower()': word1.lower(),
#             '-1:word.istitle()': word1.istitle(),
#             '-1:word.isupper()': word1.isupper(),
#             '-1:postag': postag1,
#             '-1:postag[:2]': postag1[:2],
#         })
#     else:
#         features['BOS'] = True
#
#     if i < len(sent)-1:
#         word1 = sent[i+1][0]
#         postag1 = sent[i+1][1]
#         features.update({
#             '+1:word.lower()': word1.lower(),
#             '+1:word.istitle()': word1.istitle(),
#             '+1:word.isupper()': word1.isupper(),
#             '+1:postag': postag1,
#             '+1:postag[:2]': postag1[:2],
#         })
#     else:
#         features['EOS'] = True
#
#     return features
#
#
# def sent2features(sent):
#     return [word2features(sent, i) for i in range(len(sent))]
#
# def sent2labels(sent):
#     return [label for token, postag, label in sent]
#
# def sent2tokens(sent):
#     return [token for token, postag, label in sent]
#
# print(nltk.corpus.conll2002.fileids())
# # ['esp.testa', 'esp.testb', 'esp.train', 'ned.testa', 'ned.testb', 'ned.train']
#
# train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))
# test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))
#
# print('Sample sentences:')
# print(train_sents[0])
# print('-----------------')
# print('-----------------')
# print()
# print()
#
# print('Feature extractions:')
# print(sent2features(train_sents[0])[0])
# print('-----------------')
# print('-----------------')
# print()
# print()
#
# X_train = [sent2features(s) for s in train_sents]
# y_train = [sent2labels(s) for s in train_sents]
#
# X_test = [sent2features(s) for s in test_sents]
# y_test = [sent2labels(s) for s in test_sents]
#
# crf = sklearn_crfsuite.CRF(
#     algorithm='lbfgs',
#     c1=0.1,
#     c2=0.1,
#     max_iterations=100,
#     all_possible_transitions=True
# )
# crf.fit(X_train, y_train)
#
# print('Labels:')
# labels = list(crf.classes_)
# labels.remove('O')
# print(labels)
# print('-----------------')
# print('-----------------')
# print()
# print()
#
# print('Accuration:')
# y_pred = crf.predict(X_test)
# print(metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=labels))
# print('-----------------')
# print('-----------------')
# print()
# print()
#
# print('Confusion matrix:')
# # group B and I results
# sorted_labels = sorted(
#     labels,
#     key=lambda name: (name[1:], name[0])
# )
# print(metrics.flat_classification_report(
#     y_test, y_pred, labels=sorted_labels, digits=3
# ))
# print('-----------------')
# print('-----------------')
# print()
# print()
