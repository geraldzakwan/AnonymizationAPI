#Script to migrate corpus to DB

import sys
import nltk
import MySQLdb

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
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

if(len(sys.argv) < 2):
    sys.exit('Supply corpus index')

db = MySQLdb.connect(
                        host="localhost",   # your host, usually localhost
                        user="root",        # your username
                        passwd="",          # your password
                        db="english_corpus" # name of the data base
                    )

comma = ", "
quote = '"'
cur = db.cursor()

def remove_quote(word):
    if(word[0] == "'"):
        word = word[1:len(word)-1]
    return word

if(sys.argv[1] == '1'):
    # print(nltk.corpus.conll2002.fileids())
    # ['esp.testa', 'esp.testb', 'esp.train', 'ned.testa', 'ned.testb', 'ned.train']

    train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))
    test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))
    it = 0
    query_error_list = []

    for doc in train_sents:
        for chunk in doc:
            # word = chunk[0]
            # pos_tag = chunk[1]
            # ner = chunk[2]
            #
            # word = remove_quote(word)
            # query = "INSERT INTO ner_annotated_corpus_conll2002_esp (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
            # try:
            #     cur.execute(query)
            #     db.commit()
            # except:
            #     query_error_list.append(query)
            #     db.rollback()

            it = it + 1
            print(it)


    # print('--------------')
    # print('--------------')
    # print('--------------')
    # for query_error in query_error_list:
    #     print(query_error)
    #
    # print('Cannot be printed to ext file')
    # print('--------------')
    # print('--------------')
    # print('--------------')
    # thefile = open('query_error_list_conll2002_esp.txt', 'w')
    # for item in query_error_list:
    #     try:
    #         thefile.write("%s\n" % item)
    #     except:
    #         print(item)
    #
    # db.close()

elif(sys.argv[1] == '2'):
    train_sents = list(nltk.corpus.conll2002.iob_sents('ned.train'))
    test_sents = list(nltk.corpus.conll2002.iob_sents('ned.testb'))
    it = 0
    query_error_list = []

    for doc in train_sents:
        for chunk in doc:
            # word = chunk[0]
            # pos_tag = chunk[1]
            # ner = chunk[2]
            #
            # word = remove_quote(word)
            # # query = "INSERT INTO ner_annotated_corpus_conll2002_ned (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
            # query = "INSERT INTO ner_annotated_corpus_conll2002_ned_2 (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
            # try:
            #     cur.execute(query)
            #     db.commit()
            # except:
            #     query_error_list.append(query)
            #     db.rollback()

            it = it + 1
            print(it)

    # print('--------------')
    # print('--------------')
    # print('--------------')
    # for query_error in query_error_list:
    #     print(query_error)
    #
    # print('Cannot be printed to ext file')
    # print('--------------')
    # print('--------------')
    # print('--------------')
    # thefile = open('query_error_list_conll2002_ned.txt', 'w')
    # for item in query_error_list:
    #     try:
    #         thefile.write("%s\n" % item)
    #     except:
    #         print(item)
    #
    # db.close()

elif(sys.argv[1] == '3'):
    # print(nltk.corpus.ieer.fileids())
    it = 0
    query_error_list = []
    for docs_name in nltk.corpus.ieer.fileids():
        documents = nltk.corpus.ieer.parsed_docs(docs_name)
        sentence = ""
        sentence_list = []
        for docs in documents:
            for items in docs.text:
                end_of_sentence = False

                if(type(items) == nltk.tree.Tree):
                    # word = str(items[0]) + ' - ' + str(items.label())
                    word = str(items[0])
                elif(type(items) == unicode):
                    word = str(items)
                    if(word.find('.') != -1):
                        end_of_sentence = True

                sentence = sentence + word + " "
                if(end_of_sentence):
                    sentence = sentence[:len(sentence)-1]
                    sentence_list.append(sentence)

                    text = nltk.word_tokenize(sentence)
                    pos_tagged_sentence = nltk.pos_tag(text)
                    ne_chunked_sentence = nltk.ne_chunk(pos_tagged_sentence)

                    for words in ne_chunked_sentence:
                        word = None
                        pos_tag = None
                        ner = None

                        it = it + 1
                        print(it)
                        if(type(words) == nltk.tree.Tree):
                            word = words[0][0]
                            pos_tag = words[0][1]
                            ner = words.label()
                            # print(words.label(), words[0][0], words[0][1])
                        else:
                            word = words[0]
                            pos_tag = words[1]
                            ner = 'O'
                            # print(words[0], words[1])

                        # word = remove_quote(word)
                        # query = "INSERT INTO ner_annotated_corpus_ieer (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ");";
                        # print(query)
                        # try:
                        #     cur.execute(query)
                        #     db.commit()
                        # except:
                        #     query_error_list.append(query)
                        #     db.rollback()

                    # print(ne_chunked_sentence)
                    # print(pos_tagged_sentence)
                    # print(sentence)
                    print('----------------')
                    sentence = ""

    print('--------------')
    print('--------------')
    print('--------------')
    for query_error in query_error_list:
        print(query_error)

    print('Cannot be printed to ext file')
    print('--------------')
    print('--------------')
    print('--------------')
    thefile = open('query_error_list_ieer.txt', 'w')
    for item in query_error_list:
        try:
            thefile.write("%s\n" % item)
        except:
            print(item)

    db.close()

    # Harus kumpulin per sentence (per titik)
    # pos_tag in pake nltk automatic tag
    # baru masukin ke db
    db.close()
else:
    print('Not defined')
