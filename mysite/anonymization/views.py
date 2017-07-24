# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import sys
import nltk
import sklearn
import sklearn_crfsuite
import cPickle

import fetch_user_profile
import google_search
import access_gmb_corpus
import feature_extraction
import anonymization
import postprocessing
import sentence_similarity
import sample_rule_based
import normalization
import temporal_phrase_tagger
import location_generalization
import genderize
import org_anonymization

def load_or_train_crf(load, filename):
    crf = None

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
        with open(filename, 'rb') as fid:
            crf = cPickle.load(fid)

    return crf

def add_full_stop(text):
    if(text[len(text) - 1] != '.'):
        text = text + '.'
    return text

def do_pos_tag(text_input):
    tokenized_input = nltk.word_tokenize(text_input)

    # Spell checking disini, tapi ternyata yang named entity ikut keubah jadi jangan
    # tokenized_input = spell_checker.input_spell_correction(tokenized_input)
    # print(tokenized_input)

    pos_tagged_input = nltk.pos_tag(tokenized_input)
    # print('POS Tagged ONLY:')
    # print(pos_tagged_input)
    # print('----------')

    # Normalized here
    stemmed_tokenized_output = normalization.stem_list_of_token_awal(pos_tagged_input)
    # print('Stemmed: ', stemmed_tokenized_output)

    normalized_tokenized_output = normalization.lemmatize_list_of_token_awal(stemmed_tokenized_output)

    # print('Lemmatized: ', normalized_tokenized_output)
    list_of_ret = []
    list_of_ret.append(normalized_tokenized_output)

    normalized_original_token = []
    for i in range(0, len(normalized_tokenized_output)):
        normalized_original_token.append((normalized_tokenized_output[i][0], pos_tagged_input[i][0]))

    list_of_ret.append(normalized_original_token)
    return list_of_ret

def extract_features(pos_tagged_input):
    featured_input = feature_extraction.sent2features(pos_tagged_input)
    # print(featured_input)
    return featured_input

def predict_named_entity(crf, featured_input):
    iob_prediction = crf.predict_single(featured_input)
    # print(tokenized_input)

    return iob_prediction

    # Spell checking disini aja setelah predict named entity
    # Kadang masih sering error ini
    # tokenized_input = spell_checker.input_spell_correction(tokenized_input, iob_prediction)
    # print('Spell checking')
    # print(tokenized_input)

    # Print prediction in IOB format
    # print(iob_prediction)

def combine_named_entity_chunks(pos_tagged_input, iob_prediction):
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
            tuple_list = []
            tuple_list.append(curr_items)
            tuple_list.append(ner_tag)
            ner_prediction.append(tuple_list)
            i = i - 1
        else:
            # curr_items = tokenized_input[i]
            curr_items = pos_tagged_input[i][0]
            ner_tag = iob_prediction[i]
            tuple_list = []
            tuple_list.append(curr_items)
            tuple_list.append(ner_tag)
            ner_prediction.append(tuple_list)
        i = i + 1

    return ner_prediction
    # for tup in ner_prediction:
    #     print(tup)


# Ambil smua yang ke tagged_named_entity
# Bandingin sama yang sama (person dgn person) dah trus baru itung co-occurence terbesarnya
def co_occurence_calculation(username, ner_prediction):
    # Kasi kasus disini, kalo dia location dibandingin ama attribut mana aja di user profil, dkk
    user_dict = fetch_user_profile.get_data(username)
    # print(user_dict)
    predicted_sentence_cooccurence = []

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
    return predicted_sentence_cooccurence

# Ambil smua yang ke tagged_named_entity
# Bandingin sama yang sama (person dgn person) dah trus baru itung co-occurence terbesarnya
def co_occurence_calculation_2(username, ner_prediction):
    # Kasi kasus disini, kalo dia location dibandingin ama attribut mana aja di user profil, dkk
    user_dict = fetch_user_profile.get_data(username)
    # print(user_dict)
    # predicted_sentence_cooccurence = []

    for i in range(0, len(ner_prediction)):
        co_occurence_dict = {}
        highest_co_occurence = 0
        # print(chunk_tuple[1])
        if ("O" == ner_prediction[i][1]):
            # Compare with all
            co_occurence_dict['education'] = google_search.co_occurence(user_dict['education'], ner_prediction[i][0])
            co_occurence_dict['work'] = google_search.co_occurence(user_dict['work'], ner_prediction[i][0])
            # co_occurence_dict['email_address'] = google_search.co_occurence(user_dict['email_address'], ner_prediction[i][0])
            co_occurence_dict['full_name'] = google_search.co_occurence(user_dict['full_name'], ner_prediction[i][0])
            co_occurence_dict['hometown_city'] = google_search.co_occurence(user_dict['hometown_city'], ner_prediction[i][0])
            co_occurence_dict['current_city'] = google_search.co_occurence(user_dict['current_city'], ner_prediction[i][0])

            key = 'None'
            value = 0
            for keys in co_occurence_dict.keys():
                value = co_occurence_dict[keys]
                if(value > highest_co_occurence):
                    highest_co_occurence = value
                    key = keys

            if(key != 'None'):
                print('MASUK SINI GAN')
                if(value >= 0,03):
                    if(key == 'education' or key == 'work'):
                        ner_prediction[i][1] = 'org'
                    elif(key == 'full_name'):
                        ner_prediction[i][1] = 'per'
                    elif(key == 'hometown_city' or key == 'current_city'):
                        ner_prediction[i][1] = 'geo'
                print(key, value, ner_prediction[i][1])

            # predicted_sentence_cooccurence.append(co_occurence)
        else:
            pass
            # predicted_sentence_cooccurence.append(co_occurence)

    # print(predicted_sentence_cooccurence)
    # return predicted_sentence_cooccurence
    return ner_prediction

def simple_anonymize(ner_prediction):
    anonymize_predicted_sentence = anonymization.simple_anonymization(ner_prediction)
    final_sentence = postprocessing.restructure_sentence(anonymize_predicted_sentence)
    return final_sentence

def compute_similarity(text_input, final_sentence):
    # print('Original text : ')
    # print(text_input)
    # print('Anonymized text : ')
    # print(final_sentence)

    # print('Similarity : ')
    return sentence_similarity.symmetric_sentence_similarity(text_input, final_sentence)

# Note : sementara genderize masih pake first name, mayan akurat
def identify_person_entity_further(ner_prediction):
    # print('PERSON ENTITY FURTHER')
    for token_tuple in ner_prediction:
        noun = token_tuple[0]
        ner = token_tuple[1]

        if(noun[0].isupper()):
            gender = genderize.get_gender_info_only(noun)
            # print(noun, gender)
            if(gender != 'None'):
                token_tuple[1] = 'per'
            else:
                pass
                # Kasus kalo sebenernya bukan person, ntar aja ini
                # if(ner == 'per')
    # print ''
    # print ''
    # print(ner_prediction)
    # Kan udh ke gabung chunknya si ner_prediction, jadi kgk usah chunking lgi
    return ner_prediction

# Buat yang alphanya di bawah threshold (co-occurencenya kecil), di cek lagi sama rule based approach
# loc_candidate_phrases = sample_rule_based.identify_candidate_private_locational_phrases(ner_prediction)
def identify_private_locational_phrases(normalized_tokenized_output, level):
    all_idx = sample_rule_based.private_locational_main_function(normalized_tokenized_output)
    anonymized_loc_sentence = location_generalization.anonymize_all_location(normalized_tokenized_output, all_idx, level)
    print('Anonymize private locational phrases:')
    return anonymized_loc_sentence

def identify_private_personal_phrases(normalized_tokenized_output):
    all_idx = sample_rule_based.private_personal_main_function(normalized_tokenized_output)
    anonymized_per_sentence = genderize.anonymize_all_person(normalized_tokenized_output, all_idx)
    print('Anonymize private personal phrases:')
    return anonymized_per_sentence

def identify_private_organizational_phrases(normalized_tokenized_output):
    all_idx = sample_rule_based.private_organizational_main_function(normalized_tokenized_output)
    anonymized_per_sentence = org_anonymization.anonymize_all_org(normalized_tokenized_output, all_idx)
    print('Anonymize private organizational phrases:')
    return anonymized_per_sentence

def identify_private_event_phrases(normalized_tokenized_output):
    all_idx = sample_rule_based.private_event_main_function(normalized_tokenized_output)
    anonymized_per_sentence = org_anonymization.anonymize_all_event(normalized_tokenized_output, all_idx)
    print('Anonymize private event phrases:')
    return anonymized_per_sentence

# def post_processing_1(normalized_tokenized_output, ner_prediction):
#     anonymized_dict = {}
#     for i in range(0, len(ner_prediction)):
#         if(normalized_tokenized_output[i][0] != ner_prediction[i])
#     pass

def identify_private_temporal_phrases(message):
    # message = ""
    # i = 0
    # for tuples in ner_prediction:
    #     message = message + tuples[0]
    #     i = i + 1
    #     if (i < len(pos_tagged_input)):
    #         message = message + " "

    message = temporal_phrase_tagger.do_temporal_tag(message)

    # Anonymization here

    return message

if __name__ == '__main__':
    # python main.py load save_model_crf_gmb_dua_kali.pkl "On June 24th, I went to Bali for vacation" "Geraldi Dzakwan"
    # python main.py load save_model_crf_gmb_dua_kali.pkl "My sister's name is Alice. Alice lives in Jakarta." "Geraldi Dzakwan"
    # python main.py load save_model_crf_gmb_dua_kali.pkl "I live in Jakarta with my sister, Alice." "Geraldi Dzakwan"
    # python main.py load save_model_crf_gmb_dua_kali.pkl 'Cristiano Ronaldo is a football player for Real Madrid and Portugal national team.' "Geraldi Dzakwan"
    # python main.py load "save_model_crf_gmb_dua_kali.pkl" "My hometown is Jakarta. My favorite food is fried rice. I've studied at Bandung Institute of Technology for three years  majoring in computer science." "Geraldi Dzakwan"
    # python main.py load "save_model_crf_gmb_dua_kali.pkl" "I will meet my sister, Alice, at 3 pm maybe around Motosu." "Geraldi Dzakwan"
    # python main.py load "save_model_crf_gmb_dua_kali.pkl" "I am one of the member of Youth Foundation in Bandung." "Geraldi Dzakwan"

    if(len(sys.argv) < 5):
        sys.exit('Wrong arguments')

    crf = None
    if(sys.argv[1] == 'load'):
        crf = load_or_train_crf(True, sys.argv[2])
    elif(sys.argv[1] == 'save'):
        crf = load_or_train_crf(False, sys.argv[2])
    else:
        sys.exit('Wrong 1st arguments')

    input_message = sys.argv[3]
    input_message = add_full_stop(input_message)

    # Di awal aja
    anonymized_temporal_message = identify_private_temporal_phrases(input_message)
    is_generalized_temporal = not (input_message == anonymized_temporal_message)
    # print('')
    # print('')
    # print('')

    list_of_ret = do_pos_tag(anonymized_temporal_message)
    # list_of_ret_2 = do_pos_tag(input_message)
    pos_tagged_input = list_of_ret[0]
    normalized_original_token = list_of_ret[1]

    # Ini yg bener2 asli kgk di anonymize temporalnya
    # normalized_original_token_2 = list_of_ret_2[1]
    # print(list_of_ret[1])
    # sys.exit()
    featured_input = extract_features(pos_tagged_input)
    iob_prediction = predict_named_entity(crf, featured_input)
    ner_prediction = combine_named_entity_chunks(pos_tagged_input, iob_prediction)

    # Di sini genderize.io pake buat nambel NER person
    # print('Sebelum : ')
    # print(ner_prediction)
    # print ''
    # print ''
    # ner_prediction = identify_person_entity_further(ner_prediction)
    # print('Sesudah : ')
    # print(ner_prediction)
    # print ''
    # print ''

    # predicted_sentence_cooccurence = co_occurence_calculation(sys.argv[4], ner_prediction)
    # KUOTA ABIS
    # ner_prediction = co_occurence_calculation_2(sys.argv[4], ner_prediction)
    # print('This is it:')
    # print(ner_prediction)
    # sys.exit()

    print('')
    print('')
    print('')
    print('POS Tagging, Stemming, and Lemmatization:')
    print(pos_tagged_input)
    print('')
    print('')
    print('')
    print('Named entity recognition and combining chunks:')
    print(iob_prediction)
    print('')
    print('')
    print('')
    print(ner_prediction)
    print('')
    print('')
    print('')
    # print(predicted_sentence_cooccurence)
    # print('----------')
    print(identify_private_locational_phrases(ner_prediction, 1))
    print('')
    print('')
    print('')
    print(identify_private_organizational_phrases(ner_prediction))
    print('')
    print('')
    print('')
    print(identify_private_personal_phrases(ner_prediction))
    print('')
    print('')
    print('')
    print(identify_private_event_phrases(ner_prediction))
    print('')
    print('')
    print('')

    # Ntar disatuin ama threshold dan co-occurence yang LOC sama ORG besok
    # PERSON pikirin lagi
    # Time/temporal phrase di akhir aja

    # print ''
    # print ''
    # print (ner_prediction)

    list_of_post_ret = postprocessing.rebuild_to_original(ner_prediction, normalized_original_token)
    anonymized_text_with_space = list_of_post_ret[0]
    original_text_with_space = list_of_post_ret[1]

    # Di awal aja
    # anonymized_text_with_space = identify_private_temporal_phrases(anonymized_text_with_space)
    # print('')
    # print('')
    # print('')

    print('Final anonymized sentence:')
    print(anonymized_text_with_space)
    print('')
    print('')
    print('')

    print('Similarity measure value:')
    similarity = compute_similarity(original_text_with_space, anonymized_text_with_space)
    if(similarity == 1.0 and is_generalized_temporal):
        similarity = compute_similarity(input_message, anonymized_text_with_space)
    print(similarity)


@csrf_exempt
def index(request):
    if (request.method == 'GET'):
        text = 'Welcome to English message anonymization API.'
        text += '\n\n'
        text += 'You can access several routes:'
        text += '\n'
        text += '1. "/anonymization/train" to train new model.'
        text += '\n'
        text += '2. "/anonymization/load" to load your trained model.'
        text += '\n'
        text += '3. "/anonymization/anonymize" to anonymize your message.'
        text += '\n\n'
        text += 'Use GET method to see the detailed explanation for each route.'
        text += '\n'
        text += 'Use POST method to execute the functionality of each route.'
    elif (request.method == 'POST'):
        text = 'Index routing has no POST handling mechanism.'

    return HttpResponse(text)

@csrf_exempt
def anonymize(request):
    if (request.method == 'GET'):
        text = 'Welcome to anonymize route.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    message: "My friend, Ibrahim, comes from France."' + '\n' +'}'
        return HttpResponse(text)
    elif (request.method == 'POST'):
        text = request.POST.get('message')
        username = request.POST.get('username')
        if (text == None or username == None):
            text = 'Wrong JSON format sent.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    message: "My friend, Ibrahim, comes from France."' + '\n'
        else:
            # python main.py load save_model_crf_gmb_dua_kali.pkl "On June 24th, I went to Bali for vacation" "Geraldi Dzakwan"
            # python main.py load save_model_crf_gmb_dua_kali.pkl "My sister's name is Alice. Alice lives in Jakarta." "Geraldi Dzakwan"
            # python main.py load save_model_crf_gmb_dua_kali.pkl "I live in Jakarta with my sister, Alice." "Geraldi Dzakwan"
            # python main.py load save_model_crf_gmb_dua_kali.pkl 'Cristiano Ronaldo is a football player for Real Madrid and Portugal national team.' "Geraldi Dzakwan"
            # python main.py load "save_model_crf_gmb_dua_kali.pkl" "My hometown is Jakarta. My favorite food is fried rice. I've studied at Bandung Institute of Technology for three years  majoring in computer science." "Geraldi Dzakwan"
            # python main.py load "save_model_crf_gmb_dua_kali.pkl" "I will meet my sister, Alice, at 3 pm maybe around Motosu." "Geraldi Dzakwan"
            # python main.py load "save_model_crf_gmb_dua_kali.pkl" "I am one of the member of Youth Foundation in Bandung." "Geraldi Dzakwan"

            crf = None
            crf = load_or_train_crf(True, "save_model_crf_gmb_dua_kali.pkl")

            input_message = text
            input_message = add_full_stop(input_message)

            # Di awal aja
            anonymized_temporal_message = identify_private_temporal_phrases(input_message)
            is_generalized_temporal = not (input_message == anonymized_temporal_message)
            # print('')
            # print('')
            # print('')

            list_of_ret = do_pos_tag(anonymized_temporal_message)
            # list_of_ret_2 = do_pos_tag(input_message)
            pos_tagged_input = list_of_ret[0]
            normalized_original_token = list_of_ret[1]

            # Ini yg bener2 asli kgk di anonymize temporalnya
            # normalized_original_token_2 = list_of_ret_2[1]
            # print(list_of_ret[1])
            # sys.exit()
            featured_input = extract_features(pos_tagged_input)
            iob_prediction = predict_named_entity(crf, featured_input)
            ner_prediction = combine_named_entity_chunks(pos_tagged_input, iob_prediction)

            # Di sini genderize.io pake buat nambel NER person
            # print('Sebelum : ')
            # print(ner_prediction)
            # print ''
            # print ''
            # ner_prediction = identify_person_entity_further(ner_prediction)
            # print('Sesudah : ')
            # print(ner_prediction)
            # print ''
            # print ''

            # predicted_sentence_cooccurence = co_occurence_calculation(username, ner_prediction)
            # KUOTA ABIS
            # ner_prediction = co_occurence_calculation_2(username, ner_prediction)
            # print('This is it:')
            # print(ner_prediction)
            # sys.exit()

            print('')
            print('')
            print('')
            print('POS Tagging, Stemming, and Lemmatization:')
            print(pos_tagged_input)
            print('')
            print('')
            print('')
            print('Named entity recognition and combining chunks:')
            print(iob_prediction)
            print('')
            print('')
            print('')
            print(ner_prediction)
            print('')
            print('')
            print('')
            # print(predicted_sentence_cooccurence)
            # print('----------')
            print(identify_private_locational_phrases(ner_prediction, 1))
            print('')
            print('')
            print('')
            print(identify_private_organizational_phrases(ner_prediction))
            print('')
            print('')
            print('')
            print(identify_private_personal_phrases(ner_prediction))
            print('')
            print('')
            print('')
            print(identify_private_event_phrases(ner_prediction))
            print('')
            print('')
            print('')

            # Ntar disatuin ama threshold dan co-occurence yang LOC sama ORG besok
            # PERSON pikirin lagi
            # Time/temporal phrase di akhir aja

            # print ''
            # print ''
            # print (ner_prediction)

            list_of_post_ret = postprocessing.rebuild_to_original(ner_prediction, normalized_original_token)
            anonymized_text_with_space = list_of_post_ret[0]
            original_text_with_space = list_of_post_ret[1]

            # Di awal aja
            # anonymized_text_with_space = identify_private_temporal_phrases(anonymized_text_with_space)
            # print('')
            # print('')
            # print('')

            print('Final anonymized sentence:')
            print(anonymized_text_with_space)
            print('')
            print('')
            print('')

            print('Similarity measure value:')
            similarity = compute_similarity(original_text_with_space, anonymized_text_with_space)
            if(similarity == 1.0 and is_generalized_temporal):
                similarity = compute_similarity(input_message, anonymized_text_with_space)
            print(similarity)

            return HttpResponse("Anonymized text: " + anonymized_text_with_space + "\n\n" + "Similarity value: " + str(similarity))
