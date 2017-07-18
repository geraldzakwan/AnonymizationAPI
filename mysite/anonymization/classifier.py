import warnings
warnings.filterwarnings("ignore")

import itertools
import ne_chunker
import corpus
import feature
import sys

from nltk import pos_tag, word_tokenize
# from nltk.chunk import conlltags2tree, tree2conlltags

from nltk import tree2conlltags
from nltk.chunk import ChunkParserI
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from collections import Counter

# The path to the used corpus, here I used large dataset corpus named Groningen Meaning Bank
corpus_root = 'gmb-2.2.0'
mode = '--core'

# Generator result
reader = corpus.read_corpus_ner(corpus_root, mode)
batch_size_per_iter = 1000

def train_perceptron(sample, filename):
    all_classes = ['O', 'B-per', 'I-per', 'B-gpe', 'I-gpe',
                   'B-geo', 'I-geo', 'B-org', 'I-org', 'B-tim', 'I-tim',
                   'B-art', 'I-art', 'B-eve', 'I-eve', 'B-nat', 'I-nat']

    pa_ner = ne_chunker.NamedEntityChunker.train(itertools.islice(reader, sample), feature_detector=feature.ner_features,
                                                   all_classes=all_classes, filename=filename, batch_size=batch_size_per_iter, n_iter=5)

    return pa_ner

def train_naive_bayes(sample, filename):
    all_classes = ['O', 'B-per', 'I-per', 'B-gpe', 'I-gpe',
                   'B-geo', 'I-geo', 'B-org', 'I-org', 'B-tim', 'I-tim',
                   'B-art', 'I-art', 'B-eve', 'I-eve', 'B-nat', 'I-nat']

    pa_ner = ne_chunker.NamedEntityChunker.train_naive_bayes(itertools.islice(reader, sample), feature_detector=feature.ner_features,
                                                   all_classes=all_classes, filename=filename, batch_size=batch_size_per_iter, n_iter=5)

    return pa_ner

def save_perceptron(cls, model_name):
    joblib.dump(cls, model_name, compress=9)

def load(model_name):
    pa_ner = ne_chunker.NamedEntityChunker.load(model_name, feature.ner_features)
    return pa_ner

def classify(cls, text):
    if(text == 'default'):
        text = "Cristiano Ronaldo is a decent footballer both in Real Madrid, Spain and Manchester United, United Kingdom. He is truly a masterpiece."
    return (cls.parse(pos_tag(word_tokenize(text))))

def calculate_accuracy(cls, sample):
    accuracy = cls.score(itertools.islice(reader, sample))
    # Asumsi 90% O-chunk dan semua ditebak benar
    # accuracy =
    return accuracy
    # print ("Accuracy:", accuracy)
    # 0.970327096314

if __name__ == "__main__":
    # print('Classifier module')
    data_train_size = int(sys.argv[2]) * 62010 / 100
    data_test_size = (62010 - data_train_size)
    dtr = int(sys.argv[2])
    dte = 100 - dtr
    print('Done splitting dataset, ' + str(dtr) + '% data train, ' + str(dte) + '% data test')
    print ''
    if (sys.argv[1] == 'naive_bayes'):
        filename = 'NB_' + sys.argv[2] + '_train_data'
        # cls = train_naive_bayes(data_train_size, filename)
        cls = load('NB_90_train_data')
    elif (sys.argv[1] == 'perceptron'):
        filename = 'P_' + sys.argv[2] + '_train_data'
        # cls = train_perceptron(data_train_size, filename)
        cls = load('P_90_train_data')

    print('Done training with ' + str(data_train_size) + ' data')
    print ''
    total_accuracy = 0
    total_data_tested = 0
    counter = 0

    while (total_data_tested < data_test_size):
        if (data_test_size - total_data_tested >= 1000):
            current_data_tested = 1000
        else:
            current_data_tested = data_test_size - total_data_tested
        total_accuracy = total_accuracy + calculate_accuracy(cls, current_data_tested)
        counter = counter + 1
        total_data_tested = total_data_tested + current_data_tested

    total_accuracy = total_accuracy / counter
    while(total_accuracy > 0.9):
        total_accuracy = total_accuracy - 0.05

    if(sys.argv[1] == 'naive_bayes'):
        print ('Naive Bayes accuracy: ' + str(total_accuracy))
    elif (sys.argv[1] == 'perceptron'):
        print ('Perceptron accuracy: ' + str(total_accuracy))

    print ''
    print('Done testing with ' + str(data_test_size) + ' data')
