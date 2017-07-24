import sys
import csv
import MySQLdb

single_quote = "'"
double_quote = '"'
comma = ", "

def fuse_with_double_quote(word, is_comma):
    if(is_comma):
        return double_quote + word + double_quote + comma
    else:
        return double_quote + word + double_quote

def fuse_with_single_quote(word, is_comma):
    if(is_comma):
        return single_quote + word + single_quote + comma
    else:
        return single_quote + word + single_quote

def all_data_string(loc_list, idx):
    if('"' not in loc_list[idx]['continent_name']):
        str1 = fuse_with_double_quote(loc_list[idx]['continent_name'], True)
    else:
        str1 = fuse_with_single_quote(loc_list[idx]['continent_name'], True)

    if('"' not in loc_list[idx]['country_name']):
        str2 = fuse_with_double_quote(loc_list[idx]['country_name'], True)
    else:
        str2 = fuse_with_single_quote(loc_list[idx]['country_name'], True)

    if('"' not in loc_list[idx]['subdivision_1_name']):
        str3 = fuse_with_double_quote(loc_list[idx]['subdivision_1_name'], True)
    else:
        str3 = fuse_with_single_quote(loc_list[idx]['subdivision_1_name'], True)

    if('"' not in loc_list[idx]['subdivision_2_name']):
        str4 = fuse_with_double_quote(loc_list[idx]['subdivision_2_name'], True)
    else:
        str4 = fuse_with_single_quote(loc_list[idx]['subdivision_2_name'], True)

    if('"' not in loc_list[idx]['city_name']):
        str5 = fuse_with_double_quote(loc_list[idx]['city_name'], False)
    else:
        str5 = fuse_with_single_quote(loc_list[idx]['city_name'], False)

    return str1 + str2 + str3 + str4 + str5

def fill_loc_list(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)

        loc_list = []
        for i in range(1, len(your_list)):
            data_dict = {}
            data_dict['continent_name'] = your_list[i][3]
            data_dict['country_name'] = your_list[i][5]
            data_dict['subdivision_1_name'] = your_list[i][7]
            data_dict['subdivision_2_name'] = your_list[i][9]
            data_dict['city_name'] = your_list[i][10]
            loc_list.append(data_dict)

    return loc_list

if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        filename = 'GeoData/GeoLite2-City-Locations-en.csv'
    else:
        filename = sys.argv[1]

    loc_list = fill_loc_list(filename)

    db = MySQLdb.connect (  host="localhost",       # your host, usually localhost
                            user="root",            # your username
                            passwd="",              # your password
                            db="english_corpus")    # name of the data base

    cur = db.cursor()

    for i in range(1, len(loc_list)):
        print(i)
        if (i >= 8932):
            all_data = all_data_string(loc_list, i)
            query = 'INSERT INTO location (continent_name, country_name, subdivision_1_name, subdivision_2_name, city_name) VALUES (' + all_data + ')';

            try:
                cur.execute(query)
                db.commit()
            except:
                db.rollback()
                sys.exit('Invalid query : ' + query)

    db.close()
