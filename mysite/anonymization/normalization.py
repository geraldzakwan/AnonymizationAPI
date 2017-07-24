from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import tag_converter

stemmer = SnowballStemmer('english')
# stemmer = PorterStemmer()
# stemmer = LancasterStemmer()
stemmer.stem('maximum')

wordnet_lemmatizer = WordNetLemmatizer()

def stem_list_of_token(ner_prediction):
    stemmed_list_of_token = []

    for token_tuple in ner_prediction:
        if(token_tuple[1] == 'O'):
            stemmed_token = stemmer.stem(token_tuple[0])
        else:
            stemmed_token = token_tuple[0]

        stemmed_list_of_token.append((stemmed_token, token_tuple[1]))

    return stemmed_list_of_token

def lemmatize_list_of_token(ner_prediction, pos_tagged_list):
    lemmatized_list_of_token = []

    # print(ner_prediction)
    # print(pos_tagged_list)

    i = 0
    for token_tuple in ner_prediction:
        if(token_tuple[1] == 'O'):
            tag = tag_converter.penn_to_wn(pos_tagged_list[i])
            lemmatized_token = wordnet_lemmatizer.lemmatize(token_tuple[0], pos=tag)
            # print(pos_tag_list[i], tag, lemmatized_token)
        else:
            lemmatized_token = token_tuple[0]
        i = i + 1

        # print('Add lemmatized:')
        # print(lemmatized_token, postoken_tuple[1])

        lemmatized_list_of_token.append((lemmatized_token, token_tuple[1]))

    return lemmatized_list_of_token

def stem_list_of_token_awal(pos_tagged_list):
    stemmed_list_of_token = []

    # print(pos_tagged_list)

    for token_tuple in pos_tagged_list:
        if(token_tuple[1] != 'NNP'):
            # tag = tag = tag_converter.penn_to_wn(token_tuple[1])
            stemmed_token = stemmer.stem(token_tuple[0])
            # print(stemmed_token)
        else:
            stemmed_token = token_tuple[0]

        stemmed_list_of_token.append((stemmed_token, token_tuple[1]))

    return stemmed_list_of_token

def lemmatize_list_of_token_awal(pos_tagged_list):
    lemmatized_list_of_token = []

    # print(pos_tagged_list)

    i = 0
    for token_tuple in pos_tagged_list:
        if(token_tuple[1] != 'NNP'):
            tag = tag_converter.penn_to_wn(token_tuple[1])
            lemmatized_token = wordnet_lemmatizer.lemmatize(token_tuple[0], pos=tag)
            # print(token_tuple[1], tag, lemmatized_token)
        else:
            lemmatized_token = token_tuple[0]
        i = i + 1

        # print('Add lemmatized:')
        # print(lemmatized_token, postoken_tuple[1])

        lemmatized_list_of_token.append((lemmatized_token, token_tuple[1]))

    return lemmatized_list_of_token
