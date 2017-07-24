# https://noisy-text.github.io/norm-shared-task.html

# import matplotlib.pyplot as plt
# plt.style.use('ggplot')

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
import collections

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
test_sents = access_gmb_corpus.read_corpus_ner('gmb-2.2.0', '--core')

X_train = [feature_extraction.sent2features(s) for s in train_sents]
y_train = [feature_extraction.sent2labels(s) for s in train_sents]

X_test = [feature_extraction.sent2features(s) for s in test_sents]
y_test = [feature_extraction.sent2labels(s) for s in test_sents]

load = True

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
    with open(sys.argv[1], 'wb') as fid:
        cPickle.dump(crf, fid)
else:
    with open(sys.argv[1], 'rb') as fid:
        crf = cPickle.load(fid)

# labels = list(crf.classes_)
# labels.remove('O')
#
# y_pred = crf.predict(X_test)

# print('Accuration:')
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

text_input = sys.argv[2]
tokenized_input = nltk.word_tokenize(text_input)

# Spell checking disini, tapi ternyata yang named entity ikut keubah jadi jangan
# tokenized_input = spell_checker.input_spell_correction(tokenized_input)
# print(tokenized_input)

# stemmed_tokenized_input = normalization.stem_list_of_token(tokenized_input)
# print(stemmed_tokenized_input)
# pos_tagged_input = nltk.pos_tag(stemmed_tokenized_input)
pos_tagged_input = nltk.pos_tag(tokenized_input)

# Normalized here
stemmed_tokenized_output = normalization.stem_list_of_token_awal(pos_tagged_input)
print('Stemmed: ', stemmed_tokenized_output)

normalized_tokenized_output = normalization.lemmatize_list_of_token_awal(stemmed_tokenized_output)

print('Lemmatized: ', normalized_tokenized_output)
pos_tagged_input = normalized_tokenized_output
# sys.exit()

# print('Pos tagged input:')
# print(pos_tagged_input)
# print(pos_tagged_input)
featured_input = feature_extraction.sent2features(pos_tagged_input)
# print(featured_input)

iob_prediction = crf.predict_single(featured_input)
# print(tokenized_input)
# print(iob_prediction)

# Spell checking disini aja setelah predict named entity
# Kadang masih sering error ini
# tokenized_input = spell_checker.input_spell_correction(tokenized_input, iob_prediction)
# print('Spell checking')
# print(tokenized_input)

# Kasi kasus disini, kalo dia location dibandingin ama attribut mana aja di user profil, dkk
user_dict = fetch_user_profile.get_data(sys.argv[3])
# print(user_dict)
predicted_sentence_cooccurence = []

# Print prediction in IOB format
# print(iob_prediction)

# Sebelum ini harusnya preprocessing dulu, digabungin semua yang B sama I
# List of tuple (string, ner)
ner_prediction = []
curr_items = ""
i = 0

while (i<len(iob_prediction)):
    if("B" in iob_prediction[i]):
        ner_tag = iob_prediction[i][2:]
        # curr_items = tokenized_input[i]
        curr_items = pos_tagged_input[i][0]
        i = i + 1
        while("I" in iob_prediction[i]):
            # curr_items = curr_items + " " + tokenized_input[i]
            curr_items = curr_items + " " + pos_tagged_input[i][0]
            i = i + 1
            # Buggy for end of sentence : if(i >= len(iob_prediction)-1):
            if(i >= len(iob_prediction)):
                break
        ner_prediction.append((curr_items, ner_tag))
        i = i - 1
    else:
        # curr_items = tokenized_input[i]
        curr_items = pos_tagged_input[i][0]
        ner_tag = iob_prediction[i]
        ner_prediction.append((curr_items, ner_tag))
    i = i + 1

# for tup in ner_prediction:
#     print(tup)

# Ambil smua yang ke tagged_named_entity
# Bandingin sama yang sama (person dgn person) dah trus baru itung co-occurence terbesarnya

i = 0
for chunk_tuple in ner_prediction:
    co_occurence = 0
    # print(chunk_tuple[1])
    if ("per" == chunk_tuple[1]):
        # Compare with full name
        co_occurence = google_search.co_occurence(user_dict['full_name'], chunk_tuple[0])
    elif ("org" == chunk_tuple[1]):
        # Compare with education, work
        co_occurence_1 = google_search.co_occurence(user_dict['education'], chunk_tuple[0])
        co_occurence_2 = google_search.co_occurence(user_dict['work'], chunk_tuple[0])
        if (co_occurence_1 > co_occurence_2):
            co_occurence = co_occurence_1
        else:
            co_occurence = co_occurence_2
    elif ("geo" == chunk_tuple[1]):
        # Compare with hometown_city, current_city,
        co_occurence_1 = google_search.co_occurence(user_dict['hometown_city'], chunk_tuple[0])
        co_occurence_2 = google_search.co_occurence(user_dict['current_city'], chunk_tuple[0])
        if (co_occurence_1 > co_occurence_2):
            co_occurence = co_occurence_1
        else:
            co_occurence = co_occurence_2

    predicted_sentence_cooccurence.append(co_occurence)

# print(predicted_sentence_cooccurence)

anonymize_predicted_sentence = anonymization.simple_anonymization(ner_prediction)
final_sentence = postprocessing.restructure_sentence(anonymize_predicted_sentence)

# print('Original text : ')
# print(text_input)
# print('Anonymized text : ')
# print(final_sentence)
#
# print('Similarity : ')
# print(sentence_similarity.symmetric_sentence_similarity(text_input, final_sentence))

# print('Stemmed:')
# print(stemmed_tokenized_output)
# normalized_tokenized_output = normalization.lemmatize_list_of_token(stemmed_tokenized_output, pos_tagged_list)
# normalized_tokenized_output = stemmed_tokenized_output
normalized_tokenized_output = ner_prediction
# print('Lemmatized:')
# print(normalized_tokenized_output)

# Buat yang alphanya di bawah threshold (co-occurencenya kecil), di cek lagi sama rule based approach
# loc_candidate_phrases = sample_rule_based.identify_candidate_private_locational_phrases(ner_prediction)
loc_candidate_phrases = sample_rule_based.identify_candidate_private_locational_phrases(normalized_tokenized_output)
print('Step 3a : ')
print(loc_candidate_phrases)
non_neg_loc_candidate_phrases = sample_rule_based.check_negative_phrases(loc_candidate_phrases)
print('Step 4a : ')
print(non_neg_loc_candidate_phrases)
private_loc_candidate_phrases = sample_rule_based.check_non_private_locational_verb(non_neg_loc_candidate_phrases)
print('Step 5a : ')
print(private_loc_candidate_phrases)
truly_private_loc_candidate_phrases = sample_rule_based.check_private_locational_verb(private_loc_candidate_phrases)
print('Step 6a : ')
print(truly_private_loc_candidate_phrases)

org_candidate_phrases = sample_rule_based.identify_candidate_private_organizational_phrases(ner_prediction)
print('Step 3b : ')
print(org_candidate_phrases)
non_neg_org_candidate_phrases = sample_rule_based.check_negative_phrases(org_candidate_phrases)
print('Step 4b : ')
print(non_neg_org_candidate_phrases)
private_org_candidate_phrases = sample_rule_based.check_non_private_organizational_verb(non_neg_org_candidate_phrases)
print('Step 5b : ')
print(private_org_candidate_phrases)
truly_private_org_candidate_phrases = sample_rule_based.check_private_organizational_verb(private_org_candidate_phrases)
print('Step 6b : ')
print(truly_private_org_candidate_phrases)

# Sample run
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl 'Yes, I currently stay in Japan for six weeks to do research internship at Gifu National College of Technology' 'Geraldi Dzakwan'
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "How many time I'll tell you that I'm not from California?" "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "I really want to fly out to Los Angeles and meet all the amazing people/artists out there." "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "I live in Seattle, do you know what station is showing your new show?" "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "I live in Jakarta. I work at Qontak company." "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "Currently, I am living at San Frasisco Bay Area. I am now working at Palantyr Software." "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "Last month, I went to Bali for vacation" "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "Lastt monntth, Iii weennt to Bali for vacationnn" "Geraldi Dzakwan"
# python simple_crf_gmb.py save_model_crf_gmb_dua_kali.pkl "On June 24th, Ii weennt to Bali for vacationnn" "Geraldi Dzakwan"
