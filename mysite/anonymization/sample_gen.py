import sys
from nltk import wordnet as wn

# If you are using nltk version 3.0.1, the following will tell you all the synsets for "green" and will thenn find all of their hypernyms. If you're running nltk 3.0.0, you can change the first line to `for synset in wn.synsets('bank'):
for synset in wn.wordnet.synsets(sys.argv[1]):
    for hypernym in synset.hypernyms():
        print synset, hypernym
