import MySQLdb
import os
import sys
import collections
from nltk import conlltags2tree

db = MySQLdb.connect(
                        host="localhost",   # your host, usually localhost
                        user="root",        # your username
                        passwd="",          # your password
                        db="english_corpus" # name of the data base
                    )

comma = ", "
quote = "'"
cur = db.cursor()

def remove_quote(word):
    if(word[0] == "'"):
        word = word[1:len(word)-1]
    return word

def to_conll_iob(annotated_sentence):
    """
    `annotated_sentence` = list of triplets [(w1, t1, iob1), ...]
    Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
    to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
    """
    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token

        if ner != 'O':
            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][2] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append((tag, word, ner))
    return proper_iob_tokens

def migrate_gmb_corpus():
    corpus_root = 'gmb-2.2.0'
    it = 0
    query_error_list = []

    #Iterate through all the files
    for root, dirs, files in os.walk(corpus_root):
        # if (exit):
        #     break;
        for filename in files:
            # if (exit):
            #     break;
            # Only process tag file
            if filename.endswith("en.tags"):

                # Open the full path
                with open(os.path.join(root, filename), 'rb') as file_handle:
                    # Decode file content
                    file_content = file_handle.read().decode('utf-8').strip()

                    # Split sentences, sentences are separated with two newline characters
                    annotated_sentences = file_content.split('\n\n')

                    # Iterate through sentences
                    for annotated_sentence in annotated_sentences:

                        # Split words, words are separated with a newline character
                        annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]

                        standard_form_tokens = []

                        for idx, annotated_token in enumerate(annotated_tokens):
                            # Split annotations, annotations are separated with a tab character
                            annotations = annotated_token.split('\t')

                            # The 1st annotation is the word itself, the 2nd is pos_tag, and the 3rd is it's named entity
                            word, pos_tag, ner = annotations[0], annotations[1], annotations[3]

                            # Get only the primary category
                            if ner != 'O':
                                ner = ner.split('-')[0]

                            standard_form_tokens.append((word, pos_tag, ner))

                            word = remove_quote(word)
                            query = "INSERT INTO ner_annotated_corpus (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
                            # print(query)
                            # cur.execute(query)
                            it = it + 1
                            try:
                                cur.execute(query)
                                db.commit()
                            except:
                                query_error_list.append(query)
                                db.rollback()

                        conll_tokens = to_conll_iob(standard_form_tokens)

                        # Debugging
                        # it = it + 1
                        print(it)
                        # print('-------------------')
                        # for item in conlltags2tree(conll_tokens):
                        #     print(item)
                        # print('-------------------')

    # db.commit()
    # db.close()
    return query_error_list

if __name__ == "__main__":
    print('Migrate module')

    query_error_list = migrate_gmb_corpus()

    for query_error in query_error_list:
        print(query_error_list)
        print('--------------')

    thefile = open('query_error_list.txt', 'w')
    for item in query_error_list:
        thefile.write("%s\n" % item)
