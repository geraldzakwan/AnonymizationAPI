import sys
import MySQLdb

def get_data(user_fullname):
    ret_dict = {}

    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM user_profile WHERE full_name = ' + '"' + user_fullname + '"';
    cur.execute(query)

    for row in cur.fetchall():
        ret_dict['education'] = row['education']
        ret_dict['work'] = row['work']
        ret_dict['email_address'] = row['email_address']
        ret_dict['full_name'] = row['full_name']
        ret_dict['hometown_city'] = row['hometown_city']
        ret_dict['current_city'] = row['current_city']

    db.close()

    # print(ret_dict)

    return ret_dict
