import itertools

from nltk import tree2conlltags
from nltk.chunk import ChunkParserI
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from nltk.chunk import conlltags2tree, tree2conlltags

from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB

batch_size_per_iter = 1000

class NamedEntityChunker(ChunkParserI):

    @classmethod
    def to_dataset(cls, parsed_sentences, feature_detector):
        """
        Transform a list of tagged sentences into a scikit-learn compatible POS dataset
        :param parsed_sentences:
        :param feature_detector:
        :return:
        """
        X, y = [], []
        for parsed in parsed_sentences:
            iob_tagged = tree2conlltags(parsed)
            words, tags, iob_tags = zip(*iob_tagged)

            tagged = zip(words, tags)

            for index in range(len(iob_tagged)):
                X.append(feature_detector(tagged, index, history=iob_tags[:index]))
                y.append(iob_tags[index])

        return X, y

    @classmethod
    def get_minibatch(cls, parsed_sentences, feature_detector, batch_size=batch_size_per_iter):
        batch = list(itertools.islice(parsed_sentences, batch_size))
        X, y = cls.to_dataset(batch, feature_detector)
        return X, y

    @classmethod
    def load(cls, model_name, feature_detector, **kwargs):
        clf = joblib.load(model_name)
        return cls(clf, feature_detector)

    @classmethod
    def train(cls, parsed_sentences, feature_detector, all_classes, filename, **kwargs):
        X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', batch_size_per_iter))
        vectorizer = DictVectorizer(sparse=False)
        vectorizer.fit(X)

        clf = Perceptron(verbose=10, n_jobs=-1, n_iter=kwargs.get('n_iter', 5))

        while len(X):
            X = vectorizer.transform(X)
            clf.partial_fit(X, y, all_classes)
            X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', batch_size_per_iter))

        clf = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', clf)
        ])

        joblib.dump(clf, filename)

        return cls(clf, feature_detector)

    @classmethod
    def train_naive_bayes(cls, parsed_sentences, feature_detector, all_classes, filename, **kwargs):
        X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', batch_size_per_iter))
        vectorizer = DictVectorizer(sparse=False)
        vectorizer.fit(X)

        clf = MultinomialNB()

        while len(X):
            X = vectorizer.transform(X)
            clf.partial_fit(X, y, all_classes)
            X, y = cls.get_minibatch(parsed_sentences, feature_detector, kwargs.get('batch_size', batch_size_per_iter))

        clf = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', clf)
        ])

        joblib.dump(clf, filename)

        return cls(clf, feature_detector)

    def __init__(self, classifier, feature_detector):
        self._classifier = classifier
        self._feature_detector = feature_detector

    def parse(self, tokens):
        """
        Chunk a tagged sentence
        :param tokens: List of words [(w1, t1), (w2, t2), ...]
        :return: chunked sentence: nltk.Tree
        """
        history = []
        iob_tagged_tokens = []
        for index, (word, tag) in enumerate(tokens):
            iob_tag = self._classifier.predict([self._feature_detector(tokens, index, history)])[0]
            history.append(iob_tag)
            iob_tagged_tokens.append((word, tag, iob_tag))

        return conlltags2tree(iob_tagged_tokens)

    def score(self, parsed_sentences):
        """
        Compute the accuracy of the tagger for a list of test sentences
        :param parsed_sentences: List of parsed sentences: nltk.Tree
        :return: float 0.0 - 1.0
        """
        X_test, y_test = self.__class__.to_dataset(parsed_sentences, self._feature_detector)
        return self._classifier.score(X_test, y_test)

if __name__ == "__main__":
    print('NE_Chunker module')
