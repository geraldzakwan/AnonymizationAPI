import sys
import nltk
import MySQLdb

# text_input = sys.argv[1]
# tokenized_input = nltk.word_tokenize(text_input)
# pos_tagged_input = nltk.pos_tag(tokenized_input)
#
# print(pos_tagged_input)

def identify_candidate_private_locational_phrases(ner_prediction):
    # print(ner_prediction)

    list_of_ner = [item[1] for item in ner_prediction]
    list_of_token = [item[0] for item in ner_prediction]

    # List all locations
    loc_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "geo"):
            loc_index_list.append(i)

    # List all locations
    org_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "org"):
            org_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i" or list_of_token[i] == "My" or list_of_token[i] == "my"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    # print(list_of_ner)
    # print(list_of_token)

    # print(loc_index_list)
    # print(org_index_list)
    # print(i_index_list)
    # print(dot_index_list)

    loc_candidate_phrases = []

    for idx_loc in loc_index_list:
        for idx_i in i_index_list:
            if(idx_i < idx_loc):
                # Cek apakah kepotong titik antara I/My dengan lokasi
                is_cut = False
                for idx_dot in dot_index_list:
                    if(idx_dot > idx_i and idx_dot < idx_loc):
                        is_cut = True

                if(not is_cut):
                    token_list = []
                    for i in range(idx_i, idx_loc+1):
                        token_list.append(list_of_token[i])
                    loc_candidate_phrases.append(token_list)

    return loc_candidate_phrases

def identify_candidate_private_event_phrases(ner_prediction):
    # print(ner_prediction)

    list_of_ner = [item[1] for item in ner_prediction]
    list_of_token = [item[0] for item in ner_prediction]

    # List all events
    loc_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "eve"):
            loc_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i" or list_of_token[i] == "My" or list_of_token[i] == "my"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    # print(list_of_ner)
    # print(list_of_token)

    # print(loc_index_list)
    # print(org_index_list)
    # print(i_index_list)
    # print(dot_index_list)

    loc_candidate_phrases = []

    for idx_loc in loc_index_list:
        for idx_i in i_index_list:
            if(idx_i < idx_loc):
                # Cek apakah kepotong titik antara I/My dengan lokasi
                is_cut = False
                for idx_dot in dot_index_list:
                    if(idx_dot > idx_i and idx_dot < idx_loc):
                        is_cut = True

                if(not is_cut):
                    token_list = []
                    for i in range(idx_i, idx_loc+1):
                        token_list.append(list_of_token[i])
                    loc_candidate_phrases.append(token_list)

    return loc_candidate_phrases

def identify_candidate_private_organizational_phrases(ner_prediction):
    list_of_ner = [item[1] for item in ner_prediction]
    list_of_token = [item[0] for item in ner_prediction]

    # List all organization
    org_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "org"):
            org_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i" or list_of_token[i] == "My" or list_of_token[i] == "my"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    org_candidate_phrases = []

    for idx_org in org_index_list:
        for idx_i in i_index_list:
            if(idx_i < idx_org):
                # Cek apakah kepotong titik antara I/My dengan lokasi
                is_cut = False
                for idx_dot in dot_index_list:
                    if(idx_dot > idx_i and idx_dot < idx_org):
                        is_cut = True

                if(not is_cut):
                    token_list = []
                    for i in range(idx_i, idx_org+1):
                        token_list.append(list_of_token[i])
                    org_candidate_phrases.append(token_list)

    return org_candidate_phrases

def identify_candidate_private_personal_phrases(ner_prediction):
    list_of_ner = [item[1] for item in ner_prediction]
    list_of_token = [item[0] for item in ner_prediction]

    # List all person
    per_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "per"):
            per_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i" or list_of_token[i] == "My" or list_of_token[i] == "my"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    per_candidate_phrases = []

    for idx_org in per_index_list:
        for idx_i in i_index_list:
            if(idx_i < idx_org):
                # Cek apakah kepotong titik antara I/My dengan person
                is_cut = False
                for idx_dot in dot_index_list:
                    if(idx_dot > idx_i and idx_dot < idx_org):
                        is_cut = True

                if(not is_cut):
                    token_list = []
                    for i in range(idx_i, idx_org+1):
                        token_list.append(list_of_token[i])
                    per_candidate_phrases.append(token_list)


    # print('Candidate phrases person:')
    # print(per_candidate_phrases)
    # print ''
    # print ''
    # print ''
    return per_candidate_phrases

def check_negative_phrases(list_candidate_phrases):
    candidate_phrases_without_negative = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM negative_words';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in list_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(not is_inside):
            candidate_phrases_without_negative.append(candidate_phrases)

        # is_negative = False
        # for token in candidate_phrases:
        #     if(token == "no" or token == "not" or token =="never"):
        #         is_negative = True
        #
        # if(not is_negative):
        #     candidate_phrases_without_negative.append(candidate_phrases)

    return candidate_phrases_without_negative

def check_non_private_event_verb(non_neg_loc_candidate_phrases):
    private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM non_private_event_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in non_neg_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(not is_inside):
            private_loc_candidate_phrases.append(candidate_phrases)

    return private_loc_candidate_phrases

def check_non_private_locational_verb(non_neg_loc_candidate_phrases):
    private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM non_private_locational_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in non_neg_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(not is_inside):
            private_loc_candidate_phrases.append(candidate_phrases)

    return private_loc_candidate_phrases

def check_private_locational_verb(private_loc_candidate_phrases):
    truly_private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM private_locational_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in private_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(is_inside):
            truly_private_loc_candidate_phrases.append(candidate_phrases)

    return truly_private_loc_candidate_phrases

def check_private_event_verb(private_loc_candidate_phrases):
    truly_private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM private_event_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in private_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(is_inside):
            truly_private_loc_candidate_phrases.append(candidate_phrases)

    return truly_private_loc_candidate_phrases

def check_non_private_organizational_verb(non_neg_loc_candidate_phrases):
    private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM non_private_organizational_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in non_neg_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(not is_inside):
            private_loc_candidate_phrases.append(candidate_phrases)

    return private_loc_candidate_phrases

def check_private_organizational_verb(private_loc_candidate_phrases):
    truly_private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM private_organizational_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in private_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(is_inside):
            truly_private_loc_candidate_phrases.append(candidate_phrases)

    return truly_private_loc_candidate_phrases

def check_non_private_personal_verb(non_neg_loc_candidate_phrases):
    private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM non_private_personal_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in non_neg_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(not is_inside):
            private_loc_candidate_phrases.append(candidate_phrases)

    return private_loc_candidate_phrases

def check_private_personal_verb(private_loc_candidate_phrases):
    truly_private_loc_candidate_phrases = []

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM private_personal_verbs';
    cur.execute(query)

    word_dict = {}
    for row in cur.fetchall():
        # print(row['word'])
        word_dict[row['word']] = True

    db.close()

    for candidate_phrases in private_loc_candidate_phrases:
        is_inside = False
        for i in range(1, len(candidate_phrases)-1):
            if(candidate_phrases[i] in word_dict):
                is_inside = True

        if(is_inside):
            truly_private_loc_candidate_phrases.append(candidate_phrases)

    return truly_private_loc_candidate_phrases

def get_loc_idx(ner_prediction, truly_private_loc_candidate_phrases):
    idx_dict = {}
    # print(ner_prediction)
    for phrase in truly_private_loc_candidate_phrases:
        loc_word = phrase[len(phrase)-1]
        before_word_1 = phrase[len(phrase)-2]
        before_word_2 = phrase[len(phrase)-3]
        idx = 1

        for i in range(2, len(ner_prediction)):
            if(ner_prediction[i][0] == loc_word):
                # print("Masuk : ", loc_word)
                if(ner_prediction[i-1][0] == before_word_1 and ner_prediction[i-2][0] == before_word_2):
                    if i not in idx_dict:
                        idx_dict[i] = True

    return idx_dict

def get_org_idx(ner_prediction, truly_private_loc_candidate_phrases):
    idx_dict = {}
    # print(ner_prediction)
    for phrase in truly_private_loc_candidate_phrases:
        loc_word = phrase[len(phrase)-1]
        before_word_1 = phrase[len(phrase)-2]
        before_word_2 = phrase[len(phrase)-3]
        idx = 1

        for i in range(2, len(ner_prediction)):
            if(ner_prediction[i][0] == loc_word):
                # print("Masuk : ", loc_word)
                if(ner_prediction[i-1][0] == before_word_1 and ner_prediction[i-2][0] == before_word_2):
                    if i not in idx_dict:
                        idx_dict[i] = phrase
                    else:
                        if(len(phrase) > idx_dict[i]):
                            idx_dict[i] = phrase

    return idx_dict

def get_per_idx(ner_prediction, truly_private_loc_candidate_phrases):
    idx_dict = {}
    # print(ner_prediction)
    for phrase in truly_private_loc_candidate_phrases:
        loc_word = phrase[len(phrase)-1]
        before_word_1 = phrase[len(phrase)-2]
        before_word_2 = phrase[len(phrase)-3]
        idx = 1

        for i in range(2, len(ner_prediction)):
            if(ner_prediction[i][0] == loc_word):
                # print("Masuk : ", loc_word)
                if(ner_prediction[i-1][0] == before_word_1 and ner_prediction[i-2][0] == before_word_2):
                    if i not in idx_dict:
                        idx_dict[i] = True

    return idx_dict

def private_locational_main_function(normalized_tokenized_output):
    loc_candidate_phrases = identify_candidate_private_locational_phrases(normalized_tokenized_output)
    # print('Step 3a : ')
    # print(loc_candidate_phrases)
    non_neg_loc_candidate_phrases = check_negative_phrases(loc_candidate_phrases)
    # print('Step 4a : ')
    # print(non_neg_loc_candidate_phrases)
    private_loc_candidate_phrases = check_non_private_locational_verb(non_neg_loc_candidate_phrases)
    # print('Step 5a : ')
    # print(private_loc_candidate_phrases)
    truly_private_loc_candidate_phrases = check_private_locational_verb(private_loc_candidate_phrases)
    # print('Step 6a : ')
    print('Private locational candidate_phrases:')
    print(truly_private_loc_candidate_phrases)
    print ''
    print ''
    print ''

    all_idx = get_loc_idx(normalized_tokenized_output, truly_private_loc_candidate_phrases)
    # print(all_idx)
    return all_idx

def private_organizational_main_function(normalized_tokenized_output):
    org_candidate_phrases = identify_candidate_private_organizational_phrases(normalized_tokenized_output)
    # print('Step 3b : ')
    # print(org_candidate_phrases)
    non_neg_org_candidate_phrases = check_negative_phrases(org_candidate_phrases)
    # print('Step 4b : ')
    # print(non_neg_org_candidate_phrases)
    private_org_candidate_phrases = check_non_private_organizational_verb(non_neg_org_candidate_phrases)
    # print('Step 5b : ')
    # print(private_org_candidate_phrases)
    truly_private_org_candidate_phrases = check_private_organizational_verb(private_org_candidate_phrases)
    # print('Step 6b : ')
    print('Private organizational candidate_phrases:')
    print(truly_private_org_candidate_phrases)
    print ''
    print ''
    print ''

    all_idx = get_org_idx(normalized_tokenized_output, truly_private_org_candidate_phrases)
    # print(all_idx)
    return all_idx

def private_personal_main_function(normalized_tokenized_output):
    per_candidate_phrases = identify_candidate_private_personal_phrases(normalized_tokenized_output)
    # print('Step 3c : ')
    # print(per_candidate_phrases)
    non_neg_per_candidate_phrases = check_negative_phrases(per_candidate_phrases)
    # print('Step 4c : ')
    # print(non_neg_per_candidate_phrases)
    private_per_candidate_phrases = check_non_private_personal_verb(non_neg_per_candidate_phrases)
    # print('Step 5c : ')
    # print(private_per_candidate_phrases)
    truly_private_per_candidate_phrases = check_private_personal_verb(private_per_candidate_phrases)
    # print('Step 6c : ')
    print('Private personal candidate_phrases:')
    print(truly_private_per_candidate_phrases)
    print ''
    print ''
    print ''

    all_idx = get_per_idx(normalized_tokenized_output, truly_private_per_candidate_phrases)

    return all_idx

def private_event_main_function(normalized_tokenized_output):
    per_candidate_phrases = identify_candidate_private_event_phrases(normalized_tokenized_output)
    # print('Step 3c : ')
    # print(per_candidate_phrases)
    non_neg_per_candidate_phrases = check_negative_phrases(per_candidate_phrases)
    # print('Step 4c : ')
    # print(non_neg_per_candidate_phrases)
    private_per_candidate_phrases = check_non_private_event_verb(non_neg_per_candidate_phrases)
    # print('Step 5c : ')
    # print(private_per_candidate_phrases)
    truly_private_per_candidate_phrases = check_private_event_verb(private_per_candidate_phrases)
    # print('Step 6c : ')
    print('Private event candidate_phrases:')
    print(truly_private_per_candidate_phrases)
    print ''
    print ''
    print ''

    all_idx = get_org_idx(normalized_tokenized_output, truly_private_per_candidate_phrases)

    return all_idx
