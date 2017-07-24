import sys
import MySQLdb
import requests, json
from random import randint

def get_name_list():
    db = MySQLdb.connect(host="localhost",      # your host, usually localhost
                         user="root",           # your username
                         passwd="",             # your password
                         db="english_corpus")   # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM name_corpus';
    cur.execute(query)
    ret_dict = {}
    gen_dict = {}
    ret_dict['first_name'] = {}
    ret_dict['last_name'] = []
    gen_dict['+'] = []
    gen_dict['-'] = []

    for row in cur.fetchall():
        if(row['pos'] == 'last_name'):
            ret_dict['last_name'].append(row['word'])
        else:
            gen_dict[row['gender']].append(row['word'])

    ret_dict['first_name']['+'] = gen_dict['+']
    ret_dict['first_name']['-'] = gen_dict['-']

    db.close()
    return ret_dict

def get_first_name(name):
    first_name = ""
    for i in range(0, len(name)):
        if(name[i] == " "):
            break
        else:
            first_name = first_name + name[i]

    return first_name

def get_genders(names):
    url = ""
    cnt = 0
    if not isinstance(names, list):
        names = [names,]

    for name in names:
        first_name = get_first_name(name)
        if url == "":
            url = "name[0]=" + first_name
        else:
            cnt += 1
            url = url + "&name[" + str(cnt) + "]=" + first_name

    req = requests.get("https://api.genderize.io?" + url)
    results = json.loads(req.text)

    retrn = []

    for result in results:
        if(result["gender"] is not None):
            retrn.append((result["gender"], result["probability"], result["count"]))
        else:
            retrn.append((u'None',u'0.0',0.0))

    return retrn

def get_gender_info_only(name):
    name_list = []
    name_list.append(name)
    gender_list = get_genders(name_list)

    # print('Gender list:')
    # print(gender_list)

    gender_tuple = gender_list[0]
    gender = gender_tuple[0]

    return gender

def number_of_words(name):
    ret = 1
    for i in range (0, len(name)):
        if(name[i] == ' '):
            ret = ret + 1
    return ret

def anonymize_all_person(normalized_tokenized_output, all_idx):
    name_list = get_name_list()
    male_list = name_list['first_name']['+']
    m = len(male_list)
    female_list = name_list['first_name']['-']
    n = len(female_list)
    surname_list = name_list['last_name']
    o = len(surname_list)

    solution_dict = {}

    for idx in all_idx:
        if(normalized_tokenized_output[idx][0] not in solution_dict):
            # Get gender from API
            name = normalized_tokenized_output[idx][0]
            number_of_word = number_of_words(name)

            gender = get_gender_info_only(name)

            if (gender == None):
                sys.exit('New case gender None')
            else:
                if(gender == 'male'):
                    # Nanti ini bisa diganti jadi yang terdekat, kalo niat, NGK USAH DUDE TY
                    if(number_of_word == 1):
                        rand_int = randint(0, m-1)
                        solution_dict[normalized_tokenized_output[idx][0]] = male_list[rand_int]
                        normalized_tokenized_output[idx][0] = male_list[rand_int]
                    else:
                        rand_int_first_name = randint(0, m-1)
                        rand_int_last_name = randint(0, o-1)
                        solution_dict[normalized_tokenized_output[idx][0]] = male_list[rand_int_first_name] + " " + surname_list[rand_int_last_name]
                        normalized_tokenized_output[idx][0] = male_list[rand_int_first_name] + " " + surname_list[rand_int_last_name]
                elif(gender == 'female'):
                    if(number_of_word == 1):
                        rand_int = randint(0, n-1)
                        solution_dict[normalized_tokenized_output[idx][0]] = female_list[rand_int]
                        normalized_tokenized_output[idx][0] = female_list[rand_int]
                    else:
                        rand_int_first_name = randint(0, n-1)
                        rand_int_last_name = randint(0, o-1)
                        solution_dict[normalized_tokenized_output[idx][0]] = female_list[rand_int_first_name] + " " + surname_list[rand_int_last_name]
                        normalized_tokenized_output[idx][0] = female_list[rand_int_first_name] + " " + surname_list[rand_int_last_name]
                else:
                    sys.exit('New case strange')
        else:
            normalized_tokenized_output[idx][0] = solution_dict[normalized_tokenized_output[idx][0]]

    return normalized_tokenized_output

if __name__ == '__main__':
    # print(get_name_list())

    # if(len(sys.argv) < 2):
    #     sys.exit('Supply name')
    # name_list = []
    # for i in range(1, len(sys.argv)):
    #     name_list.append(sys.argv[i])
    # print(get_genders(name_list))

    # name_list = get_name_list()
    # print(name_list)

    print(get_gender_info_only(sys.argv[1]))
